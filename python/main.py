import traci
import time

sumo_cmd = [
    "sumo-gui",
    "-n", r"C:\FuzzyPSO\sumo\intersection.net.xml",
    "-r", r"C:\FuzzyPSO\sumo\traffic.rou.xml",
    "--start"
]

traci.start(sumo_cmd)

print("CONNECTED TO SUMO!", flush=True)

for step in range(100):

    traci.simulationStep()

    vehicles = traci.vehicle.getIDList()

    # Queue length
    waiting_vehicles = 0

    for vehicle_id in vehicles:
        speed = traci.vehicle.getSpeed(vehicle_id)

        if speed < 0.1:
            waiting_vehicles += 1

    # Vehicles entering during THIS step
    arrival_rate = traci.simulation.getDepartedNumber()

    if step % 10 == 0:
        print(
            "Step:", step,
            "| Queue:", waiting_vehicles,
            "| Arrival Rate:", arrival_rate,
            flush=True
        )

    time.sleep(0.1)

traci.close()

print("DONE!", flush=True)