import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error
import joblib

# Load your dataset
df = pd.read_csv("../data/pune_aqi.csv")

# Fix timestamp format
df["timestamp"] = pd.to_datetime(df["timestamp"])
df = df.sort_values("timestamp")

# Keep only pm25 for prediction
df = df.dropna(subset=["pm25"])   # remove rows with missing pm25

# Create time-based features
df["hour"] = df["timestamp"].dt.hour
df["day"] = df["timestamp"].dt.day
df["weekday"] = df["timestamp"].dt.weekday

# ---------------------------
# LAG FEATURES (very important)
# ---------------------------

# We assume your script logs every 15 minutes.
# So lag_2 = 30 minutes ago.

df["lag_1"] = df["pm25"].shift(1)  # 15 mins ago
df["lag_2"] = df["pm25"].shift(2)  # 30 mins ago
df["lag_3"] = df["pm25"].shift(3)  # 45 mins ago

# ---------------------------
# TARGET: PM2.5 after 30 minutes
# ---------------------------

df["target_pm25_30min"] = df["pm25"].shift(-2)

# Remove rows with missing lag/target values
df = df.dropna()

# Feature columns for training
features = ["hour", "weekday", "lag_1", "lag_2", "lag_3"]

X = df[features]
y = df["target_pm25_30min"]

# Train-test split (no shuffle because it's time-series)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, shuffle=False
)

# Random Forest model
model = RandomForestRegressor(
    n_estimators=300,
    max_depth=12,
    random_state=42
)

model.fit(X_train, y_train)

# Evaluate
pred = model.predict(X_test)
mae = mean_absolute_error(y_test, pred)
print("Model MAE:", mae)

# Save model
joblib.dump({
    "model": model,
    "features": features
}, "aqi_model.pkl")

print("🎉 Model saved as aqi_model.pkl")
