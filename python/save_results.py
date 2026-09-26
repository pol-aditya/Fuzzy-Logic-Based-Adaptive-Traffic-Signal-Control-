import csv

results = [
    ["Light", 80, 40.7027, 40.9010, 50.5096, 50.7481, 1.4750, 1.5125, -0.49],
    ["Moderate", 160, 46.0193, 43.4024, 57.0538, 53.8483, 1.8813, 1.6187, 5.69],
    ["Heavy", 240, 47.5694, 46.9704, 58.9743, 58.2870, 1.9500, 1.7042, 1.26]
]

file_path = r"C:\FuzzyPSO\results\traffic_comparison.csv"

with open(file_path, "w", newline="") as file:
    writer = csv.writer(file)

    writer.writerow([
        "Traffic Level",
        "Vehicles",
        "Baseline Fitness",
        "PSO Fitness",
        "Baseline Time Loss",
        "PSO Time Loss",
        "Baseline Stops",
        "PSO Stops",
        "Fitness Change (%)"
    ])

    writer.writerows(results)

print("Results saved successfully.")
print(file_path)