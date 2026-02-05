import subprocess
import time
import os
from flask import Flask, jsonify, redirect, request

app = Flask(__name__)

# Track active sessions: { session_id: port }
sessions = {}
base_vnc_port = 5900
base_web_port = 6081 # Start noVNC ports from 6081+
next_display = 1

@app.route('/new_game')
def create_session():
    global next_display
    
    display = f":{next_display}"
    vnc_port = base_vnc_port + next_display
    web_port = base_web_port + next_display
    
    # 1. Start Xvfb
    subprocess.Popen(["Xvfb", display, "-screen", "0", "1600x900x16"])
    
    # 2. Start the Game on that display
    env = os.environ.copy()
    env["DISPLAY"] = display
    subprocess.Popen(["python3", "snake_game.py"], env=env)
    
    # 3. Start x11vnc
    subprocess.Popen(["x11vnc", "-display", display, "-forever", "-shared", 
                      "-nopw", "-rfbport", str(vnc_port), "-bg"])
    
    # 4. Start Websockify (noVNC bridge)
    # This points the web_port to the specific VNC port
    subprocess.Popen([
        "websockify", "--web", "/usr/share/novnc/", 
        str(web_port), f"localhost:{vnc_port}"
    ])
    
    next_display += 1

    # host_name = request.host.split(':')[0]
    
    # Return the URL to the user
    # Note: Replace 'localhost' with your server IP if running remotely
    # return f"Game started! Access it at: http://{host_name}:{web_port}/vnc.html"
    # return redirect(f"http://{host_name}:{web_port}/vnc.html")

    # We don't change the port in the URL anymore, we change the PATH
    # The 'vnc.html?path=view/{web_port}/websockify' tells noVNC where to find the stream
    shareable_url = f"https://{request.host}/view/{web_port}/vnc.html"
    
    return redirect(shareable_url)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5010)