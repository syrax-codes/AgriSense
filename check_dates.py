import pandas as pd
import os

# --- PATHS ---
DATA_DIR = "data"
WEATHER_PATH = os.path.join(DATA_DIR, "weather_data.csv")
SATELLITE_PATH = os.path.join(DATA_DIR, "satellite_data.csv")

print("--- Checking for date overlaps ---\n")

# --- Load and inspect weather data ---
try:
    weather_df = pd.read_csv(WEATHER_PATH)
    weather_df['date'] = pd.to_datetime(weather_df.get('datetime', weather_df.get('date'))).dt.strftime('%Y-%m-%d')
    weather_dates = set(weather_df['date'])
    print(f"✅ Found {len(weather_dates)} unique dates in weather_data.csv.")
    print(f"   Sample dates: {list(weather_dates)[:5]}\n")
except Exception as e:
    print(f"❌ Error reading weather_data.csv: {e}")
    weather_dates = set()

# --- Load and inspect satellite data ---
try:
    satellite_df = pd.read_csv(SATELLITE_PATH)
    satellite_df['date'] = pd.to_datetime(satellite_df['date']).dt.strftime('%Y-%m-%d')
    satellite_dates = set(satellite_df['date'])
    print(f"✅ Found {len(satellite_dates)} unique dates in satellite_data.csv.")
    print(f"   Sample dates: {list(satellite_dates)[:5]}\n")
except Exception as e:
    print(f"❌ Error reading satellite_data.csv: {e}")
    satellite_dates = set()

# --- Find the intersection ---
if weather_dates and satellite_dates:
    common_dates = weather_dates.intersection(satellite_dates)
    print(f"--- RESULTS ---")
    print(f"🗓️ Found {len(common_dates)} common dates between the two files.")
    if common_dates:
        print(f"   Common dates sample: {list(common_dates)[:5]}")
    else:
        print("   ‼️ The files have no dates in common, which explains the empty merge.")