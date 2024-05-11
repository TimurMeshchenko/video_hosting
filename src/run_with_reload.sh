#!/bin/bash

# Function to restart Gunicorn
restart_gunicorn() {
    echo "Restarting Gunicorn..."
    pkill -f uvicorn
    uvicorn main:app --port 8004 &
}

# Start Gunicorn
uvicorn main:app --port 8004 &

# Watch for changes in the project directory and restart Gunicorn when necessary
while inotifywait -r -e modify,move,create,delete /python/pet_projects/video_hosting; do 
    restart_gunicorn
done