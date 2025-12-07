from flask import Flask, request, jsonify
import joblib
import pandas as pd
import os

app = Flask(__name__)

# Base directory = project root (where this file is, go up one level)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

MODEL_PATH = os.path.join(BASE_DIR, "model", "aqi_model.pkl")

bundle = joblib.load(MODEL_PATH)
model = bundle["model"]
features = bundle["features"]


@app.route("/", methods=["GET"])
def home():
    return "AQI Prediction Server Running"


@app.route("/predict", methods=["POST"])
def predict():
    """
    Expected JSON:
    {
        "hour": 14,
        "weekday": 2,
        "lag_1": 90,
        "lag_2": 85,
        "lag_3": 82
    }
    """
    try:
        data = request.json
        df = pd.DataFrame([data])
        df = df[features]   # ensure correct columns order
        prediction = model.predict(df)[0]

        return jsonify({
            "predicted_pm25_30min": float(prediction)
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 400


if __name__ == "__main__":
    # For local running
    app.run(host="0.0.0.0", port=5000)
