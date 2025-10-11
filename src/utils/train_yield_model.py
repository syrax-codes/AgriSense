# train_yield_model.py (Final version with District name cleaning)

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score
import joblib
import os

print("--- Starting Final District-Aware Model Training ---")

# --- PATHS ---
DATA_DIR = 'data'
SATELLITE_DATA_PATH = os.path.join(DATA_DIR, 'satellite_data_all_districts.csv')
YIELD_DATA_PATH = os.path.join(DATA_DIR, 'yield_data_tidy.csv')
MODEL_DIR = 'models'
MODEL_PATH = os.path.join(MODEL_DIR, 'yield_prediction_model.joblib')
MODEL_COLUMNS_PATH = os.path.join(MODEL_DIR, 'model_columns.pkl')

os.makedirs(MODEL_DIR, exist_ok=True)

# --- 1. LOAD DATA ---
try:
    satellite_df = pd.read_csv(SATELLITE_DATA_PATH)
    yield_df = pd.read_csv(YIELD_DATA_PATH)
    print("✅ Data loaded successfully.")
except FileNotFoundError as e:
    print(f"❌ Error: Missing data file. {e}")
    exit()

# --- 2. DATA PREPARATION & AGGREGATION ---
satellite_df['date'] = pd.to_datetime(satellite_df['date'])
satellite_df['Year'] = satellite_df['date'].dt.year

yield_df.dropna(subset=['Year'], inplace=True)
yield_df['Year'] = yield_df['Year'].astype(str).apply(lambda x: x.split('-')[0].strip())
yield_df['Year'] = pd.to_numeric(yield_df['Year'], errors='coerce')
yield_df.dropna(subset=['Year'], inplace=True)
yield_df['Year'] = yield_df['Year'].astype(int)

# Aggregate satellite data
yearly_agg_df = satellite_df.groupby(['Year', 'District'])['ndvi'].mean().reset_index()

# --- NEW FIX: Standardize the 'District' names in both dataframes before merging ---
yield_df['District'] = yield_df['District'].str.strip().str.upper()
yearly_agg_df['District'] = yearly_agg_df['District'].str.strip().str.upper()
# --- End of Fix ---

print("\nAggregated yearly NDVI data per district (sample):")
print(yearly_agg_df.head())

# Merge the two datasets
master_df = pd.merge(yield_df, yearly_agg_df, on=['Year', 'District'], how='inner')
master_df.dropna(inplace=True)

# Check if the merge was successful
if master_df.empty:
    print("\n❌ CRITICAL ERROR: The master dataset is empty after merging.")
    print("   This means there are still no matching 'Year' and 'District' pairs.")
    print(f"   Sample Years in yield_df: {yield_df['Year'].unique()[:5]}")
    print(f"   Sample Years in yearly_agg_df: {yearly_agg_df['Year'].unique()[:5]}")
    exit()

print("\nCreated master training dataset (sample):")
print(master_df.head())

# --- 3. FEATURE ENGINEERING ---
target = 'Yield'
features = ['Year', 'District', 'Crop', 'ndvi'] 

X = pd.get_dummies(master_df[features], columns=['District', 'Crop'], drop_first=True)
y = master_df[target]

joblib.dump(X.columns.tolist(), MODEL_COLUMNS_PATH)
print(f"\n✅ Model columns saved to {MODEL_COLUMNS_PATH}")

# --- 4. MODEL TRAINING ---
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
print(f"\nData split into {len(X_train)} training and {len(X_test)} testing records.")

model = RandomForestRegressor(n_estimators=100, random_state=42)
print("\nTraining the model...")
model.fit(X_train, y_train)
print("✅ Model training complete.")

# --- 5. MODEL EVALUATION ---
y_pred = model.predict(X_test)
mae = mean_absolute_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print("\n--- Model Performance ---")
print(f"R-squared (R²): {r2:.2%}")
print(f"Mean Absolute Error (MAE): {mae:.4f} tonnes/hectare")

# --- 6. SAVE THE TRAINED MODEL ---
joblib.dump(model, MODEL_PATH)
print(f"\n✅ Trained model saved to: {MODEL_PATH}")