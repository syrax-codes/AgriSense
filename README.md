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

## Exploratory Analysis Notebooks
The `/notebooks` directory contains additional exploratory models built using XGBoost, which were part of our team's initial research and model comparison efforts.