from simulator import generate_signal
from classifier import classify_signal
from threat_scorer import calculate_threat_score
from alerts import generate_alert


print("========================================")
print(" LIVE SIMULATED RF MONITOR")
print("========================================")


for i in range(10):

    # 1. Generate a new simulated observation
    signal = generate_signal()

    # 2. AI classification
    classification = classify_signal(signal)

    # 3. Priority scoring
    threat_result = calculate_threat_score(
        signal,
        classification
    )

    # 4. Alert generation
    alert = generate_alert(
        signal,
        classification,
        threat_result
    )

    # 5. Display complete result
    print(f"\n[{i + 1:02}] "
          f"{signal['frequency_mhz']:.3f} MHz | "
          f"{classification['predicted_class']:<8} | "
          f"{classification['confidence']:>6.2f}% | "
          f"{threat_result['threat_score']:>5.1f}/100 | "
          f"{threat_result['priority']}")

    if alert["alert"]:
        print("     ⚠ ALERT: High-priority simulated observation detected.")


print("\n========================================")
print(" MONITORING TEST COMPLETE")
print("========================================")