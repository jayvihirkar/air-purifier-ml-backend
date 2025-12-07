import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# How many days of fake data?
DAYS = 7

start_time = datetime.now() - timedelta(days=DAYS)
timestamps = []
pm25_values = []
pm10_values = []

current_time = start_time
current_pm25 = 70      # base value
current_pm10 = 110     # base value

while current_time <= datetime.now():
    timestamps.append(current_time.isoformat())

    # Add random small fluctuations like real air quality
    current_pm25 += np.random.randint(-8, 9)
    current_pm10 += np.random.randint(-12, 13)

    # Keep values realistic
    current_pm25 = max(20, min(current_pm25, 350))
    current_pm10 = max(30, min(current_pm10, 400))

    pm25_values.append(current_pm25)
    pm10_values.append(current_pm10)

    # Move forward 15 minutes
    current_time += timedelta(minutes=15)

# Create DataFrame
df = pd.DataFrame({
    "timestamp": timestamps,
    "pm25": pm25_values,
    "pm10": pm10_values
})

df.to_csv("../data/pune_aqi.csv", index=False)

print("Fake dataset generated → ../data/pune_aqi.csv")
print("Rows:", len(df))
