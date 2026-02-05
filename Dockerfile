FROM python:3.14
RUN apt-get update && apt-get install -y \
    python3-tk xvfb x11vnc novnc websockify procps net-tools nginx \
    && apt-get clean
    
RUN pip install flask

WORKDIR /app
COPY snake_game.py session_manager.py ./
COPY nginx.conf /etc/nginx/nginx.conf

# We need a range of ports for multiple sessions
EXPOSE 80

CMD nginx && python3 session_manager.py