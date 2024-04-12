# video_hosting

# создание бд

mongosh 
use video_hosting
db.createCollection("videos")

cd mongodb_backup
mongorestore --db=video_hosting .

# Запуск

poetry run python -m uvicorn main:app --reload
sudo poetry run ./reload.sh


# mongosh комманды

db.videos.insertOne({
    "title": "minecraft",
    "image_path": "minecraft/minecraft.jpg",
    "file_path": "minecraft/minecraft.mp4",
})

db.videos.deleteOne({"title": "minecraft"})
