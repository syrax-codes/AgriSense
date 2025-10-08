# inspect_new_data.py

import pandas as pd

# The name of the new CSV file you uploaded
INPUT_CSV_NAME = 'historical_data_2010-2020.csv'

try:
    # Load the CSV file
    df = pd.read_csv(INPUT_CSV_NAME)
    
    print("\n--- CSV File Inspection ---")
    print("Here are the first 5 rows of your new file:\n")
    print(df.head())
    
    print("\n\n" + "="*50)
    print("!!! ACTION REQUIRED !!!")
    print("Please copy the ENTIRE output below this line—especially the list of column names—and paste it in your next reply.")
    print("="*50 + "\n")
    
    # Print the info to see data types
    df.info()
    
    print("\n--- Column Names ---")
    # Print the list of column names
    print(df.columns.tolist())
    
except FileNotFoundError:
    print(f"❌ Error: Could not find '{INPUT_CSV_NAME}'. Make sure it's in your project root folder.")
except Exception as e:
    print(f"An unexpected error occurred: {e}")