import pandas as pd
import matplotlib.pyplot as plt

file_path = r"C:\FuzzyPSO\results\final_results.csv"

data = pd.read_csv(file_path)

plt.figure(figsize=(8, 5))

plt.plot(
    data["Traffic Level"],
    data["Baseline Fitness"],
    marker="o",
    label="Baseline"
)

plt.plot(
    data["Traffic Level"],
    data["PSO Fitness"],
    marker="o",
    label="PSO"
)

plt.xlabel("Traffic Level")
plt.ylabel("Fitness")

plt.title("Baseline vs PSO Fitness")

plt.legend()

plt.grid(True)

plt.tight_layout()

plt.savefig(
    r"C:\FuzzyPSO\results\fitness_comparison.png",
    dpi=300
)

plt.show()

print("Graph saved successfully.")
print(r"C:\FuzzyPSO\results\fitness_comparison.png")