# prepare_yield_data.py (Final Version with ffill)

import pandas as pd
import os

# --- CONFIGURATION ---
INPUT_XLSX_NAME = 'historical_data_2010-2020.xlsx' 

# --- PATHS ---
output_dir = 'data'
TIDY_CSV_PATH = os.path.join(output_dir, 'yield_data_tidy.csv')

os.makedirs(output_dir, exist_ok=True)

print(f"Reading and transforming complex Excel file: '{INPUT_XLSX_NAME}'...")

try:
    # 1. Read the Multi-Level Header
    df = pd.read_excel(INPUT_XLSX_NAME, header=[0, 1, 2])
    
    # 2. Flatten the Headers
    new_columns = ['_'.join(str(c) for c in col).strip() for col in df.columns]
    df.columns = new_columns

    # 3. Select Only the Columns We Need
    id_cols_original = df.columns[:3].tolist()
    yield_cols = [col for col in df.columns if 'Yield' in col]
    df_yields = df[id_cols_original + yield_cols]
    
    # 4. Melt the DataFrame
    df_long = pd.melt(
        df_yields,
        id_vars=id_cols_original,
        var_name='Crop_Season_Metric',
        value_name='Yield'
    )
    
    # 5. --- FINAL CLEANING ---
    df_long[['Crop', 'Season', 'Metric']] = df_long['Crop_Season_Metric'].str.split('_', expand=True)
    
    # Rename the original ID columns to simple names
    df_long.rename(columns={
        id_cols_original[0]: 'State',
        id_cols_original[1]: 'District',
        id_cols_original[2]: 'Year'
    }, inplace=True)
    
    df_final = df_long[['State', 'District', 'Year', 'Crop', 'Season', 'Yield']]
    
    # --- NEW FIX: Forward fill to handle merged cells ---
    df_final['State'] = df_final['State'].ffill()
    df_final['District'] = df_final['District'].ffill()
    
    # --- NEW FIX: Clean prefixes like "1. " from names ---
    df_final['State'] = df_final['State'].str.split('. ').str[-1].str.strip()
    df_final['District'] = df_final['District'].str.split('. ').str[-1].str.strip()
    
    df_final.dropna(subset=['Yield'], inplace=True)
    df_final = df_final[df_final['Yield'] != 0].copy()

    # 6. --- SAVE THE FINAL CSV ---
    df_final.to_csv(TIDY_CSV_PATH, index=False)

    print(f"\n✅✅✅ Success! Final clean file saved to '{TIDY_CSV_PATH}'")
    print("\n--- Final Transformed Data (Tidy Format) ---")
    print(df_final.head())
    
except FileNotFoundError:
    print(f"❌ Error: The file '{INPUT_XLSX_NAME}' was not found.")
except Exception as e:
    print(f"An unexpected error occurred: {e}")