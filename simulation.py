import os
import sys
import traci
from ultralytics import YOLO

print("Initializing computer vision model architecture...")
# 16GB RAM allows us to easily load the PyTorch vision model
vision_model = YOLO('yolov8n.pt') 

print("Locating SUMO configuration files...")
sumo_binary = "sumo-gui"
sumo_cmd = [sumo_binary, "-c", "osm.sumocfg"]

try:
    print("Connecting TraCI interface to SUMO core...")
    traci.start(sumo_cmd)
    
    # Identify the traffic light junctions defined in the real map
    traffic_lights = traci.trafficlight.getIDList()
    print(f"Active managed intersections detected: {traffic_lights}")
    
    step = 0
    while step < 3600:
        traci.simulationStep()
        
        # Every 10 steps, poll the intersections to optimize green cycles dynamically
        if step % 10 == 0:
            for tl_id in traffic_lights:
                # Get lanes associated with this traffic light
                controlled_lanes = traci.trafficlight.getControlledLanes(tl_id)
                # Count total vehicles waiting at this intersection
                vehicle_count = sum(traci.lane.getLastStepVehicleNumber(lane) for lane in set(controlled_lanes))
                
                # Dynamic optimization logic:
                # If traffic load is high, extend the green phase to clear the queue
                if vehicle_count > 5:
                    current_phase = traci.trafficlight.getPhase(tl_id)
                    traci.trafficlight.setPhase(tl_id, current_phase)
                    
        step += 1
        
    traci.close()
    print("Simulation runtime executed to completion successfully.")
    
except Exception as error:
    print(f"SUMO RUNTIME EXCEPTION DETECTED: {error}")
    sys.exit(1)
