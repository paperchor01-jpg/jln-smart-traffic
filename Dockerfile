FROM python:3.10-slim

# Install system dependencies, VNC server, Fluxbox window manager, and SUMO
RUN apt-get update && apt-get install -y \
    xvfb x11vnc fluxbox \
    sumo sumo-tools sumo-doc \
    wget net-tools \
    libgl1 libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Install noVNC for browser-based video streaming
RUN wget -qO- https://github.com/novnc/noVNC/archive/v1.3.0.tar.gz | tar xz -C /opt/ \
    && mv /opt/noVNC-1.3.0 /opt/novnc \
    && wget -qO- https://github.com/novnc/websockify/archive/v0.10.0.tar.gz | tar xz -C /opt/ \
    && mv /opt/websockify-0.10.0 /opt/novnc/utils/websockify

WORKDIR /app

# Copy and install Python requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application files
COPY . .
RUN chmod +x start.sh

# Define the environment variable so TraCI knows where SUMO is located
ENV SUMO_HOME=/usr/share/sumo

CMD ["./start.sh"]
