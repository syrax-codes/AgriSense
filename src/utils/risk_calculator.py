import numpy as np
import pandas as pd
from typing import Dict, Any

# --- DYRS CALCULATION UTILITIES ---

def calculate_full_dyrs(
    predicted_yield: float, 
    historical_avg_yield: float, 
    historical_yield_cv: float, 
    ndvi_z_score: float, 
    base_score: int = 50
) -> Dict[str, float]:
    """
    Calculates the full Dynamic Yield Risk Score (DYRS, 0-100) based on 
    the weighted combination of three factors.
    
    Weights: 60% Yield Accuracy, 30% Anomaly Stress, 10% Volatility Penalty.
    
    Args:
        predicted_yield (float): The XGBoost-predicted yield (Y_pred).
        historical_avg_yield (float): The farm's long-term average yield (Y_avg).
        historical_yield_cv (float): The Coefficient of Variation (CV) of historical yields (volatility).
        ndvi_z_score (float): The real-time Z-score of current NDVI vs. historical trend (stress).
        base_score (int): The neutral starting score (default 50).
        
    Returns:
        Dict[str, float]: Dictionary containing the Final_DYRS and points breakdown.
    """
    
    # 1. YIELD ACCURACY INDEX (60% Weight)
    # Measures how confident we are that the predicted yield meets the benchmark.
    yield_dev_pct = (predicted_yield - historical_avg_yield) / historical_avg_yield
    
    # Scale: +/- 20% deviation is the max allowed boost/penalty (max +/- 60 points)
    # 0.20 * 300 = 60
    yield_accuracy_score = np.clip(yield_dev_pct, -0.2, 0.2) * 300 
    
    # 2. ANOMALY STRESS FACTOR (30% Weight - Dynamic/Real-Time)
    # Penalizes the score based on real-time stress alerts (NDVI Z-Score).
    # Critical thresholds: Z-Score <= -2.0 is Severe Stress. Z-Score <= -1.0 is Minor Stress.
    if ndvi_z_score <= -2.0:
        anomaly_penalty = 30.0 # Max Penalty
    elif ndvi_z_score <= -1.0:
        anomaly_penalty = 15.0 # Minor Penalty
    else:
        anomaly_penalty = 0.0
        
    # 3. HISTORICAL VOLATILITY PENALTY (10% Weight)
    # Penalizes farms with historically erratic yields (high CV).
    # Scaling Factor: 25. Max penalty for a CV of 0.40 is 10 points (0.40 * 25).
    volatility_penalty = historical_yield_cv * 25
    
    # 4. FINAL DYRS CALCULATION
    # DYRS = Base + Yield_Score - Anomaly_Penalty - Volatility_Penalty
    dyrs = base_score + yield_accuracy_score - anomaly_penalty - volatility_penalty
    
    # Final Clipping (0-100)
    final_dyrs = np.clip(dyrs, 0, 100)
    
    return {
        'Yield_Index_Points': float(yield_accuracy_score),
        'Anomaly_Penalty': float(anomaly_penalty),
        'Volatility_Penalty': float(volatility_penalty),
        'Final_DYRS': float(final_dyrs)
    }

# --- HELPER FUNCTION FOR DASHBOARD SCORING (For later use) ---

def score_to_risk_level(score: float) -> str:
    """Converts the DYRS score into a simple risk level."""
    if score >= 75:
        return 'LOW RISK'
    elif score >= 50:
        return 'MODERATE RISK'
    else:
        return 'HIGH RISK'

if __name__ == '__main__':
    # Simple test case: A healthy farm with a good prediction.
    test_score = calculate_full_dyrs(
        predicted_yield=6000,
        historical_avg_yield=5000,
        historical_yield_cv=0.10,
        ndvi_z_score=-0.5 
    )
    print("--- Test Case Output ---")
    print(f"Predicted Yield: 6000 | Avg Yield: 5000 (20% better)")
    print(f"Yield Index: {test_score['Yield_Index_Points']:.1f} (+60 points)")
    print(f"Anomaly Penalty: {test_score['Anomaly_Penalty']:.1f} (No Stress)")
    print(f"Volatility Penalty: {test_score['Volatility_Penalty']:.1f} (Low Volatility)")
    print(f"Final DYRS: {test_score['Final_DYRS']:.1f}") # Expected: 50 + 60 - 0 - 2.5 = 100 (Capped)