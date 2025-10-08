# inspect_excel_deeper.py

import pandas as pd

# --- IMPORTANT ---
# Make sure this is the name of your 2010-2020 Excel file
INPUT_XLSX_NAME = 'historical_data_2010-2020.xlsx' 
# If you haven't renamed it, the original file you uploaded might still have a long name.
# Please double-check the filename in your project folder.

try:
    # --- KEY CHANGE: Reads the second row of the file as the header ---
    df = pd.read_excel(INPUT_XLSX_NAME, header=1)
    
    print("\n--- Deeper Excel File Inspection ---")
    print("Here are the first 5 rows using the *second row* as headers:\n")
    print(df.head())
    
    print("\n\n" + "="*50)
    print("!!! ACTION REQUIRED !!!")
    print("The column names below should now be descriptive (e.g., 'Area', 'Production', 'Yield').")
    print("Please find the exact name for the YIELD column and paste it in your next reply.")
    print("="*50 + "\n")
    print(df.columns.tolist())
    
except FileNotFoundError:
    print(f"❌ Error: Could not find the file '{INPUT_XLSX_NAME}'. Please check the filename.")
except Exception as e:
    print(f"An unexpected error occurred: {e}")