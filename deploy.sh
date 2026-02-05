# Remove container if it exists
docker rm -f game-server

# Build the Docker image
docker build -t python-snake-web .

# Run the Docker container
docker run -d -p 5010:5010 -p 6081-6090:6081-6090 --name game-server python-snake-web