from collections import deque
from pathlib import Path

import joblib
import pandas as pd


# --------------------------------------------------
# LOAD TRAINED FREQUENCY PREDICTOR
# --------------------------------------------------

MODEL_PATH = (
    Path(__file__).resolve().parents[3]
    / "ml"
    / "saved_models"
    / "frequency_predictor.joblib"
)

model = joblib.load(MODEL_PATH)


# --------------------------------------------------
# RECENT FREQUENCY HISTORY
# --------------------------------------------------

frequency_history = deque(maxlen=4)


# --------------------------------------------------
# PREDICT NEXT FREQUENCY
# --------------------------------------------------

def predict_next_frequency(current_frequency):
    """
    Add the latest observed frequency to our simulated
    monitoring history and predict the next frequency.

    The model requires four recent observations.
    """

    frequency_history.append(current_frequency)

    # We need four observations before using the model.
    if len(frequency_history) < 4:

        return {
            "ready": False,
            "next_frequency_mhz": round(current_frequency, 3),
            "history_size": len(frequency_history),
            "message": "Collecting frequency history..."
        }

    # Convert the four most recent observations into
    # the feature structure used during training.

    recent = list(frequency_history)

    input_data = pd.DataFrame([{
        "frequency_lag_3": recent[0],
        "frequency_lag_2": recent[1],
        "frequency_lag_1": recent[2],
        "current_frequency_mhz": recent[3]
    }])

    prediction = model.predict(input_data)[0]

    return {
        "ready": True,
        "next_frequency_mhz": round(float(prediction), 3),
        "history_size": len(frequency_history),
        "message": "Next monitoring frequency predicted."
    }