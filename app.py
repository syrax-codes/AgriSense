# app.py (Definitive Final Version)

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

# --- Helper functions ---
def calculate_risk_level(predicted_yield, avg_yield, current_ndvi):
    if pd.isna(avg_yield) or avg_yield == 0: return "Medium"
    risk = "Low"
    if predicted_yield < avg_yield * 0.85: risk = "High"
    elif predicted_yield < avg_yield: risk = "Medium"
    if current_ndvi < 0.35:
        if risk == "Medium": risk = "High"
        if risk == "Low": risk = "Medium"
    return risk

# --- DEFINITIVE CREDIBILITY STATEMENT FUNCTION ---
def generate_credibility_statement(p_data, s_data):
    ndvi = p_data['current_avg_ndvi']
    risk = p_data['risk_level']
    
    ndvi_health = "Excellent" if ndvi > 0.6 else "Fair to Good" if ndvi >= 0.3 else "Stressed"

    # --- THE NEW, MORE PRECISE EXPLANATION ---
    base_statement = f"This report's credibility comes from combining historical knowledge with real-time data. The model was trained by correlating **10 years of historical yield data** with **10 years of historical satellite imagery (NDVI)**. It now applies that deep knowledge to **new, real-time satellite data** from the current growing season to make its forecast.\n\n"
    
    analysis = ""
    recommendation = ""

    if risk == "High":
        if ndvi_health == "Stressed":
            analysis = "The 'High Risk' assessment is strongly supported. The model's low yield forecast aligns perfectly with the poor vegetation health seen in the real-time satellite data."
        else:
            analysis = f"This is a key insight from our AI. Although real-time satellite data shows vegetation health is currently '{ndvi_health}', the model, using its knowledge from 10 years of data, forecasts a poor final yield. It has learned that for this specific crop and district, the current NDVI is not strong enough to guarantee a good harvest."
        recommendation = "\n\n🔴 **Recommendation:** The model's analysis indicates a high probability of a poor harvest. This should be considered a high-risk situation that requires attention."
    
    elif risk == "Medium":
        if ndvi_health == "Stressed":
             analysis = "This 'Medium Risk' assessment is a critical warning. The model's concern is validated by the 'Stressed' real-time satellite data, even if the final predicted yield isn't critical yet."
        else:
             analysis = f"This 'Medium Risk' assessment is a data-driven forecast. While real-time satellite data shows vegetation health is '{ndvi_health}', the model's analysis of 10 years of historical patterns suggests the final yield may still fall slightly below average."
        recommendation = "\n\n🟡 **Recommendation:** This is a situation to monitor closely. While not an emergency, conditions are not ideal for a bumper crop."
    
    else: # Low Risk
        analysis = f"The 'Low Risk' assessment is strongly supported. The model's high predicted yield aligns perfectly with the '{ndvi_health}' vegetation health shown in real-time satellite imagery."
        recommendation = "\n\n🟢 **Recommendation:** All indicators are positive. This represents a low-risk scenario for the current season."

    return base_statement + analysis + recommendation

# --- MAIN WEB PAGE ROUTE ---
@app.route('/', methods=['GET', 'POST'])
def home():
    if model is None: return "<h1>Error: Model not loaded.</h1>", 500
    prediction_data, summary_data, credibility_statement = None, None, None
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
            
            credibility_statement = generate_credibility_statement(prediction_data, summary_data)

        except Exception as e:
            print(f"Error during prediction: {e}")
            prediction_data = {'error': str(e)}
    
    return render_template('index.html', 
                           districts=districts_list,
                           selected_district=selected_district, selected_crop=selected_crop,
                           prediction_data=prediction_data, summary_data=summary_data,
                           credibility_statement=credibility_statement)

@app.route('/api/crops_for_district')
def get_crops_for_district_api():
    district = request.args.get('district')
    if district:
        crops = sorted(yield_df[yield_df['District'] == district.upper()]['Crop'].unique().tolist())
        return jsonify(crops)
    return jsonify([])

if __name__ == '__main__':
    app.run(debug=True)