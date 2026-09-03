from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.services.simulator import generate_signal
from app.services.classifier import classify_signal
from app.services.threat_scorer import calculate_threat_score
from app.services.alerts import generate_alert
from app.services.predictor import predict_next_frequency

app = FastAPI(
    title="AI RF Threat Detection System",
    description="Software-only simulated RF monitoring system",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
    "http://localhost:5173",
    "https://ai-rf-threat-detector.vercel.app",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {
        "status": "online",
        "message": "AI RF monitoring system is running"
    }


@app.get("/api/signal")
def get_signal():

    # 1. Generate simulated RF observation
    signal = generate_signal()

    # 2. Classify using trained AI
    classification = classify_signal(signal)

    # 3. Calculate simulated priority
    threat_result = calculate_threat_score(
        signal,
        classification
    )

    # 4. Generate alert
    alert = generate_alert(
        signal,
        classification,
        threat_result
    )

     # 5. Predict next monitoring frequency
    prediction = predict_next_frequency(
    signal["frequency_mhz"]
    )

    # 6. Return everything as JSON
    return {
        "signal": {
            "frequency_mhz": signal["frequency_mhz"],
            "power_db": signal["power_db"],
            "bandwidth_mhz": signal["bandwidth_mhz"],
            "pulse_width_ms": signal["pulse_width_ms"],
            "pulse_interval_ms": signal["pulse_interval_ms"],
            "frequency_variation_mhz": signal["frequency_variation_mhz"],
            "duration_sec": signal["duration_sec"],
            "spectral_entropy": signal["spectral_entropy"]
        },

        "classification": classification,

        "threat": threat_result,

        "alert": alert,

        "prediction": prediction
    }