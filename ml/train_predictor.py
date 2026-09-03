import pandas as pd
import joblib

from pathlib import Path
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error
from sklearn.model_selection import train_test_split


# --------------------------------------------------
# 1. LOAD DATASET
# --------------------------------------------------

dataset_path = (
    Path(__file__).parent
    / "data"
    / "frequency_sequence.csv"
)

df = pd.read_csv(dataset_path)

print("Frequency sequence dataset loaded!")
print(f"Dataset shape: {df.shape}")


# --------------------------------------------------
# 2. CREATE HISTORY FEATURES
# --------------------------------------------------

# We use the current frequency plus the previous
# three observations to predict the next frequency.

df["frequency_lag_1"] = (
    df.groupby("sequence_id")["current_frequency_mhz"]
    .shift(1)
)

df["frequency_lag_2"] = (
    df.groupby("sequence_id")["current_frequency_mhz"]
    .shift(2)
)

df["frequency_lag_3"] = (
    df.groupby("sequence_id")["current_frequency_mhz"]
    .shift(3)
)


# Remove rows that don't have enough history
df = df.dropna().reset_index(drop=True)


# --------------------------------------------------
# 3. FEATURES AND TARGET
# --------------------------------------------------

features = [
    "frequency_lag_3",
    "frequency_lag_2",
    "frequency_lag_1",
    "current_frequency_mhz"
]

X = df[features]

y = df["next_frequency_mhz"]


# --------------------------------------------------
# 4. TRAIN / TEST SPLIT
# --------------------------------------------------

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42
)

print(f"\nTraining samples: {len(X_train)}")
print(f"Testing samples : {len(X_test)}")


# --------------------------------------------------
# 5. CREATE MODEL
# --------------------------------------------------

model = RandomForestRegressor(
    n_estimators=200,
    random_state=42,
    n_jobs=-1
)


# --------------------------------------------------
# 6. TRAIN MODEL
# --------------------------------------------------

print("\nTraining frequency prediction model...")

model.fit(X_train, y_train)

print("Training completed!")


# --------------------------------------------------
# 7. PREDICTIONS
# --------------------------------------------------

y_pred = model.predict(X_test)


# --------------------------------------------------
# 8. EVALUATION
# --------------------------------------------------

mae = mean_absolute_error(y_test, y_pred)

mse = mean_squared_error(y_test, y_pred)

rmse = mse ** 0.5


print("\n========================================")
print(" FREQUENCY PREDICTOR PERFORMANCE")
print("========================================")

print(f"\nMAE  : {mae:.4f} MHz")
print(f"RMSE : {rmse:.4f} MHz")


# --------------------------------------------------
# 9. FEATURE IMPORTANCE
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
# 10. SAVE MODEL
# --------------------------------------------------

model_directory = (
    Path(__file__).parent
    / "saved_models"
)

model_directory.mkdir(exist_ok=True)

model_path = (
    model_directory
    / "frequency_predictor.joblib"
)

joblib.dump(model, model_path)


print("\n========================================")
print(" MODEL SAVED")
print("========================================")

print(f"Location: {model_path}")