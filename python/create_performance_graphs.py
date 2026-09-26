import pandas as pd
import matplotlib.pyplot as plt

file_path = r"C:\FuzzyPSO\results\final_results.csv"

data = pd.read_csv(file_path)


# ==========================================
# TIME LOSS
# ==========================================

plt.figure(figsize=(8, 5))

plt.plot(
    data["Traffic Level"],
    data["Baseline Time Loss"],
    marker="o",
    label="Baseline"
)

plt.plot(
    data["Traffic Level"],
    data["PSO Time Loss"],
    marker="o",
    label="PSO"
)

plt.xlabel("Traffic Level")
plt.ylabel("Mean Time Loss (seconds/vehicle)")

plt.title("Baseline vs PSO Mean Time Loss")

plt.legend()
plt.grid(True)
plt.tight_layout()

plt.savefig(
    r"C:\FuzzyPSO\results\time_loss_comparison.png",
    dpi=300
)

plt.show()


# ==========================================
# STOPS
# ==========================================

plt.figure(figsize=(8, 5))

plt.plot(
    data["Traffic Level"],
    data["Baseline Stops"],
    marker="o",
    label="Baseline"
)

plt.plot(
    data["Traffic Level"],
    data["PSO Stops"],
    marker="o",
    label="PSO"
)

plt.xlabel("Traffic Level")
plt.ylabel("Mean Stops (stops/vehicle)")

plt.title("Baseline vs PSO Mean Stops")

plt.legend()
plt.grid(True)
plt.tight_layout()

plt.savefig(
    r"C:\FuzzyPSO\results\stops_comparison.png",
    dpi=300
)

plt.show()

print("Performance graphs saved successfully.")
print(r"C:\FuzzyPSO\results\time_loss_comparison.png")
print(r"C:\FuzzyPSO\results\stops_comparison.png")