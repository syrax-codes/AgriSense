# inspect_excel.py

import pandas as pd

# --- IMPORTANT ---
# Replace this with the name of the NEW Excel file you just uploaded
INPUT_XLSX_NAME = 'historical_data_2010-2020.xlsx'

try:
    df = pd.read_excel(INPUT_XLSX_NAME)
    
    print("\n--- Excel File Inspection ---")
    print("Here are the first 5 rows of your new file:\n")
    print(df.head())
    
    print("\n\n" + "="*50)
    print("!!! ACTION REQUIRED !!!")
    print("Please copy the list of column names below and paste it in your next reply.")
    print("="*50 + "\n")
    print(df.columns.tolist())
    
except FileNotFoundError:
    print(f"❌ Error: Could not find the file '{INPUT_XLSX_NAME}'. Please check the filename.")
except Exception as e:
    print(f"An unexpected error occurred: {e}")