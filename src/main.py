from fastapi import FastAPI, Request

from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId
from pathlib import Path
from typing import IO, Generator
from fastapi.responses import StreamingResponse
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

app.mount("/static", StaticFiles(directory=f"static"), name="static")
app.mount("/media", StaticFiles(directory=f"media"), name="media")

templates = Jinja2Templates(directory="../templates")

mongo_uri = f'mongodb://{os.getenv("DB_HOST")}:{os.getenv("DB_PORT")}'

class MongoDBConnection:
    def __init__(self, mongo_uri):
        self.mongo_uri = mongo_uri
        self.client = None

    async def __aenter__(self):
        self.client = AsyncIOMotorClient(self.mongo_uri)
        return self.client

    async def __aexit__(self, *args):
        self.client.close()

@app.get("/")
async def main(request: Request):
    async with MongoDBConnection(mongo_uri) as client:
        db = client.get_database("video_hosting")
        videos_collection = db.get_collection("videos")
        videos = []
        cursor = videos_collection.find()
        async for video in cursor:
            videos.append(video)               
        context = {"request": request, "videos": videos}
        return templates.TemplateResponse("main.html", context)

@app.get("/video/{video_id}")
async def video(request: Request, video_id: str):  
    async with MongoDBConnection(mongo_uri) as client:
        db = client.get_database("video_hosting")
        videos_collection = db.get_collection("videos")
        video = await videos_collection.find_one({"_id": ObjectId(video_id)})       
        context = {"request": request, "video": video}
        return templates.TemplateResponse("video.html", context)

@app.get("/api/video/{video_id}")
async def get_streaming_video(request: Request, video_id: str) -> StreamingResponse:
    file, status_code, content_length, headers = await open_file(request, video_id)
    response = StreamingResponse(
        file,
        media_type='video/mp4',
        status_code=status_code,
    )

    response.headers.update({
        'Accept-Ranges': 'bytes',
        'Content-Length': str(content_length),
        **headers,
    })
    return response


async def open_file(request: Request, video_id: str) -> tuple:
    async with MongoDBConnection(mongo_uri) as client:
        db = client.get_database("video_hosting")
        videos_collection = db.get_collection("videos")
        video = await videos_collection.find_one({"_id": ObjectId(video_id)})  
 
    path = Path(__file__).parent / f"media/videos/{video['file_path']}"
    file = path.open('rb')
    file_size = path.stat().st_size
    content_length = file_size
    status_code = 200
    headers = {}
    content_range = request.headers.get('range')

    if content_range is not None:
        content_range = content_range.strip().lower()
        content_ranges = content_range.split('=')[-1]
        range_start, range_end, *_ = map(str.strip, (content_ranges + '-').split('-'))
        range_start = max(0, int(range_start)) if range_start else 0
        range_end = min(file_size - 1, int(range_end)) if range_end else file_size - 1
        content_length = (range_end - range_start) + 1
        file = ranged(file, start=range_start, end=range_end + 1)
        status_code = 206
        headers['Content-Range'] = f'bytes {range_start}-{range_end}/{file_size}'

    return file, status_code, content_length, headers

def ranged(
    file: IO[bytes],
    start: int = 0,
    end: int = None,
    block_size: int = 8192,
) -> Generator[bytes, None, None]:
    consumed = 0
    file.seek(start)
    while True:
        data_length = min(block_size, end - start - consumed) if end else block_size
        if data_length <= 0:
            break
        data = file.read(data_length)
        if not data:
            break
        consumed += data_length
        yield data

    if hasattr(file, 'close'):
        file.close()