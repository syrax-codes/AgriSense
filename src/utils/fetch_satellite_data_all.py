# fetch_satellite_data_all.py (Updated for 10-year range)

import pandas as pd
import os
import time

# This assumes your original function is in the file below.
from src.utils.satellite_data import get_ndvi_for_location

# --- PATHS ---
DATA_DIR = 'data'
DISTRICTS_CSV_PATH = os.path.join(DATA_DIR, 'karnataka_districts.csv')
OUTPUT_CSV_PATH = os.path.join(DATA_DIR, 'satellite_data_all_districts.csv')

# --- CONFIGURATION (THE ONLY CHANGE IS HERE) ---
# Fetch data for the entire 2010-2020 period
START_DATE = '2010-01-01'
END_DATE = '2020-12-31'


def run_batch_fetch():
    """
    Loops through districts and fetches satellite data for each one.
    """
    try:
        districts_df = pd.read_csv(DISTRICTS_CSV_PATH)
    except FileNotFoundError:
        print(f"❌ Error: Could not find '{DISTRICTS_CSV_PATH}'.")
        return

    all_ndvi_data = []
    print(f"--- Starting 10-YEAR satellite data fetch for {len(districts_df)} districts ---")
    print(f"--- Period: {START_DATE} to {END_DATE} ---")

    # Loop through each district from the CSV
    for index, row in districts_df.iterrows():
        district_name = str(row['District']).split('. ')[-1].strip()
        lat = row['Latitude']
        lon = row['Longitude']
        
        print(f"\nFetching data for: {district_name} ({lat:.4f}, {lon:.4f})")
        
        try:
            # Call your existing function to get NDVI data
            ndvi_data = get_ndvi_for_location(lat, lon, START_DATE, END_DATE)
            
            if ndvi_data:
                # Add the district name to each result
                for record in ndvi_data:
                    record['District'] = district_name
                
                all_ndvi_data.extend(ndvi_data)
                print(f"  ✅ Found {len(ndvi_data)} records.")
            else:
                print("  ⚠️ No data found for this district.")
                
        except Exception as e:
            print(f"  ❌ An error occurred for {district_name}: {e}")
        
        time.sleep(1)

    if all_ndvi_data:
        final_df = pd.DataFrame(all_ndvi_data)
        final_df.to_csv(OUTPUT_CSV_PATH, index=False)
        print(f"\n\n✅✅✅ Success! All satellite data saved to '{OUTPUT_CSV_PATH}'")
        print(f"Total records fetched: {len(final_df)}")
    else:
        print("\n\n❌ No satellite data was fetched for any district.")


if __name__ == "__main__":
    run_batch_fetch()