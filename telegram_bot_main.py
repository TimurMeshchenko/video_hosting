import asyncio
import os
import telegram
from dotenv import load_dotenv
import requests
import mimetypes

load_dotenv()

TOKEN = os.getenv("TOKEN")
# CHUNK_SIZE = 8 * 1024 * 1024
CHUNK_SIZE = 1 * 1024 * 1024

async def main():
    bot = telegram.Bot(TOKEN)
    async with bot:
        # print((await bot.get_updates())[0])

        # with open("src/media/144p.mp4", 'rb') as document:
        with open("src/media/1.mp4", 'rb') as document:
            chunks_counter = 0
            while True:
                document.seek(chunks_counter * CHUNK_SIZE)
                chunk = document.read(CHUNK_SIZE)
                if not chunk:
                    break             
                video = await bot.send_document(
                    chat_id=648340875, 
                    document=chunk, 
                    filename=f"1_{chunks_counter * CHUNK_SIZE}.mp4"
                )
                chunks_counter += 1
                if chunks_counter > 1:
                    break

            # video = await bot.send_document(chat_id=648340875, document=document)
            # print(video.document.file_id)
            # # print(video.video.file_id)
            # # print(video.video.file_size)
            # file_id = video.document.file_id
            # print(await bot.getFile(file_id=file_id))

            # file_info_url = f'https://api.telegram.org/bot{TOKEN}/getFile'
            # params = {'file_id': file_id}
            # response = requests.get(file_info_url, params=params)
            # file_path = response.json()['result']['file_path']
            # print(f"! {file_path}")
        file_id = "BAACAgIAAxkDAAMHZgnA936frDzWFL9_jnmNdSW9CgsAAqdDAAImrVBIy2kR53I78Y80BA"
        # print(await bot.getFile(file_id=file_id))
        file_path = f"https://api.telegram.org/file/bot{TOKEN}/videos/file_0.mp4"
        
        # TODO: HTTPX support stream?
        # response = requests.get(file_path)       
        # with open("test.mp4", "wb") as video_file:
        #     video_file.write(response.content)  

        # with requests.get(file_path, stream=True) as response:
        #     with open("test.mp4", 'wb') as file:
        #         for chunk in response.iter_content(chunk_size=1024):
        #             if chunk:
        #                 file.write(chunk)

        # response = requests.get(file_path, stream=True)       
        # for chunk in response.iter_content(chunk_size=1024):
        #     yield chunk    

if __name__ == '__main__':
    asyncio.run(main())