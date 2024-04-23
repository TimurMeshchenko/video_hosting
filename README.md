# video_hosting

# Настройка mongodb

mongosh 
use video_hosting
db.createCollection("videos")

cd mongodb_backup
mongorestore --db=video_hosting .

# Запуск

sudo poetry install
cd src
sudo poetry run python -m uvicorn main:app --reload --port 8004
sudo poetry run ./run_with_reload.sh


# mongosh комманды

db.videos.insertOne({
    "title": "minecraft",
    "image_path": "minecraft/minecraft.jpg",
    "file_path": "minecraft/minecraft.mp4",
})

db.videos.deleteOne({"title": "minecraft"})
