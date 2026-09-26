import traci

from fuzzy_parameterized import create_fuzzy_controller


# ============================================================
# SUMO SETTINGS
# ============================================================

NETWORK_FILE = r"C:\FuzzyPSO\sumo\intersection.net.xml"
ROUTE_FILE = r"C:\FuzzyPSO\sumo\traffic.rou.xml"

TLS_ID = "A0"

GREEN_PHASES = [0, 2]

INCOMING_EDGES = [
    "A1A0",
    "B0A0",
    "bottom0A0",
    "left0A0"
]


# ============================================================
# PARAMETER SETS
# ============================================================

BASELINE = [
    0, 5,
    15, 5,
    30, 5,
    0, 2,
    5, 2,
    10, 2
]


PSO_PARAMETERS = [
    4.6155, 4.6529,
    12.1053, 6.9995,
    21.9304, 6.5655,
    0.4197, 3.7562,
    7.7210, 1.3556,
    9.6414, 1.3673
]


# ============================================================
# RUN DIAGNOSTIC
# ============================================================

def run_diagnostic(parameters, name):

    print()
    print("======================================")
    print(name)
    print("======================================")

    controller = create_fuzzy_controller(
        parameters
    )

    sumo_cmd = [
        "sumo",
        "-n", NETWORK_FILE,
        "-r", ROUTE_FILE,
        "--no-step-log",
        "true",
	"--seed",
    	"42"
    ]

    traci.start(sumo_cmd)

    previous_phase = -1
    decision_count = 0

    try:

        while (
            traci.simulation.getMinExpectedNumber()
            > 0
        ):

            traci.simulationStep()

            current_phase = (
                traci.trafficlight.getPhase(
                    TLS_ID
                )
            )

            # Only inspect when a new phase begins
            if current_phase != previous_phase:

                previous_phase = current_phase

                if current_phase in GREEN_PHASES:

                    # ========================================
                    # QUEUE
                    # ========================================

                    queue_length = 0

                    for edge_id in INCOMING_EDGES:

                        lane_count = (
                            traci.edge.getLaneNumber(
                                edge_id
                            )
                        )

                        for lane_index in range(
                            lane_count
                        ):

                            lane_id = (
                                f"{edge_id}_{lane_index}"
                            )

                            vehicle_ids = (
                                traci.lane
                                .getLastStepVehicleIDs(
                                    lane_id
                                )
                            )

                            for vehicle_id in vehicle_ids:

                                speed = (
                                    traci.vehicle
                                    .getSpeed(
                                        vehicle_id
                                    )
                                )

                                if speed < 0.1:

                                    queue_length += 1


                    # ========================================
                    # ARRIVAL RATE
                    # ========================================

                    arrival_rate = (
                        traci.simulation
                        .getDepartedNumber()
                    )


                    # ========================================
                    # FUZZY DECISION
                    # ========================================

                    controller.input[
                        "queue"
                    ] = queue_length

                    controller.input[
                        "arrival"
                    ] = arrival_rate

                    controller.compute()

                    green_change = (
                        controller.output[
                            "green_change"
                        ]
                    )


                    new_duration = (
                        42 + green_change
                    )

                    new_duration = max(
                        20,
                        min(
                            60,
                            new_duration
                        )
                    )


                    decision_count += 1

                    print(
                        f"Decision {decision_count}: "
                        f"Phase={current_phase}, "
                        f"Queue={queue_length}, "
                        f"Arrival={arrival_rate}, "
                        f"Green change={green_change:.2f}, "
                        f"New green={new_duration:.2f}s"
                    )

                    traci.trafficlight.setPhaseDuration(
                        TLS_ID,
                        new_duration
                    )


    finally:

        traci.close()


# ============================================================
# RUN BOTH
# ============================================================

run_diagnostic(
    BASELINE,
    "BASELINE PARAMETERS"
)

run_diagnostic(
    PSO_PARAMETERS,
    "PSO PARAMETERS"
)