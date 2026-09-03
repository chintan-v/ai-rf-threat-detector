# --------------------------------------------------
# THREAT PRIORITY SCORER
# --------------------------------------------------
# This is a simulated decision-support score.
# It is NOT a real-world threat assessment system.
# --------------------------------------------------


def calculate_threat_score(signal, classification):
    """
    Calculate a simulated priority score from 0-100.

    Inputs:
        signal          -> simulated RF observation
        classification  -> AI classification result

    Returns:
        score and priority level
    """

    score = 0.0

    predicted_class = classification["predicted_class"]
    confidence = classification["confidence"]

    # --------------------------------------------------
    # 1. AI CLASSIFICATION CONTRIBUTION
    # --------------------------------------------------

    class_weights = {
        "STABLE": 10,
        "PULSED": 35,
        "AGILE": 50,
        "WIDEBAND": 40
    }

    score += class_weights.get(predicted_class, 0)


    # --------------------------------------------------
    # 2. AI CONFIDENCE CONTRIBUTION
    # --------------------------------------------------

    # Higher confidence slightly increases the score.
    confidence_score = confidence * 0.20

    score += confidence_score


    # --------------------------------------------------
    # 3. SIGNAL POWER CONTRIBUTION
    # --------------------------------------------------

    power = signal["power_db"]

    # Convert the simulated power range into a 0-20 score.
    # Stronger simulated signals contribute more to the priority score.
    # Expected power range: approximately -90 dB to -30 dB.
    power_score = max(
    0,
    min(20, ((power + 90) / 60) * 20)
    )

    score += power_score


    # --------------------------------------------------
    # 4. FREQUENCY VARIATION CONTRIBUTION
    # --------------------------------------------------

    variation = signal["frequency_variation_mhz"]

    variation_score = min(
        15,
        variation / 50 * 15
    )

    score += variation_score


    # --------------------------------------------------
    # 5. BANDWIDTH CONTRIBUTION
    # --------------------------------------------------

    bandwidth = signal["bandwidth_mhz"]

    bandwidth_score = min(
        10,
        bandwidth / 100 * 10
    )

    score += bandwidth_score


    # --------------------------------------------------
    # LIMIT SCORE TO 0-100
    # --------------------------------------------------

    score = max(0, min(100, score))

    score = round(score, 2)


    # --------------------------------------------------
    # PRIORITY LEVEL
    # --------------------------------------------------

    if score >= 75:
        priority = "HIGH"

    elif score >= 45:
        priority = "MEDIUM"

    else:
        priority = "LOW"


    return {
    "threat_score": score,
    "priority": priority,

    "score_breakdown": {
        "classification": class_weights.get(predicted_class, 0),
        "confidence": round(confidence_score, 2),
        "power": round(power_score, 2),
        "frequency_variation": round(variation_score, 2),
        "bandwidth": round(bandwidth_score, 2)
    }
}


# --------------------------------------------------
# TEST
# --------------------------------------------------

if __name__ == "__main__":

    test_signal = {
        "frequency_mhz": 2475.0,
        "power_db": -43.0,
        "bandwidth_mhz": 21.0,
        "pulse_width_ms": 0.6,
        "pulse_interval_ms": 4.2,
        "frequency_variation_mhz": 27.0,
        "duration_sec": 8.0,
        "spectral_entropy": 0.58
    }

    test_classification = {
        "predicted_class": "AGILE",
        "confidence": 99.0
    }

    result = calculate_threat_score(
        test_signal,
        test_classification
    )

    print("========================================")
    print(" SIMULATED THREAT PRIORITY")
    print("========================================")

    print(f"\nClassification : {test_classification['predicted_class']}")
    print(f"Confidence     : {test_classification['confidence']}%")
    print(f"Priority Score : {result['threat_score']}/100")
    print(f"Priority Level : {result['priority']}")