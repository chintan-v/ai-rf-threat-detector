import random


SIGNAL_CLASSES = [
    "STABLE",
    "PULSED",
    "AGILE",
    "WIDEBAND"
]


def generate_signal():
    """
    Generate one simulated RF signal.

    This is a software-only simulation. The generated
    values represent synthetic observations rather
    than measurements from real RF hardware.
    """

    signal_class = random.choice(SIGNAL_CLASSES)

    frequency = random.uniform(2400, 2500)

    # --------------------------------------------
    # Generate features based on signal class
    # --------------------------------------------

    if signal_class == "STABLE":

        power = random.gauss(-55, 6)
        bandwidth = max(2, min(15, random.gauss(8, 2)))
        pulse_width = 0.0
        pulse_interval = 0.0
        frequency_variation = abs(random.gauss(1.5, 0.8))
        duration = random.uniform(5, 20)
        spectral_entropy = max(
            0.05,
            min(0.5, random.gauss(0.25, 0.06))
        )

    elif signal_class == "PULSED":

        power = random.gauss(-45, 7)
        bandwidth = max(5, min(35, random.gauss(18, 5)))
        pulse_width = max(0.2, min(2.0, random.gauss(0.8, 0.25)))
        pulse_interval = max(1.5, min(10, random.gauss(5, 1.2)))
        frequency_variation = abs(random.gauss(4, 2))
        duration = random.uniform(4, 18)
        spectral_entropy = max(
            0.15,
            min(0.75, random.gauss(0.45, 0.08))
        )

    elif signal_class == "AGILE":

        power = random.gauss(-42, 7)
        bandwidth = max(5, min(40, random.gauss(20, 6)))
        pulse_width = max(0.1, min(2.0, random.gauss(0.6, 0.25)))
        pulse_interval = max(1, min(9, random.gauss(4, 1.5)))
        frequency_variation = max(
            8,
            min(50, random.gauss(25, 8))
        )
        duration = random.uniform(3, 15)
        spectral_entropy = max(
            0.2,
            min(0.9, random.gauss(0.55, 0.1))
        )

    else:  # WIDEBAND

        power = random.gauss(-48, 7)
        bandwidth = max(35, min(100, random.gauss(65, 15)))
        pulse_width = 0.0
        pulse_interval = 0.0
        frequency_variation = max(
            1,
            min(20, random.gauss(8, 4))
        )
        duration = random.uniform(2, 12)
        spectral_entropy = max(
            0.45,
            min(0.98, random.gauss(0.78, 0.08))
        )

    return {
        "frequency_mhz": round(frequency, 3),
        "power_db": round(power, 3),
        "bandwidth_mhz": round(bandwidth, 3),
        "pulse_width_ms": round(pulse_width, 3),
        "pulse_interval_ms": round(pulse_interval, 3),
        "frequency_variation_mhz": round(frequency_variation, 3),
        "duration_sec": round(duration, 3),
        "spectral_entropy": round(spectral_entropy, 3),

        # Used only to verify our simulator.
        # The AI itself will NOT receive this value.
        "simulated_class": signal_class
    }


if __name__ == "__main__":

    print("========================================")
    print(" SIMULATED RF ENVIRONMENT")
    print("========================================")

    for i in range(10):

        signal = generate_signal()

        print(f"\nSignal #{i + 1}")
        print("----------------------------------------")

        for key, value in signal.items():
            print(f"{key:30} : {value}")