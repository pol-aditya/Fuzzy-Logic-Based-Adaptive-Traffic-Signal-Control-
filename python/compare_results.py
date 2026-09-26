from sumo_fitness import evaluate_parameters


# ==========================================
# BASELINE PARAMETERS
# ==========================================

baseline_parameters = [
    0, 5,
    15, 5,
    30, 5,
    0, 2,
    5, 2,
    10, 2
]


# ==========================================
# PSO PARAMETERS - HEAVY TRAFFIC
# ==========================================

pso_parameters = [
    9.8354, 2.9543,
    17.78, 8,
    22.3155, 7.6659,
    1.6186, 0.5,
    4.2632, 0.5,
    7.165, 4
]


# ==========================================
# BASELINE
# ==========================================

print("\n==============================")
print("BASELINE CONTROLLER")
print("==============================")

(
    baseline_fitness,
    baseline_delay,
    baseline_stops,
    baseline_throughput,
    baseline_mean_queue,
    baseline_max_queue,
    baseline_emergency_time
) = evaluate_parameters(baseline_parameters)


print("Fitness:", round(baseline_fitness, 4))
print("Mean time loss:", round(baseline_delay, 4))
print("Mean stops:", round(baseline_stops, 4))
print("Throughput:", baseline_throughput, "vehicles")
print("Mean queue:", round(baseline_mean_queue, 4), "vehicles")
print("Maximum queue:", baseline_max_queue, "vehicles")


# ==========================================
# PSO
# ==========================================

print("\n==============================")
print("PSO CONTROLLER")
print("==============================")

(
    pso_fitness,
    pso_delay,
    pso_stops,
    pso_throughput,
    pso_mean_queue,
    pso_max_queue,
    pso_emergency_time
) = evaluate_parameters(pso_parameters)


print("Fitness:", round(pso_fitness, 4))
print("Mean time loss:", round(pso_delay, 4))
print("Mean stops:", round(pso_stops, 4))
print("Throughput:", pso_throughput, "vehicles")
print("Mean queue:", round(pso_mean_queue, 4), "vehicles")
print("Maximum queue:", pso_max_queue, "vehicles")


# ==========================================
# COMPARISON
# ==========================================

print("\n==============================")
print("COMPARISON")
print("==============================")

fitness_change = baseline_fitness - pso_fitness
delay_change = baseline_delay - pso_delay
stops_change = baseline_stops - pso_stops
throughput_change = pso_throughput - baseline_throughput
mean_queue_change = baseline_mean_queue - pso_mean_queue
max_queue_change = baseline_max_queue - pso_max_queue


print(
    "Fitness difference:",
    round(fitness_change, 4)
)

print(
    "Time-loss difference:",
    round(delay_change, 4)
)

print(
    "Stops difference:",
    round(stops_change, 4)
)

print(
    "Throughput difference:",
    throughput_change,
    "vehicles"
)

print(
    "Mean queue difference:",
    round(mean_queue_change, 4),
    "vehicles"
)

print(
    "Maximum queue difference:",
    max_queue_change,
    "vehicles"
)


# ==========================================
# FITNESS PERCENTAGE
# ==========================================

if baseline_fitness != 0:

    fitness_percent = (
        fitness_change / baseline_fitness
    ) * 100

    print(
        "Fitness change (%):",
        round(fitness_percent, 2),
        "%"
    )