# Remove container if it exists
docker rm -f game-server

# Kill any existing ngrok processes
killall ngrok

# Start ngrok in the background to tunnel port 80
ngrok http 8080 > /dev/null &

# Build the Docker image
docker build -t python-snake-web .

# Run the Docker container
docker run -d -p 8080:80 --name game-server python-snake-web