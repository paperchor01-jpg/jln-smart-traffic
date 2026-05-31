import os
import sys
import traci

# TEMPORARILY DISABLED TO SAVE RAM ON FREE CLOUD TIER
# from ultralytics import YOLO
# print("Initializing computer vision model architecture...")
# vision_model = YOLO('yolov8n.pt') 

print("Locating SUMO configuration files...")
sumo_binary = "sumo-gui"
sumo_cmd = [sumo_binary, "-c", "osm.sumocfg"]

try:
    print("Connecting TraCI interface to SUMO core...")
    traci.start(sumo_cmd)
    
    traffic_lights = traci.trafficlight.getIDList()
    print(f"Active managed intersections detected: {traffic_lights}")
    
    step = 0
    while step < 3600:
        traci.simulationStep()
        
        # Every 10 steps, poll the intersections
        if step % 10 == 0:
            for tl_id in traffic_lights:
                # Basic vehicle counting via TraCI (bypassing heavy computer vision for now)
                controlled_lanes = traci.trafficlight.getControlledLanes(tl_id)
                vehicle_count = sum(traci.lane.getLastStepVehicleNumber(lane) for lane in set(controlled_lanes))
                
                if vehicle_count > 5:
                    current_phase = traci.trafficlight.getPhase(tl_id)
                    traci.trafficlight.setPhase(tl_id, current_phase)
                    
        step += 1
        
    traci.close()
    print("Simulation runtime executed to completion successfully.")
    
except Exception as error:
    print(f"SUMO RUNTIME EXCEPTION DETECTED: {error}")
    sys.exit(1)
