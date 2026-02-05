# Snake-Xen

A multiplayer Snake game that runs in Docker with VNC and Flask backend, allowing multiple players to connect and play simultaneously.

## How It Works

Snake-Xen uses a session-based architecture:
- **Flask Backend**: Manages game sessions and serves the web interface
- **VNC Server**: Provides graphical access to individual game instances
- **Docker Container**: Isolates the environment with all dependencies
- **Nginx**: Reverse proxy that routes traffic and manages multiple VNC connections
- **ngrok**: Exposes your local container to the internet (optional)

Each player connecting to the web interface gets their own virtual display and game instance running on a unique port. Nginx handles routing requests to the appropriate VNC websocket bridge.

## Build & Run

### Quick Start with deploy.sh

The easiest way to get started is using the provided deploy script:

```bash
chmod +x deploy.sh
./deploy.sh
```

This will:
1. Remove any existing containers
2. Build the Docker image
3. Start the container with all necessary port mappings
4. Automatically start ngrok for remote access

### Manual Build

```bash
docker build -t python-snake-web .
```

### Manual Run

```bash
docker run -d -p 8080:80 --name game-server python-snake-web
```

### Run NGROK
```
ngrok http 8080
```

This exposes:
- **Port 5000**: Flask web server
- **Ports 6081-6090**: VNC ports for individual game sessions (up to 10 concurrent players)

## Play

### Local Gaming (Not supported at the moment)

1. Open your browser and navigate to:
   ```
   http://localhost:5000/new_game
   ```
2. A new game session will be created and you'll be directed to the noVNC viewer
3. Use arrow keys or WASD to control the snake
4. Press ESC to exit the game

### Remote Gaming (with ngrok)

If using `deploy.sh`, ngrok is automatically started. Check the terminal output for the public URL:

```
ngrok → <public-url>
```

Access the game at:
```
<public-url>/new_game
```

Share this URL with others to let them play!

## Controls

- **Arrow Keys** or **WASD**: Move the snake
- **R Key**: Restart game
- **ESC**: Exit game

## Features

- Multiple simultaneous game sessions (up to 10 players)
- Browser-based VNC viewer (noVNC)
- Isolated game instances per player
- Nginx reverse proxy for routing
- Easy remote access with ngrok
- Docker containerization for portability

## Project Structure

```
Snake-Xen/
├── snake_game.py          # Main Snake game (Tkinter-based)
├── session_manager.py     # Flask app for managing game sessions
├── nginx.conf             # Nginx configuration for routing
├── Dockerfile             # Docker image definition
├── deploy.sh              # Automated deployment script
├── README.md              # This file
└── LICENSE                # MIT License
```

## Architecture

- **Session Manager**: Listens on port 5000 and handles `/new_game` requests
- **Per-Session Setup**: Each new game spawns:
  - Xvfb (virtual display)
  - Snake game instance
  - x11vnc server on unique port
  - Websockify bridge for VNC-to-WebSocket conversion
- **Nginx**: Routes incoming connections to the appropriate VNC port

## Stop the Container

```bash
docker stop game-server
docker rm game-server
```

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

Original Snake game code adapted from [RileyFranco/Python-Snake-Game](https://github.com/RileyFranco/Python-Snake-Game).