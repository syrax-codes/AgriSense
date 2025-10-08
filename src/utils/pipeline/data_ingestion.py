import os
import pandas as pd

# --- PATH HANDLING (fixed for project root) ---
SRC_DIR = os.path.dirname(os.path.abspath(__file__))              # .../src/utils/pipeline
PROJECT_ROOT = os.path.abspath(os.path.join(SRC_DIR, "../../..")) # .../IBM-datathon
DATA_DIR = os.path.join(PROJECT_ROOT, "data")                     # .../IBM-datathon/data
os.makedirs(DATA_DIR, exist_ok=True)

# Input file paths
WEATHER_PATH = os.path.join(DATA_DIR, "weather_data.csv")
SATELLITE_PATH = os.path.join(DATA_DIR, "satellite_data.csv")

# Output file path
MERGED_PATH = os.path.join(DATA_DIR, "merged_farm_data.csv")


def merge_weather_ndvi():
    """Merge weather and NDVI datasets by date."""
    if not os.path.exists(WEATHER_PATH):
        raise FileNotFoundError(f"❌ Missing: {WEATHER_PATH}")
    if not os.path.exists(SATELLITE_PATH):
        raise FileNotFoundError(f"❌ Missing: {SATELLITE_PATH}")

    # Load both CSVs
    weather_df = pd.read_csv(WEATHER_PATH)
    ndvi_df = pd.read_csv(SATELLITE_PATH)

    # --- Normalize column names and date formats ---
    if 'datetime' in weather_df.columns:
        weather_df.rename(columns={'datetime': 'date'}, inplace=True)

    weather_df['date'] = pd.to_datetime(weather_df['date']).dt.strftime('%Y-%m-%d')
    ndvi_df['date'] = pd.to_datetime(ndvi_df['date']).dt.strftime('%Y-%m-%d')

    # --- Merge on 'date' ---
    merged = pd.merge(ndvi_df, weather_df, on='date', how='inner')

    # Save merged data
    merged.to_csv(MERGED_PATH, index=False)
    print(f"✅ Merged dataset saved to: {MERGED_PATH}")
    print(f"🔹 Records merged: {len(merged)}")

    return merged


if __name__ == "__main__":
    df = merge_weather_ndvi()
    print("\nPreview of merged dataset:")
    print(df.head())
