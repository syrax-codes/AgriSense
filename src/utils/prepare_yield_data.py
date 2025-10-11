# prepare_yield_data.py (Final Version)
import pandas as pd
import os

DATA_DIR = 'data'
# Looks for the raw file inside the 'data' folder now
INPUT_CSV_NAME = os.path.join(DATA_DIR, 'historical_data_2010-2020.csv')
TIDY_CSV_PATH = os.path.join(DATA_DIR, 'yield_data_tidy.csv')

print(f"Reading and transforming '{INPUT_CSV_NAME}'...")
try:
    # Reads the first 3 rows as the headers
    df = pd.read_excel(INPUT_CSV_NAME.replace('.csv', '.xlsx'), header=[0, 1, 2])
    
    # Flatten the multi-level headers
    df.columns = ['_'.join(str(c) for c in col).strip() for col in df.columns]

    # Select only the ID and Yield columns
    id_cols = df.columns[:3].tolist()
    yield_cols = [col for col in df.columns if 'Yield' in col]
    df_yields = df[id_cols + yield_cols]
    
    # Transform from wide to long format
    df_long = pd.melt(df_yields, id_vars=id_cols, var_name='Crop_Info', value_name='Yield')
    
    # Final Cleaning
    df_long[['Crop', 'Season', 'Metric']] = df_long['Crop_Info'].str.split('_', expand=True)
    df_long.rename(columns={id_cols[0]: 'State', id_cols[1]: 'District', id_cols[2]: 'Year'}, inplace=True)
    df_final = df_long[['State', 'District', 'Year', 'Crop', 'Season', 'Yield']]
    df_final['State'] = df_final['State'].ffill()
    df_final['District'] = df_final['District'].ffill()
    df_final['State'] = df_final['State'].str.split('. ').str[-1].str.strip()
    df_final['District'] = df_final['District'].str.split('. ').str[-1].str.strip()
    df_final.dropna(subset=['Yield'], inplace=True)
    df_final = df_final[df_final['Yield'] != 0].copy()

    # Save the final clean file
    df_final.to_csv(TIDY_CSV_PATH, index=False)
    print(f"\n✅✅✅ Success! Final clean file saved to '{TIDY_CSV_PATH}'")
except Exception as e:
    print(f"An unexpected error occurred: {e}")