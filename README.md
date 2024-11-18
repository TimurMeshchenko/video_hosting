# video_hosting

# Настройка mongodb

docker run --name mongo -v ./database_backups:/database_backups -d -p 27017:27017 mongo
docker exec -it mongo bash
mongosh 
use video_hosting
db.createCollection("videos")
exit
cd mongodb_backup
mongorestore --db=video_hosting .

# Запуск

poetry install
cd src
poetry run python -m uvicorn main:app --reload --port 8004
poetry run ./run_with_reload.sh


# mongosh комманды

db.videos.insertOne({
    "title": "minecraft",
    "image_path": "minecraft/minecraft.jpg",
    "file_path": "minecraft/minecraft.mp4",
})

db.videos.deleteOne({"title": "minecraft"})
