import requests
import pandas as pd
import os

# Replace with your token
TOKEN = "3012367bab5f4e37133e943579cce21a53baee75"
URL = f"https://api.waqi.info/feed/pune/?token={TOKEN}"

# Our logfile
FILE_PATH = "../data/pune_aqi.csv"


def fetch_pune_aqi():
    """Fetch AQI data from WAQI and append to CSV."""
    try:
        r = requests.get(URL)
        data = r.json()

        if data["status"] != "ok":
            print("❌ API Error:", data)
            return

        iaqi = data["data"]["iaqi"]

        pm25 = iaqi["pm25"]["v"] if "pm25" in iaqi else None
        pm10 = iaqi["pm10"]["v"] if "pm10" in iaqi else None
        timestamp = data["data"]["time"]["iso"]

        row = {
            "timestamp": timestamp,
            "pm25": pm25,
            "pm10": pm10
        }

        # If CSV does not exist → create it
        if not os.path.exists(FILE_PATH):
            df = pd.DataFrame([row])
            df.to_csv(FILE_PATH, index=False)
            print("📄 Created pune_aqi.csv with first row.")
        else:
            # Append new row
            df = pd.DataFrame([row])
            df.to_csv(FILE_PATH, mode="a", header=False, index=False)
            print(f"➕ Added new row → {timestamp}, PM2.5={pm25}, PM10={pm10}")

    except Exception as e:
        print("❌ Error:", e)


# Run the function
fetch_pune_aqi()
