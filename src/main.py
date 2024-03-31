from fastapi import FastAPI, Request

from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId

app = FastAPI()

app.mount("/static", StaticFiles(directory=f"static"), name="static")
app.mount("/media", StaticFiles(directory=f"media"), name="media")

templates = Jinja2Templates(directory="../templates")

mongo_uri = "mongodb://localhost:27017"

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
    context = {"request": request}
    return templates.TemplateResponse("main.html", context)

@app.get("/video")
async def video(request: Request):        
    context = {"request": request}
    return templates.TemplateResponse("video.html", context)

from pathlib import Path
from fastapi import Response
from fastapi import Header
from typing import IO, Generator
from fastapi.responses import StreamingResponse

# @app.get("/api/video")
# async def video(request: Request, range: str = Header(None)):    
#     CHUNK_SIZE = 1024*1024
#     video_path = Path(__file__).parent / "media/1.mp4"
#     start, end = range.replace("bytes=", "").split("-")
#     start = int(start)
#     end = int(end) if end else start + CHUNK_SIZE
#     with open(video_path, "rb") as video:
#         video.seek(start)
#         data = video.read(end - start)
#         filesize = str(video_path.stat().st_size)
#         headers = {
#             'Content-Range': f'bytes {str(start)}-{str(end)}/{filesize}',
#             'Accept-Ranges': 'bytes'
#         }
#         return Response(data, status_code=206, headers=headers, media_type="video/mp4")

@app.get("/api/video/{video_id}")
async def get_streaming_video(request: Request, video_id: int) -> StreamingResponse:
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


async def open_file(request: Request, video_id: int) -> tuple:
    # video = await Video.objects.get(id=video_id)
    # path = Path(video.path)
    # path = Path(__file__).parent / "media/1.mp4"
    path = Path(__file__).parent / "media/1_1048576.mp4"

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