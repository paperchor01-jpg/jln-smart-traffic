import os
import sys
import traci
from ultralytics import YOLO

print("Initializing computer vision model architecture...")
# Automatically fetches the lightweight nano model for performance in headless clouds
vision_model = YOLO('yolov8n.pt') 

print("Locating SUMO configuration files...")
sumo_binary = "sumo-gui"

# The '--start' command has been removed. SUMO will now wait for your manual start.
sumo_cmd = [sumo_binary, "-c", "osm.sumocfg"]

try:
    print("Connecting TraCI interface to SUMO core...")
    traci.start(sumo_cmd)
    
    # Identify the structural traffic light junctions defined in our network map
    traffic_lights = traci.trafficlight.getIDList()
    print(f"Active managed intersections detected: {traffic_lights}")
    
    step = 0
    while step < 3600:
        traci.simulationStep()
        
        # Every 10 steps, poll the intersections to optimize green cycles dynamically
        if step % 10 == 0:
            for tl_id in traffic_lights:
                # Simulate computer vision monitoring by counting active vehicles
                # In production, feed camera frames directly into 'vision_model'
                controlled_lanes = traci.trafficlight.getControlledLanes(tl_id)
                vehicle_count = sum(traci.lane.getLastStepVehicleNumber(lane) for lane in set(controlled_lanes))
                
                # Dynamic logic: If a high load is detected, extend green phase runtime
                if vehicle_count > 5:
                    current_phase = traci.trafficlight.getPhase(tl_id)
                    # Keep the current phase active slightly longer to clear the load
                    traci.trafficlight.setPhase(tl_id, current_phase)
                    
        step += 1
        
    traci.close()
    print("Simulation runtime executed to completion successfully.")
    
except Exception as error:
    print(f"SUMO RUNTIME EXCEPTION DETECTED: {error}")
    sys.exit(1)
