# AgriSecure: An AI-Powered Crop Yield Prediction Dashboard

## Problem Statement
Traditional crop insurance is slow, expensive, and prone to fraud, especially in regions with limited infrastructure. Our project builds a satellite-based crop insurance platform that leverages satellite imagery and machine learning to automatically evaluate crop health and predict yield. This provides faster, fairer, and more accessible financial security for farmers, investors, and lenders.

## Features
- **Dynamic Yield Prediction:** Select a district and crop to get a real-time yield prediction for the current season.
- **AI-Powered Risk Assessment:** The dashboard provides a "Low," "Medium," or "High" risk assessment based on a comparison of the predicted yield against historical data and current satellite imagery (NDVI).
- **Data-Rich Dashboard:** View key metrics including predicted yield, historical average, min/max yields, and the current NDVI score.
- **Downloadable Reports:** Generate and download a clean PDF report of the analysis with a single click.

## How to Run This Project
1.  Clone the repository.
2.  Create and activate a Python virtual environment:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Linux/Mac
    .\venv\Scripts\Activate.ps1 # On Windows
    ```
3.  Install the required packages:
    ```bash
    pip install -r requirements.txt
    ```
4.  Run the Flask application:
    ```bash
    flask run
    ```
5.  Open your web browser and navigate to `http://127.0.0.1:5000`.

## Exploratory Research Using ML Models (XGBoost): Validating the AgriSense Concept (Jupyter Notebooks)
Agrisense Ai engine comprising of 2 models Validating the AgriSense Concept, Provides real-time anomaly detection for stress events and forecasting for future planning.

The Jupyter notebooks in the /notebooks directory contain the foundational research that validates the concept behind AgriSecure. While these models are not directly integrated into this prototype dashboard, they serve as the *proof-of-concept, demonstrating that it is *possible to accurately predict crop yield by fusing historical and satellite data. This analysis is the scientific backbone of the project, proving that the core idea is technically sound and data-driven.

### How This Research Enhances Our Project

The notebooks provide a deep, visual exploration of the data and our modeling journey. Through dozens of graphs and statistical analyses, they show:

* *How to Overcome Data Challenges:* We document the process of cleaning and reshaping complex, real-world government data.
* *The Power of Data Fusion:* We prove that integrating satellite (NDVI) data with historical records significantly improves prediction accuracy. This is demonstrated by comparing two XGBoost models:
    1.  *A Baseline Model* using only historical data.
    2.  *An Enhanced Model* that incorporates the new satellite features.
* *The Path to a Complete Solution:* The notebooks also explore advanced capabilities like *Explainable AI (SHAP)* for transparency, *Anomaly Detection* for real-time monitoring, and *Forecasting* for future insights, laying out a clear roadmap for future development.

### How to Run the Analysis Notebooks

To explore our research and reproduce the models:

1.  Ensure you have completed the installation steps above.
2.  Place the raw datasets (historical_data... and satellite_data...) in the root directory.
3.  Navigate to the /notebooks directory.
4.  Open and run the Jupyter Notebooks sequentially.

---
## Datasets Used for jupyter notebooks

* **historical_data_2010-2020.csv**: The source for historical crop yield statistics.
* **satellite_data_all_districts.csv**: The source for time-series of daily NDVI (vegetation health) values.