#!/bin/bash

echo "1. Translating JLN Marg OSM data into SUMO network..."
# Converts the raw GPS map into a SUMO engineering map, automatically generating junctions and traffic signals
netconvert --osm-files map.osm -o osm.net.xml \
  --geometry.remove --roundabouts.guess --ramps.guess \
  --junctions.join --tls.guess-signals --tls.discard-simple --tls.join

echo "2. Generating high-density random traffic across the real map..."
# Injects a constant stream of vehicles into the real-world road network lanes
python $SUMO_HOME/tools/randomTrips.py -n osm.net.xml -r osm.rou.xml -e 3600 -p 1.5

echo "3. Starting virtual display server..."
export DISPLAY=:99
Xvfb :99 -screen 0 1280x720x24 &
sleep 2

fluxbox &
x11vnc -display :99 -forever -nopw -bg -xkb

echo "4. Launching Traffic AI engine..."
python simulation.py &

echo "5. Streaming to web browser via Hugging Face port..."
# Port changed to 7860 so Hugging Face can display the UI directly in your browser tab
/opt/novnc/utils/websockify/run --web=/opt/novnc/ 7860 localhost:5900
