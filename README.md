# IBM-datathon

# AgriSense Pro — Karnataka Edition (MVP)

Minimal repo to build a parcel-level Dynamic Yield Risk Score (DYRS) system.

Quickstart:
1. python3 -m venv .venv && source .venv/bin/activate
2. pip install -r requirements.txt
3. python src/prototype.py      # run synthetic end-to-end prototype
4. uvicorn src.api.app:app --reload  # start API (healthcheck)

Project layout:
- data/: sample / processed data
- src/: core code
  - src/data/: ingestion stubs
  - src/features/: feature engineering
  - src/models/: training & predict
  - src/api/: FastAPI app
- notebooks/: EDA
- tests/: unit tests

Goals:
- MVP: parcel-level risk score using NDVI-like timeseries + weather features and XGBoost
- Next: Hook into GEE + OpenWeatherMap, add PostGIS storage, refine scoring

hello world 


