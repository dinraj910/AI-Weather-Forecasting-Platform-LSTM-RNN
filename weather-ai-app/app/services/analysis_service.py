
import numpy as np
import pandas as pd
from sklearn.metrics import mean_squared_error, mean_absolute_error

class AnalysisService:
    @staticmethod
    def calculate_metrics(y_true, y_pred):
        """Calculates RMSE and MAE."""
        if len(y_true) == 0 or len(y_pred) == 0:
            return 0.0, 0.0
        
        mse = mean_squared_error(y_true, y_pred)
        rmse = np.sqrt(mse)
        mae = mean_absolute_error(y_true, y_pred)
        return rmse, mae

    @staticmethod
    def analyze_trend(recent_temps):
        """Analyzes temperature trend (Rising/Falling/Stable)."""
        if len(recent_temps) < 2:
            return "Stable"
        
        # Simple slope of last few points
        slope = recent_temps[-1] - recent_temps[0]
        if slope > 0.5:
            return "Rising"
        elif slope < -0.5:
            return "Falling"
        return "Stable"

    @staticmethod
    def get_forecast_confidence(predictions):
        """
        Estimates forecast confidence band.
        (Placeholder: Uses residual std dev from training/validation if available, 
         or simple heuristic based on prediction variance).
        """
        # Heuristic: 95% confidence interval +/- 2 degree (example)
        # In production, this should come from model uncertainty or error distribution (residuals).
        std_dev = 1.5 # derived from notebook MAE ~0.67 -> RMSE ~0.89. 2*RMSE approx 1.8.
        
        upper = [p + std_dev for p in predictions]
        lower = [p - std_dev for p in predictions]
        return upper, lower

