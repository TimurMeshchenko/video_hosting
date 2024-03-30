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
    # return templates.TemplateResponse("video.html", context)
