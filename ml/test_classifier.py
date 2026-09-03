import pandas as pd
import joblib
from pathlib import Path


# --------------------------------------------------
# 1. LOAD TRAINED MODEL
# --------------------------------------------------

model_path = Path(__file__).parent / "saved_models" / "signal_classifier.joblib"

model = joblib.load(model_path)

print("AI model loaded successfully!")


# --------------------------------------------------
# 2. CREATE A NEW SYNTHETIC SIGNAL
# --------------------------------------------------
# This represents a new signal arriving from our
# simulated RF environment.

new_signal = {
    "frequency_mhz": 2475.0,
    "power_db": -43.0,
    "bandwidth_mhz": 21.0,
    "pulse_width_ms": 0.6,
    "pulse_interval_ms": 4.2,
    "frequency_variation_mhz": 27.0,
    "duration_sec": 8.0,
    "spectral_entropy": 0.58
}


# Convert the signal into a DataFrame
signal_df = pd.DataFrame([new_signal])


# --------------------------------------------------
# 3. PREDICT SIGNAL CLASS
# --------------------------------------------------

prediction = model.predict(signal_df)[0]

# Get probability for every class
probabilities = model.predict_proba(signal_df)[0]

classes = model.classes_

confidence = max(probabilities) * 100


# --------------------------------------------------
# 4. DISPLAY RESULT
# --------------------------------------------------

print("\n========================================")
print(" AI SIGNAL CLASSIFICATION")
print("========================================")

print("\nIncoming signal:")

for feature, value in new_signal.items():
    print(f"{feature:30} : {value}")


print("\n----------------------------------------")
print(f"Predicted class : {prediction}")
print(f"Confidence      : {confidence:.2f}%")
print("----------------------------------------")


print("\nClass probabilities:")

for signal_class, probability in zip(classes, probabilities):
    print(f"{signal_class:12} : {probability * 100:.2f}%")