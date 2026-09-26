import csv

results = [
    [
        "Light",
        80,
        40.7027,
        40.9010,
        -0.49,
        50.5096,
        50.7481,
        1.4750,
        1.5125,
        "Not measured"
    ],
    [
        "Moderate",
        160,
        46.0193,
        43.4024,
        5.69,
        57.0538,
        53.8483,
        1.8813,
        1.6187,
        "Not measured"
    ],
    [
        "Heavy",
        240,
        47.5694,
        44.2749,
        6.93,
        58.9743,
        54.9572,
        1.9500,
        1.5458,
        "240 / 240"
    ]
]

file_path = r"C:\FuzzyPSO\results\final_results.csv"

with open(file_path, "w", newline="") as file:

    writer = csv.writer(file)

    writer.writerow([
        "Traffic Level",
        "Vehicles",
        "Baseline Fitness",
        "PSO Fitness",
        "Fitness Improvement (%)",
        "Baseline Time Loss",
        "PSO Time Loss",
        "Baseline Stops",
        "PSO Stops",
        "Throughput"
    ])

    writer.writerows(results)

print("Final results saved successfully.")
print(file_path)