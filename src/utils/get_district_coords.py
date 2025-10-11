# get_district_coords.py (Corrected Version)

import pandas as pd
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
import os
import time

print("--- Starting District Geocoding ---")

# --- PATHS ---
DATA_DIR = 'data'
YIELD_DATA_PATH = os.path.join(DATA_DIR, 'yield_data_tidy.csv')
DISTRICTS_CSV_PATH = os.path.join(DATA_DIR, 'karnataka_districts.csv')

try:
    # 1. Load the tidy yield data
    yield_df = pd.read_csv(YIELD_DATA_PATH)
    
    # --- NEW: Clean the 'District' column before using it ---
    yield_df.dropna(subset=['District'], inplace=True) # Remove rows with empty districts
    yield_df['District'] = yield_df['District'].astype(str) # Ensure all districts are strings
    
    # 2. Get unique district names (this is now safe to run)
    unique_districts = sorted(yield_df['District'].unique())
    print(f"Found {len(unique_districts)} unique, clean districts.")

    # 3. Geocode each district
    geolocator = Nominatim(user_agent="karnataka-crop-yield-app")
    geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)
    
    locations = []
    print("\nFetching coordinates for each district (this may take a minute or two)...")
    for district in unique_districts:
        query = f"{district}, Karnataka, India"
        try:
            location = geocode(query)
            if location:
                locations.append({
                    'District': district,
                    'Latitude': location.latitude,
                    'Longitude': location.longitude
                })
                print(f"  ✅ Found: {district} -> ({location.latitude:.4f}, {location.longitude:.4f})")
            else:
                locations.append({ 'District': district, 'Latitude': None, 'Longitude': None })
                print(f"  ❌ Not Found: {district}")
        except Exception as e:
            print(f"  An error occurred for {district}: {e}")
            locations.append({ 'District': district, 'Latitude': None, 'Longitude': None })

    # 4. Save to a new CSV file
    districts_df = pd.DataFrame(locations)
    districts_df.dropna(inplace=True) # Drop districts that were not found
    districts_df.to_csv(DISTRICTS_CSV_PATH, index=False)
    
    print(f"\n✅ Successfully saved district coordinates to '{DISTRICTS_CSV_PATH}'")
    print("\n--- Preview of Coordinates File ---")
    print(districts_df.head())

except FileNotFoundError:
    print(f"❌ Error: The file '{YIELD_DATA_PATH}' was not found. Please make sure you have run the data preparation script first.")
except Exception as e:
    print(f"An unexpected error occurred: {e}")