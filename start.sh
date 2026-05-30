#!/bin/bash

# 1. Turn on the virtual framebuffer monitor
export DISPLAY=:99
Xvfb :99 -screen 0 1280x720x24 &
sleep 2

# 2. Start the light window manager
fluxbox &

# 3. Initialize the VNC streaming link
x11vnc -display :99 -forever -nopw -bg -xkb

# 4. Launch the integrated Python simulation script in the background
python simulation.py &

# 5. Serve the noVNC client to stream the visual display to the web browser
/opt/novnc/utils/websockify/run --web=/opt/novnc/ 8080 localhost:5900