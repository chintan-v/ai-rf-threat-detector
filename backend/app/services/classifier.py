import pandas as pd
import joblib
from pathlib import Path


# --------------------------------------------------
# LOAD TRAINED MODEL
# --------------------------------------------------

MODEL_PATH = (
    Path(__file__).resolve().parents[3]
    / "ml"
    / "saved_models"
    / "signal_classifier.joblib"
)

model = joblib.load(MODEL_PATH)


# --------------------------------------------------
# FEATURES EXPECTED BY THE MODEL
# --------------------------------------------------

FEATURES = [
    "frequency_mhz",
    "power_db",
    "bandwidth_mhz",
    "pulse_width_ms",
    "pulse_interval_ms",
    "frequency_variation_mhz",
    "duration_sec",
    "spectral_entropy"
]


# --------------------------------------------------
# CLASSIFY SIGNAL
# --------------------------------------------------

def classify_signal(signal):
    """
    Take a simulated RF observation and return
    the AI classification and confidence.
    """

    # IMPORTANT:
    # simulated_class is deliberately NOT passed
    # to the AI.

    signal_features = {
        feature: signal[feature]
        for feature in FEATURES
    }

    signal_df = pd.DataFrame([signal_features])

    # Prediction
    prediction = model.predict(signal_df)[0]

    # Probabilities
    probabilities = model.predict_proba(signal_df)[0]

    classes = model.classes_

    confidence = max(probabilities) * 100

    probability_dict = {
        signal_class: round(probability * 100, 2)
        for signal_class, probability
        in zip(classes, probabilities)
    }

    return {
        "predicted_class": prediction,
        "confidence": round(confidence, 2),
        "probabilities": probability_dict
    }