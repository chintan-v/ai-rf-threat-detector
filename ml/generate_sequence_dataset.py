import numpy as np
import pandas as pd
from pathlib import Path


# --------------------------------------------------
# CONFIGURATION
# --------------------------------------------------

SEQUENCES = 100
STEPS_PER_SEQUENCE = 100

FREQUENCY_MIN = 2400
FREQUENCY_MAX = 2500

RANDOM_SEED = 42

rng = np.random.default_rng(RANDOM_SEED)


# --------------------------------------------------
# GENERATE ONE FREQUENCY SEQUENCE
# --------------------------------------------------

def generate_sequence():

    # Start at a random frequency
    current_frequency = rng.uniform(
        FREQUENCY_MIN,
        FREQUENCY_MAX
    )

    sequence = []

    for _ in range(STEPS_PER_SEQUENCE):

        # Simulate gradual movement in frequency.
        # This creates temporal structure for the
        # prediction model to learn.
        frequency_change = rng.normal(0, 2.5)

        current_frequency += frequency_change

        # Keep frequency inside our simulated range
        current_frequency = np.clip(
            current_frequency,
            FREQUENCY_MIN,
            FREQUENCY_MAX
        )

        sequence.append(current_frequency)

    return sequence


# --------------------------------------------------
# CREATE PREDICTION DATASET
# --------------------------------------------------

def generate_dataset():

    rows = []

    for sequence_id in range(SEQUENCES):

        sequence = generate_sequence()

        for time_step in range(len(sequence) - 1):

            current_frequency = sequence[time_step]

            next_frequency = sequence[time_step + 1]

            rows.append([
                sequence_id,
                time_step,
                current_frequency,
                next_frequency
            ])


    columns = [
        "sequence_id",
        "time_step",
        "current_frequency_mhz",
        "next_frequency_mhz"
    ]

    df = pd.DataFrame(
        rows,
        columns=columns
    )


    # --------------------------------------------------
    # SAVE DATASET
    # --------------------------------------------------

    output_directory = Path(__file__).parent / "data"

    output_directory.mkdir(
        exist_ok=True
    )

    output_path = (
        output_directory /
        "frequency_sequence.csv"
    )

    df.to_csv(
        output_path,
        index=False
    )


    # --------------------------------------------------
    # DISPLAY INFORMATION
    # --------------------------------------------------

    print("\n========================================")
    print(" FREQUENCY SEQUENCE DATASET")
    print("========================================")

    print(f"\nTotal samples : {len(df)}")
    print(f"Sequences     : {SEQUENCES}")
    print(f"Steps/sequence: {STEPS_PER_SEQUENCE}")

    print(f"\nOutput file:")
    print(output_path)

    print("\nFirst 10 samples:")
    print(df.head(10))


# --------------------------------------------------
# MAIN
# --------------------------------------------------

if __name__ == "__main__":
    generate_dataset()