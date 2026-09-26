import traci


# ============================================================
# SUMO FITNESS MEASUREMENT
# ============================================================

sumo_cmd = [
    "sumo",
    "-n", r"C:\FuzzyPSO\sumo\intersection.net.xml",
    "-r", r"C:\FuzzyPSO\sumo\traffic.rou.xml",
    "--start"
]

print("Starting SUMO...", flush=True)

traci.start(sumo_cmd)

print("SUMO connected!", flush=True)


# ============================================================
# VARIABLES
# ============================================================

total_delay = 0.0
total_stops = 0
completed_vehicles = 0

previous_time_loss = {}
was_moving = {}


# ============================================================
# RUN SIMULATION
# ============================================================

while traci.simulation.getMinExpectedNumber() > 0:

    traci.simulationStep()

    # Count vehicles that arrived during THIS step
    arrived_this_step = traci.simulation.getArrivedNumber()

    completed_vehicles += arrived_this_step

    vehicle_ids = traci.vehicle.getIDList()

    for vehicle_id in vehicle_ids:

        # ----------------------------------------------------
        # Time loss
        # ----------------------------------------------------

        current_time_loss = traci.vehicle.getTimeLoss(
            vehicle_id
        )

        previous_loss = previous_time_loss.get(
            vehicle_id,
            0.0
        )

        # Only add the NEW time loss since the last step
        additional_loss = (
            current_time_loss - previous_loss
        )

        total_delay += max(0.0, additional_loss)

        previous_time_loss[vehicle_id] = current_time_loss


        # ----------------------------------------------------
        # Stops
        # ----------------------------------------------------

        speed = traci.vehicle.getSpeed(
            vehicle_id
        )

        moving_now = speed > 0.1

        if vehicle_id not in was_moving:

            was_moving[vehicle_id] = moving_now

        else:

            if (
                was_moving[vehicle_id]
                and not moving_now
            ):
                total_stops += 1

            was_moving[vehicle_id] = moving_now


# ============================================================
# CLOSE SUMO
# ============================================================

traci.close()


# ============================================================
# CALCULATE AVERAGES
# ============================================================

if completed_vehicles > 0:

    mean_delay = (
        total_delay / completed_vehicles
    )

    mean_stops = (
        total_stops / completed_vehicles
    )

else:

    mean_delay = 0.0
    mean_stops = 0.0


# ============================================================
# RESULTS
# ============================================================

print()
print("==============================")
print("SUMO FITNESS MEASUREMENT")
print("==============================")

print(
    "Completed vehicles:",
    completed_vehicles
)

print(
    "Mean time loss:",
    round(mean_delay, 2),
    "seconds/vehicle"
)

print(
    "Mean stops:",
    round(mean_stops, 2),
    "stops/vehicle"
)

print("==============================")