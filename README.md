# AgriSense: An AI-Powered Crop Yield Prediction Dashboard

## The Problem
Traditional crop insurance relies on a slow, expensive, and inefficient process. When a farmer files a claim, a human inspector must physically visit the farm to verify the loss. This manual system suffers from several critical flaws:
Slow Payouts: Inspections can take weeks or months, delaying crucial financial relief for farmers.
High Costs: The operational cost of manual inspections leads to higher insurance premiums.
Inaccessibility: The model is not scalable to remote regions with limited infrastructure.
Subjectivity & Fraud: Assessments are prone to human bias and potential fraud.
->This provides faster, fairer, and more accessible financial security for farmers, investors, and lenders.

## Our Solution: AgriSense
AgriSense is an AI-powered web dashboard that revolutionizes this process. It provides a data-driven, automated solution for crop yield prediction and risk assessment.

Our platform combines 10 years of historical government yield data with 10 years of corresponding satellite imagery (NDVI) to train a highly accurate RandomForest Regressor model (R^2 score of 95.8%).
### When a user selects a district and crop, our application:
Fetches real-time satellite data for the current growing season.
Uses our pre-trained AI model to forecast the final yield.
Calculates a risk assessment (Low, Medium, High) by comparing the prediction to historical benchmarks and current vegetation health.
Presents all key metrics—including predicted yield, historical stats, and live NDVI—in a clean, intuitive dashboard.
This automates the assessment process, providing an objective, scalable, and instant analysis that empowers farmers, lenders, and investors with actionable data.

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
AgriSense AI engine comprising of 2 models Validating the AgriSense Concept, Provides real-time anomaly detection for stress events and forecasting for future planning.

The Jupyter notebooks in the directory contain the foundational research that validates the concept behind AgriSense. While these models are not directly integrated into this prototype dashboard, they serve as the *proof-of-concept, demonstrating that it is *possible to accurately predict crop yield by fusing historical and satellite data. This analysis is the scientific backbone of the project, proving that the core idea is technically sound and data-driven.

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
3.  Navigate to the directory.
4.  Open and run the Jupyter Notebooks sequentially.

---
## Datasets Used for jupyter notebooks

* **historical_data_2010-2020.csv**: The source for historical crop yield statistics.
* **satellite_data_all_districts.csv**: The source for time-series of daily NDVI (vegetation health) values.

Drive Link For The Generated Report By Our Yield Predictor Model: https://drive.google.com/drive/folders/1HWuuMQhuipM23CtAWg76T_BapTH9oJMi?usp=drive_link

Drive Link For Video-Submission: https://drive.google.com/drive/folders/1WehjKgnU8uZ053naKf6Dx9XbqMwTxeJq?usp=drive_link


Team Roles
Abhiraj Dhananjay - Lead ML Engineer (RandomForest Model) & Full-Stack Development
Abhinav Bora - Backend Development & Jupyter Notebook Prototyping (XGBoost Models)
Santosh Balla - Backend Development & Data Engineering
Aditya Vashisht - Frontend Development & UI/UX Design, pitch deck design
Aarohi Jaiswal - Frontend Development & Video Editing, pitch deck design
Abhay Kulkarni - ML Engineer & Data Analysis

