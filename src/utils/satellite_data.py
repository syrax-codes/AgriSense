import ee

# This function initializes the Earth Engine API.
# It's good practice to have it handle potential initialization errors.
try:
    ee.Initialize()
    print("Earth Engine initialized successfully.")
except Exception as e:
    print(f"Warning: Could not initialize Earth Engine. Attempting authentication...")
    try:
        ee.Authenticate()
        ee.Initialize()
        print("Earth Engine authenticated and initialized successfully.")
    except Exception as auth_e:
        print(f"Fatal Error: Could not authenticate or initialize Earth Engine: {auth_e}")


def get_ndvi_for_location(lat, lon, start_date, end_date):
    """
    Fetches a time series of NDVI values for a specific location and date range.
    Returns a list of dictionaries, e.g., [{'date': 'YYYY-MM-DD', 'ndvi': 0.75}].
    """
    point = ee.Geometry.Point(lon, lat)

    # Use the newer, harmonized Sentinel-2 dataset for better results
    s2 = ee.ImageCollection('COPERNICUS/S2_SR_HARMONIZED') \
        .filterBounds(point) \
        .filterDate(start_date, end_date) \
        .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 20)) # Filter for clear images

    def add_ndvi(image):
        """A function to calculate and add an NDVI band to an image."""
        ndvi = image.normalizedDifference(['B8', 'B4']).rename('NDVI')
        return image.addBands(ndvi)

    ndvi_col = s2.map(add_ndvi)

    # getInfo() returns a standard Python object (usually a list of lists)
    ndvi_values = ndvi_col.select('NDVI').getRegion(point, 10).getInfo()

    # --- THIS IS THE KEY FIX ---
    # The error you saw happens when an 'if' statement is used on a whole table of data.
    # The code below correctly checks if the returned list has any data rows before processing.
    if not ndvi_values or len(ndvi_values) < 2:
        return []  # Return an empty list if no data was found

    # --- Robust Data Parsing ---
    header = ndvi_values[0]
    try:
        time_index = header.index('time')
        ndvi_index = header.index('NDVI')
    except ValueError:
        # This handles cases where the expected columns aren't in the data
        return []

    ndvi_list = []
    for row in ndvi_values[1:]:  # Skip the header row
        date = ee.Date(row[time_index]).format('YYYY-MM-dd').getInfo()
        ndvi = row[ndvi_index]
        if ndvi is not None:
            # Round the NDVI value for cleaner data
            ndvi_list.append({'date': date, 'ndvi': round(ndvi, 4)})

    return ndvi_list


# This block allows you to test this file directly if you ever need to
if __name__ == "__main__":
    print("\n--- Running a standalone test for satellite_data.py ---")
    # Test with Bengaluru coordinates
    test_lat, test_lon = 12.9716, 77.5946
    test_start = '2024-04-01'
    test_end = '2024-06-30'
    
    print(f"Fetching test data for Bengaluru between {test_start} and {test_end}...")
    data = get_ndvi_for_location(test_lat, test_lon, test_start, test_end)
    
    if data:
        print(f"✅ Successfully fetched {len(data)} records for the test.")
        print("Sample data:")
        print(data[:3])
    else:
        print("❌ No data found for the test case.")