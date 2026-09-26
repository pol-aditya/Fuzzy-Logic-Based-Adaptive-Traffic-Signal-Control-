import random

from sumo_fitness import evaluate_parameters


# ============================================================
# REPRODUCIBILITY
# ============================================================

random.seed(42)

RESULTS_FILE = r"C:\FuzzyPSO\results\pso_convergence.csv"


# ============================================================
# PSO SETTINGS
# ============================================================

PARTICLES = 10
ITERATIONS = 10

W = 0.7
C1 = 1.5
C2 = 1.5


# ============================================================
# ORIGINAL FUZZY PARAMETERS
# ============================================================

INITIAL_PARAMETERS = [
    # Queue
    0, 5,
    15, 5,
    30, 5,

    # Arrival
    0, 2,
    5, 2,
    10, 2
]


# ============================================================
# PARAMETER BOUNDS
# ============================================================

BOUNDS = [
    (0, 10),     # Queue Low center
    (1, 8),      # Queue Low spread

    (5, 25),     # Queue Medium center
    (1, 8),      # Queue Medium spread

    (20, 30),    # Queue High center
    (1, 8),      # Queue High spread

    (0, 3),      # Arrival Low center
    (0.5, 4),    # Arrival Low spread

    (2, 8),      # Arrival Medium center
    (0.5, 4),    # Arrival Medium spread

    (7, 10),     # Arrival High center
    (0.5, 4)     # Arrival High spread
]


# ============================================================
# KEEP MEMBERSHIP FUNCTIONS IN LOW -> MEDIUM -> HIGH ORDER
# ============================================================

def enforce_parameter_order(parameters):

    parameters = parameters.copy()

    # --------------------------------------------------------
    # Queue membership-function centers
    # --------------------------------------------------------

    queue_centers = [
        parameters[0],
        parameters[2],
        parameters[4]
    ]

    queue_centers.sort()

    parameters[0] = queue_centers[0]
    parameters[2] = queue_centers[1]
    parameters[4] = queue_centers[2]


    # --------------------------------------------------------
    # Arrival membership-function centers
    # --------------------------------------------------------

    arrival_centers = [
        parameters[6],
        parameters[8],
        parameters[10]
    ]

    arrival_centers.sort()

    parameters[6] = arrival_centers[0]
    parameters[8] = arrival_centers[1]
    parameters[10] = arrival_centers[2]

    return parameters


# ============================================================
# FITNESS FUNCTION
# ============================================================

def run_fitness(parameters):
    fitness, _, _, _, _, _, _ = evaluate_parameters(parameters)
    return fitness


# ============================================================
# CREATE INITIAL PARTICLES
# ============================================================

particles = []

print()
print("===================================")
print("CREATING INITIAL PSO POPULATION")
print("===================================")


for i in range(PARTICLES):

    print()
    print("Testing initial particle", i + 1)


    # --------------------------------------------------------
    # First particle = original fuzzy controller
    # --------------------------------------------------------

    if i == 0:

        position = INITIAL_PARAMETERS.copy()


    # --------------------------------------------------------
    # Other particles = random parameter sets
    # --------------------------------------------------------

    else:

        position = [
            random.uniform(
                BOUNDS[d][0],
                BOUNDS[d][1]
            )
            for d in range(len(BOUNDS))
        ]

        position = enforce_parameter_order(
            position
        )


    # --------------------------------------------------------
    # Initial velocity
    # --------------------------------------------------------

    velocity = [
        random.uniform(-1, 1)
        for _ in range(len(BOUNDS))
    ]


    print(
        "Parameters:",
        [
            round(x, 3)
            for x in position
        ]
    )


    # --------------------------------------------------------
    # Evaluate particle
    # --------------------------------------------------------

    fitness = run_fitness(
        position
    )


    particles.append({

        "position": position,

        "velocity": velocity,

        "best_position": position.copy(),

        "best_fitness": fitness

    })


# ============================================================
# FIND INITIAL GLOBAL BEST
# ============================================================

best_particle = min(
    particles,
    key=lambda p: p["best_fitness"]
)

global_best_position = (
    best_particle["best_position"].copy()
)

global_best_fitness = (
    best_particle["best_fitness"]
)


print()
print(
    "Initial global best fitness:",
    round(global_best_fitness, 4)
)


# ============================================================
# CREATE CONVERGENCE FILE
# ============================================================

with open(
    RESULTS_FILE,
    "w"
) as file:

    file.write(
        "iteration,best_fitness\n"
    )

    file.write(
        f"0,{global_best_fitness}\n"
    )


# ============================================================
# PSO OPTIMIZATION
# ============================================================

for iteration in range(ITERATIONS):

    print()
    print("===================================")
    print(
        "PSO ITERATION",
        iteration + 1
    )
    print("===================================")


    for particle_number, particle in enumerate(
        particles,
        start=1
    ):

        print()
        print(
            "Particle",
            particle_number
        )


        # ====================================================
        # UPDATE PARTICLE
        # ====================================================

        for d in range(len(BOUNDS)):

            r1 = random.random()
            r2 = random.random()


            # ------------------------------------------------
            # Cognitive component
            # ------------------------------------------------

            cognitive = (
                C1
                * r1
                * (
                    particle["best_position"][d]
                    - particle["position"][d]
                )
            )


            # ------------------------------------------------
            # Social component
            # ------------------------------------------------

            social = (
                C2
                * r2
                * (
                    global_best_position[d]
                    - particle["position"][d]
                )
            )


            # ------------------------------------------------
            # Update velocity
            # ------------------------------------------------

            particle["velocity"][d] = (

                W
                * particle["velocity"][d]

                + cognitive

                + social

            )


            # ------------------------------------------------
            # Update position
            # ------------------------------------------------

            particle["position"][d] += (
                particle["velocity"][d]
            )


            # ------------------------------------------------
            # Keep parameter inside allowed range
            # ------------------------------------------------

            particle["position"][d] = max(

                BOUNDS[d][0],

                min(
                    BOUNDS[d][1],
                    particle["position"][d]
                )

            )


        # ====================================================
        # ENFORCE LOW -> MEDIUM -> HIGH ORDER
        # ====================================================

        particle["position"] = (
            enforce_parameter_order(
                particle["position"]
            )
        )


        print(
            "Parameters:",
            [
                round(x, 3)
                for x in particle["position"]
            ]
        )


        # ====================================================
        # RUN SUMO
        # ====================================================

        current_fitness = run_fitness(
            particle["position"]
        )


        # ====================================================
        # UPDATE PERSONAL BEST
        # ====================================================

        if (
            current_fitness
            < particle["best_fitness"]
        ):

            particle["best_fitness"] = (
                current_fitness
            )

            particle["best_position"] = (
                particle["position"].copy()
            )

            print(
                "New personal best!"
            )


        # ====================================================
        # UPDATE GLOBAL BEST
        # ====================================================

        if (
            current_fitness
            < global_best_fitness
        ):

            global_best_fitness = (
                current_fitness
            )

            global_best_position = (
                particle["position"].copy()
            )

            print(
                ">>> NEW GLOBAL BEST <<<"
            )


    # ========================================================
    # ITERATION RESULT
    # ========================================================

    print()

    print(
        "Best fitness after iteration",
        iteration + 1,
        "=",
        round(
            global_best_fitness,
            4
        )
    )


    # ========================================================
    # SAVE CONVERGENCE RESULT
    # ========================================================

    with open(
        RESULTS_FILE,
        "a"
    ) as file:

        file.write(
            f"{iteration + 1},"
            f"{global_best_fitness}\n"
        )


# ============================================================
# FINAL RESULT
# ============================================================

print()
print("===================================")
print("FUZZY-PSO SUMO OPTIMIZATION DONE")
print("===================================")


print(
    "Best fitness:",
    round(
        global_best_fitness,
        4
    )
)


print(
    "Best parameters:"
)


print(
    [
        round(x, 4)
        for x in global_best_position
    ]
)


print()
print(
    "Convergence results saved to:"
)

print(
    RESULTS_FILE
)