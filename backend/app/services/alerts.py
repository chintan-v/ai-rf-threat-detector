# --------------------------------------------------
# ALERT GENERATOR
# --------------------------------------------------
# This generates alerts from our simulated priority
# score. It is a software-only decision-support demo.
# --------------------------------------------------


ALERT_THRESHOLD = 75


def generate_alert(signal, classification, threat_result):
    """
    Generate an alert when the simulated priority
    score crosses the configured threshold.
    """

    score = threat_result["threat_score"]
    priority = threat_result["priority"]

    if score >= ALERT_THRESHOLD:

        return {
            "alert": True,
            "severity": priority,
            "message": "High-priority simulated RF observation detected.",
            "frequency_mhz": signal["frequency_mhz"],
            "classification": classification["predicted_class"],
            "confidence": classification["confidence"],
            "threat_score": score
        }

    return {
        "alert": False,
        "severity": priority,
        "message": "No high-priority alert.",
        "frequency_mhz": signal["frequency_mhz"],
        "classification": classification["predicted_class"],
        "confidence": classification["confidence"],
        "threat_score": score
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

    test_threat_result = {
        "threat_score": 80.0,
        "priority": "HIGH"
    }

    result = generate_alert(
        test_signal,
        test_classification,
        test_threat_result
    )

    print("========================================")
    print(" ALERT ENGINE TEST")
    print("========================================")

    print(f"\nAlert          : {result['alert']}")
    print(f"Severity       : {result['severity']}")
    print(f"Message        : {result['message']}")
    print(f"Frequency      : {result['frequency_mhz']} MHz")
    print(f"Classification : {result['classification']}")
    print(f"Confidence     : {result['confidence']}%")
    print(f"Threat Score   : {result['threat_score']}/100")