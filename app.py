# app.py (Final Version without Gemini)

import pandas as pd
from flask import Flask, request, render_template, jsonify
import joblib
import os
from datetime import datetime
import numpy as np

from src.utils.satellite_data import get_ndvi_for_location

app = Flask(__name__)

# --- LOAD ALL FILES AT STARTUP ---
try:
    model = joblib.load("models/yield_prediction_model.joblib")
    model_columns = joblib.load("models/model_columns.pkl")
    districts_df = pd.read_csv("data/karnataka_districts.csv")
    yield_df = pd.read_csv("data/yield_data_tidy.csv")

    yield_df['District'] = yield_df['District'].str.strip().str.upper()
    districts_df['District'] = districts_df['District'].str.split('. ').str[-1].str.strip().str.upper()
    districts_to_remove = ["URBAN", "RURAL"]
    districts_list = sorted([d for d in yield_df['District'].unique() if d not in districts_to_remove])
    
    print("✅✅✅ Model and data files loaded successfully!")

except Exception as e:
    print(f"❌ CRITICAL ERROR during startup: {e}")
    model, districts_list = None, []

def calculate_risk_level(predicted_yield, avg_yield, current_ndvi):
    if pd.isna(avg_yield) or avg_yield == 0: return "Medium"
    risk = "Low"
    if predicted_yield < avg_yield * 0.85: risk = "High"
    elif predicted_yield < avg_yield: risk = "Medium"
    if current_ndvi < 0.35:
        if risk == "Medium": risk = "High"
        if risk == "Low": risk = "Medium"
    return risk

@app.route('/', methods=['GET', 'POST'])
def home():
    if model is None: return "<h1>Error: Model not loaded.</h1>", 500
    prediction_data, summary_data = None, None
    selected_district = request.form.get('district', '')
    selected_crop = request.form.get('crop', '')

    if request.method == 'POST' and selected_district and selected_crop:
        try:
            year = datetime.now().year
            district_info = districts_df[districts_df['District'] == selected_district]
            if district_info.empty: raise ValueError(f"Coordinates for '{selected_district}' not found.")
            lat, lon = district_info.iloc[0]['Latitude'], district_info.iloc[0]['Longitude']
            ndvi_data = get_ndvi_for_location(lat, lon, f"{year}-01-01", datetime.now().strftime("%Y-%m-%d"))
            avg_ndvi = pd.DataFrame(ndvi_data)['ndvi'].mean() if ndvi_data else 0.4
            input_data = pd.DataFrame([{'Year': year, 'District': selected_district, 'Crop': selected_crop, 'ndvi': avg_ndvi}])
            input_encoded = pd.get_dummies(input_data, columns=['District', 'Crop'])
            final_input = input_encoded.reindex(columns=model_columns, fill_value=0)
            prediction = model.predict(final_input)[0]
            subset = yield_df[(yield_df['District'] == selected_district) & (yield_df['Crop'] == selected_crop)]
            summary_data = {'avg_yield': round(subset['Yield'].mean(), 2), 'min_yield': round(subset['Yield'].min(), 2), 'max_yield': round(subset['Yield'].max(), 2)}
            risk = calculate_risk_level(prediction, summary_data['avg_yield'], avg_ndvi)
            prediction_data = {'predicted_yield': round(prediction, 2), 'risk_level': risk, 'current_avg_ndvi': round(avg_ndvi, 4)}

        except Exception as e:
            print(f"Error during prediction: {e}")
            prediction_data = {'error': str(e)}
    
    return render_template('index.html', 
                           districts=districts_list,
                           selected_district=selected_district, selected_crop=selected_crop,
                           prediction_data=prediction_data, summary_data=summary_data)

@app.route('/api/crops_for_district')
def get_crops_for_district_api():
    district = request.args.get('district')
    if district:
        crops = sorted(yield_df[yield_df['District'] == district.upper()]['Crop'].unique().tolist())
        return jsonify(crops)
    return jsonify([])

if __name__ == '__main__':
    app.run(debug=True)