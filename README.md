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

Прод:
poetry run python -m uvicorn main:app --port 8004

# mongosh комманды

db.videos.insertOne({
    "title": "minecraft",
    "image_path": "minecraft/minecraft.jpg",
    "file_path": "minecraft/minecraft.mp4",
})

db.videos.deleteOne({"title": "minecraft"})

# Webpack optimization

Убрать .git и media, чтобы запустить

docker build -f Dockerfile.webpack -t video_hosting_webpack .
docker run --name video_hosting_webpack_container -p 8080:8080 -v ./optimized:/app/optimized -v ./webpack.config.js:/app/webpack.config.js -d video_hosting_webpack
sudo docker exec -it video_hosting_webpack_container bash

npx webpack

sudo docker stop video_hosting_webpack_container
sudo docker rm video_hosting_webpack_container
sudo docker rmi video_hosting_webpack