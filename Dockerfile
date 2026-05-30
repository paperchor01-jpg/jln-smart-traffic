RUN apt-get update && apt-get install -y \
    xvfb x11vnc fluxbox \
    sumo sumo-tools sumo-doc \
    wget net-tools \
    libgl1 libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*
