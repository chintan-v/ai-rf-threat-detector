import pandas as pd
import joblib

from pathlib import Path


# --------------------------------------------------
# 1. LOAD MODEL
# --------------------------------------------------

model_path = (
    Path(__file__).parent
    / "saved_models"
    / "frequency_predictor.joblib"
)

model = joblib.load(model_path)

print("Frequency prediction model loaded successfully!")


# --------------------------------------------------
# 2. CREATE RECENT FREQUENCY HISTORY
# --------------------------------------------------

recent_frequencies = {
    "frequency_lag_3": 2465.0,
    "frequency_lag_2": 2467.5,
    "frequency_lag_1": 2469.2,
    "current_frequency_mhz": 2471.0
}


# --------------------------------------------------
# 3. PREPARE INPUT
# --------------------------------------------------

features = [
    "frequency_lag_3",
    "frequency_lag_2",
    "frequency_lag_1",
    "current_frequency_mhz"
]

input_data = pd.DataFrame(
    [recent_frequencies],
    columns=features
)


# --------------------------------------------------
# 4. PREDICT NEXT FREQUENCY
# --------------------------------------------------

prediction = model.predict(input_data)[0]


# --------------------------------------------------
# 5. DISPLAY RESULT
# --------------------------------------------------

print("\n========================================")
print(" ADAPTIVE SCAN PREDICTION")
print("========================================")

print("\nRecent observations:")

print(f"t-3 : {recent_frequencies['frequency_lag_3']:.2f} MHz")
print(f"t-2 : {recent_frequencies['frequency_lag_2']:.2f} MHz")
print(f"t-1 : {recent_frequencies['frequency_lag_1']:.2f} MHz")
print(f"t   : {recent_frequencies['current_frequency_mhz']:.2f} MHz")

print("\n----------------------------------------")

print(
    f"Recommended next monitoring frequency: "
    f"{prediction:.2f} MHz"
)

print("----------------------------------------")