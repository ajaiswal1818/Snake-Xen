# Snake-Xen

A multiplayer Snake game that runs in Docker with VNC and Flask backend, allowing multiple players to connect and play simultaneously.

## How It Works

Snake-Xen uses a session-based architecture:
- **Flask Backend**: Manages game sessions and serves the web interface
- **VNC Server**: Provides graphical access to individual game instances
- **Docker Container**: Isolates the environment with all dependencies
- **ngrok**: Exposes your local container to the internet (optional)

Each player connecting to the web interface gets their own virtual display and game instance running on a unique port.

## Build

```bash
docker build -t python-snake-web .
```

## Run Locally

```bash
docker run -it -p 5010:5010 -p 6080-6100:6080-6100 python-snake-web
```

This exposes:
- **Port 5010**: Flask web server
- **Ports 6080-6100**: VNC ports for individual game sessions

## Play

### Local Gaming
1. Open your browser and navigate to:
   ```
   http://localhost:5010/new_game
   ```
2. A new game session will be created and you'll be directed to the noVNC viewer
3. Use arrow keys or WASD to control the snake
4. Press ESC to exit the game

### Remote Gaming (with ngrok)

In another terminal, expose your container:

```bash
ngrok http 5010
```

This generates a public URL. Use:
```
<ngrok-url>/new_game
```

Share this URL with others to let them play!

## Controls

- **Arrow Keys** or **WASD**: Move the snake
- **R Key**: Restart game
- **ESC**: Exit game

## Features

- Multiple simultaneous game sessions
- Browser-based VNC viewer (noVNC)
- Isolated game instances per player
- Easy remote access with ngrok