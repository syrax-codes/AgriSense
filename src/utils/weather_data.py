# C:\...\src\utils\weather_data.py

import os
import pandas as pd
import requests
from dotenv import load_dotenv
import time

# --- SETUP ---
# Load API key from .env file
load_dotenv()
API_KEY = os.getenv("OPENWEATHER_API_KEY")

# Define the output path
SRC_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(SRC_DIR, "../.."))
DATA_DIR = os.path.join(PROJECT_ROOT, "data")
os.makedirs(DATA_DIR, exist_ok=True)
WEATHER_PATH = os.path.join(DATA_DIR, "weather_data.csv")

def get_daily_weather(lat, lon, date_unix):
    """Fetches weather for a single day using the One Call API 1.0 (requires subscription)."""
    # Note: Free tier has limitations. This endpoint is for demonstration.
    # For a datathon, fetching the 'current' weather for each day might be a workaround if you don't have a paid key.
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}&units=metric"

    if not API_KEY:
        raise ValueError("❌ API key not found. Please add OPENWEATHER_API_KEY in .env")

    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        weather_info = {
            'date': pd.to_datetime(date_unix, unit='s').strftime('%Y-%m-%d'),
            'lat': lat,
            'lon': lon,
            'temperature': data['main']['temp'],
            'humidity': data['main']['humidity'],
            'pressure': data['main']['pressure'],
            'weather': data['weather'][0]['description']
        }
        return weather_info
    else:
        print(f"Failed to fetch data for {pd.to_datetime(date_unix, unit='s').date()}: {response.status_code}")
        return None

if __name__ == "__main__":
    lat, lon = 12.9716, 77.5946  # Bengaluru

    # --- NEW: Create a date range for the entire year ---
    date_range = pd.date_range(start='2024-01-01', end='2024-12-31', freq='D')
    all_weather_data = []

    print(f"Fetching daily weather data for {len(date_range)} days in 2024...")

    for single_date in date_range:
        # We'll use the current weather endpoint as a stand-in for historical data.
        # In a real-world scenario, you'd use a historical weather API.
        unix_timestamp = int(single_date.timestamp())
        daily_data = get_daily_weather(lat, lon, unix_timestamp)
        if daily_data:
            all_weather_data.append(daily_data)
            print(f"  -> Fetched data for {daily_data['date']}")
        time.sleep(0.1) # Small delay to be kind to the API

    # --- NEW: Save all collected data to a DataFrame and then to CSV ---
    if all_weather_data:
        weather_df = pd.DataFrame(all_weather_data)
        weather_df.to_csv(WEATHER_PATH, index=False)
        print(f"\n✅ Successfully saved {len(weather_df)} weather records to:")
        print(WEATHER_PATH)
    else:
        print("\n❌ No weather data was fetched. Please check your API key and network.")