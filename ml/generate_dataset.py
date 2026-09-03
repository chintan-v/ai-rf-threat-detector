import numpy as np
import pandas as pd
from pathlib import Path


# --------------------------------------------------
# Configuration
# --------------------------------------------------

SAMPLES_PER_CLASS = 1000

FREQUENCY_MIN = 2400
FREQUENCY_MAX = 2500

RANDOM_SEED = 42

rng = np.random.default_rng(RANDOM_SEED)


# --------------------------------------------------
# Signal generators
# --------------------------------------------------

def generate_stable():
    """Generate a stable, relatively narrowband signal."""

    frequency = rng.uniform(FREQUENCY_MIN, FREQUENCY_MAX)

    power = rng.normal(-55, 6)

    bandwidth = np.clip(
        rng.normal(8, 2),
        2,
        15
    )

    pulse_width = 0.0

    pulse_interval = 0.0

    frequency_variation = abs(
        rng.normal(1.5, 0.8)
    )

    duration = rng.uniform(5, 20)

    spectral_entropy = np.clip(
        rng.normal(0.25, 0.06),
        0.05,
        0.5
    )

    return [
        frequency,
        power,
        bandwidth,
        pulse_width,
        pulse_interval,
        frequency_variation,
        duration,
        spectral_entropy,
        "STABLE"
    ]


def generate_pulsed():
    """Generate a periodic pulsed signal."""

    frequency = rng.uniform(FREQUENCY_MIN, FREQUENCY_MAX)

    power = rng.normal(-45, 7)

    bandwidth = np.clip(
        rng.normal(18, 5),
        5,
        35
    )

    pulse_width = np.clip(
        rng.normal(0.8, 0.25),
        0.2,
        2.0
    )

    pulse_interval = np.clip(
        rng.normal(5, 1.2),
        1.5,
        10
    )

    frequency_variation = abs(
        rng.normal(4, 2)
    )

    duration = rng.uniform(4, 18)

    spectral_entropy = np.clip(
        rng.normal(0.45, 0.08),
        0.15,
        0.75
    )

    return [
        frequency,
        power,
        bandwidth,
        pulse_width,
        pulse_interval,
        frequency_variation,
        duration,
        spectral_entropy,
        "PULSED"
    ]


def generate_agile():
    """Generate a frequency-varying signal."""

    frequency = rng.uniform(FREQUENCY_MIN, FREQUENCY_MAX)

    power = rng.normal(-42, 7)

    bandwidth = np.clip(
        rng.normal(20, 6),
        5,
        40
    )

    pulse_width = np.clip(
        rng.normal(0.6, 0.25),
        0.1,
        2.0
    )

    pulse_interval = np.clip(
        rng.normal(4, 1.5),
        1,
        9
    )

    frequency_variation = np.clip(
        rng.normal(25, 8),
        8,
        50
    )

    duration = rng.uniform(3, 15)

    spectral_entropy = np.clip(
        rng.normal(0.55, 0.1),
        0.2,
        0.9
    )

    return [
        frequency,
        power,
        bandwidth,
        pulse_width,
        pulse_interval,
        frequency_variation,
        duration,
        spectral_entropy,
        "AGILE"
    ]


def generate_wideband():
    """Generate a broad, noise-like signal."""

    frequency = rng.uniform(FREQUENCY_MIN, FREQUENCY_MAX)

    power = rng.normal(-48, 7)

    bandwidth = np.clip(
        rng.normal(65, 15),
        35,
        100
    )

    pulse_width = 0.0

    pulse_interval = 0.0

    frequency_variation = np.clip(
        rng.normal(8, 4),
        1,
        20
    )

    duration = rng.uniform(2, 12)

    spectral_entropy = np.clip(
        rng.normal(0.78, 0.08),
        0.45,
        0.98
    )

    return [
        frequency,
        power,
        bandwidth,
        pulse_width,
        pulse_interval,
        frequency_variation,
        duration,
        spectral_entropy,
        "WIDEBAND"
    ]


# --------------------------------------------------
# Generate dataset
# --------------------------------------------------

def generate_dataset():

    rows = []

    generators = [
        generate_stable,
        generate_pulsed,
        generate_agile,
        generate_wideband
    ]

    for generator in generators:

        for _ in range(SAMPLES_PER_CLASS):

            rows.append(generator())

    columns = [
        "frequency_mhz",
        "power_db",
        "bandwidth_mhz",
        "pulse_width_ms",
        "pulse_interval_ms",
        "frequency_variation_mhz",
        "duration_sec",
        "spectral_entropy",
        "class"
    ]

    df = pd.DataFrame(
        rows,
        columns=columns
    )

    # Shuffle the dataset
    df = df.sample(
        frac=1,
        random_state=RANDOM_SEED
    ).reset_index(drop=True)

    # Create output directory
    output_directory = Path(__file__).parent / "data"
    output_directory.mkdir(
        exist_ok=True
    )

    output_path = (
        output_directory /
        "rf_signals.csv"
    )

    df.to_csv(
        output_path,
        index=False
    )

    print("\nDataset generated successfully!")
    print("--------------------------------")
    print(f"Total samples: {len(df)}")
    print(f"Features: {len(columns) - 1}")
    print(f"Output: {output_path}")

    print("\nClass distribution:")
    print(df["class"].value_counts())

    print("\nFirst 5 samples:")
    print(df.head())


# --------------------------------------------------
# Entry point
# --------------------------------------------------

if __name__ == "__main__":
    generate_dataset()