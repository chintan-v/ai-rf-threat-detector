import pandas as pd
from pathlib import Path

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix
)
import joblib


# --------------------------------------------------
# 1. LOAD DATASET
# --------------------------------------------------

dataset_path = Path(__file__).parent / "data" / "rf_signals.csv"

df = pd.read_csv(dataset_path)

print("Dataset loaded successfully!")
print(f"Dataset shape: {df.shape}")


# --------------------------------------------------
# 2. SELECT FEATURES AND TARGET
# --------------------------------------------------

features = [
    "frequency_mhz",
    "power_db",
    "bandwidth_mhz",
    "pulse_width_ms",
    "pulse_interval_ms",
    "frequency_variation_mhz",
    "duration_sec",
    "spectral_entropy"
]

X = df[features]
y = df["class"]


# --------------------------------------------------
# 3. SPLIT INTO TRAINING AND TESTING DATA
# --------------------------------------------------

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)

print(f"\nTraining samples: {len(X_train)}")
print(f"Testing samples : {len(X_test)}")


# --------------------------------------------------
# 4. CREATE RANDOM FOREST MODEL
# --------------------------------------------------

model = RandomForestClassifier(
    n_estimators=200,
    random_state=42,
    n_jobs=-1
)


# --------------------------------------------------
# 5. TRAIN MODEL
# --------------------------------------------------

print("\nTraining Random Forest model...")

model.fit(X_train, y_train)

print("Training completed!")


# --------------------------------------------------
# 6. MAKE PREDICTIONS
# --------------------------------------------------

y_pred = model.predict(X_test)


# --------------------------------------------------
# 7. EVALUATE MODEL
# --------------------------------------------------

accuracy = accuracy_score(y_test, y_pred)

print("\n========================================")
print(" MODEL PERFORMANCE")
print("========================================")

print(f"\nAccuracy: {accuracy:.4f}")

print("\nClassification Report:")
print(classification_report(y_test, y_pred))

print("\nConfusion Matrix:")
print(confusion_matrix(y_test, y_pred))


# --------------------------------------------------
# 8. FEATURE IMPORTANCE
# --------------------------------------------------

print("\n========================================")
print(" FEATURE IMPORTANCE")
print("========================================")

importance = pd.Series(
    model.feature_importances_,
    index=features
).sort_values(ascending=False)

print(importance)


# --------------------------------------------------
# 9. SAVE MODEL
# --------------------------------------------------

model_directory = Path(__file__).parent / "saved_models"
model_directory.mkdir(exist_ok=True)

model_path = model_directory / "signal_classifier.joblib"

joblib.dump(model, model_path)

print("\n========================================")
print(" MODEL SAVED")
print("========================================")
print(f"Location: {model_path}")