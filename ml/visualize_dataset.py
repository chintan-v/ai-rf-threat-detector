import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path


# --------------------------------------------------
# Load dataset
# --------------------------------------------------

dataset_path = Path(__file__).parent / "data" / "rf_signals.csv"

df = pd.read_csv(dataset_path)

print("Dataset loaded successfully!")
print(f"Shape: {df.shape}")

print("\nClass distribution:")
print(df["class"].value_counts())


# --------------------------------------------------
# Plot 1
# Bandwidth vs Frequency Variation
# --------------------------------------------------

plt.figure(figsize=(10, 6))

for signal_class in df["class"].unique():

    subset = df[df["class"] == signal_class]

    plt.scatter(
        subset["bandwidth_mhz"],
        subset["frequency_variation_mhz"],
        label=signal_class,
        alpha=0.5
    )

plt.xlabel("Bandwidth (MHz)")
plt.ylabel("Frequency Variation (MHz)")
plt.title("RF Signal Classes: Bandwidth vs Frequency Variation")
plt.legend()
plt.grid(True)

plt.show()


# --------------------------------------------------
# Plot 2
# Power vs Spectral Entropy
# --------------------------------------------------

plt.figure(figsize=(10, 6))

for signal_class in df["class"].unique():

    subset = df[df["class"] == signal_class]

    plt.scatter(
        subset["power_db"],
        subset["spectral_entropy"],
        label=signal_class,
        alpha=0.5
    )

plt.xlabel("Power (dB)")
plt.ylabel("Spectral Entropy")
plt.title("RF Signal Classes: Power vs Spectral Entropy")
plt.legend()
plt.grid(True)

plt.show()