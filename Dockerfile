FROM python:3.14
RUN apt-get update && apt-get install -y \
    python3-tk xvfb x11vnc novnc websockify procps net-tools \
    && apt-get clean
    
RUN pip install flask

WORKDIR /app
COPY snake_game.py session_manager.py ./

# We need a range of ports for multiple sessions
EXPOSE 5010 6080-6100

CMD ["python3", "session_manager.py"]