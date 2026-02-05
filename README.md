Build:
- docker build -t python-snake-web .

Run:
- docker run -it -p 6080:6080 python-snake-web

In another terminal, ngrok:
- ngrok http 5010 

This exposes a URL, <url> use that to run the game

Browser:
- http://localhost:5010/new_game
- <url>/new_game