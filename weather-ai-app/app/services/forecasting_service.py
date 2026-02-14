
import os
import numpy as np
import pandas as pd
import tensorflow as tf
from app.config import Config
from app.services.preprocessing_service import PreprocessingService

class ForecastingService:
    _instance = None
    _models = {}

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = ForecastingService()
        return cls._instance

    def __init__(self):
        self.load_models()
        self.preprocessing_service = PreprocessingService.get_instance()

    def load_models(self):
        try:
            print("Loading LSTM models...")
            # Load single-output model
            self._models['single'] = tf.keras.models.load_model(Config.LSTM_MODEL_PATH)
            # Load multivariate model
            self._models['multi'] = tf.keras.models.load_model(Config.MULTIVARIATE_MODEL_PATH)
            print("Models loaded successfully.")
        except Exception as e:
            print(f"Error loading models: {e}")

    def predict_next_hour(self, model_type='single'):
        """Predicts the next hour's temperature."""
        # Get recent 72h data
        input_data = self.preprocessing_service.get_recent_data(Config.WINDOW_SIZE)
        if input_data is None:
            return None
        
        model = self._models.get(model_type)
        if not model:
            return None

        prediction = model.predict(input_data)
        
        # Inverse transform
        if model_type == 'multi':
            # Prediction shape (1, 14) -> Inverse transform full
            return self.preprocessing_service.inverse_transform_prediction(prediction, is_multivariate=True)[0, 1] # Index 1 is Temp
        else:
            # Prediction shape (1, 1) -> Inverse transform single
            return self.preprocessing_service.inverse_transform_prediction(prediction, is_multivariate=False)

    def predict_sequence(self, steps, model_type='single'):
        """Recursive prediction for `steps` hours."""
        # Get recent data
        current_seq = self.preprocessing_service.get_recent_data(Config.WINDOW_SIZE) # (1, 72, 14)
        if current_seq is None:
            return []

        predictions = []
        model = self._models.get(model_type)
        
        if not model:
            return []

        # Loop for recursive prediction
        for _ in range(steps):
            # Predict next step
            pred = model.predict(current_seq) # (1, features) or (1, 1)

            if model_type == 'multi':
                # Multivariate: Feed the full prediction back
                # pred shape (1, 14)
                
                # Inverse for display
                inv_pred = self.preprocessing_service.inverse_transform_prediction(pred, is_multivariate=True)
                predictions.append(inv_pred[0, 1]) # Store Temp
                
                # Update sequence: shift left, append new
                new_step = pred.reshape(1, 1, -1) # (1, 1, 14)
                current_seq = np.concatenate([current_seq[:, 1:, :], new_step], axis=1)

            else:
                # Single output: We only get Temp back.
                # To recurse, we need the *other 13 features* for the next step.
                # Problem: Single output model only gives T. We can't update the full vector reliably without a multi-output model or assuming other features stay constant/trend.
                # Strategy: For single output recursion, we might assume persistence for other features OR just use the multivariate model for recursion logic but return single model's temp?
                # Actually, the user requirement says "Supports recursive multi-day forecasting" for the multivariate model.
                # For single model, it says "Predicts next-hour temperature". It might imply it's NOT intended for long recursive forecasts, or we use a naive approach (copy last features).
                # Let's use the multivariate model for the *sequence update* if available, but replace the Temp with the single model's prediction? No, that's complex.
                # Simple approach: If model is single, use repeat vector or stop specific logic.
                # However, the user wants "24-hour forecast" and "7-day forecast" with a toggle.
                # If they select "Single-output model", we must try.
                # We'll assume persistence for non-target features (copy last step's non-temp features).
                
                # Get last step from current sequence
                last_step_features = current_seq[:, -1, :] # (1, 14)
                
                # Construct new step
                new_step_features = last_step_features.copy()
                # Update Temp (Index 1) with prediction
                new_step_features[0, 1] = pred[0, 0] 
                
                # Inverse for display
                inv_pred = self.preprocessing_service.inverse_transform_prediction(pred, is_multivariate=False)
                predictions.append(inv_pred)
                
                # Reshape and append
                new_input = new_step_features.reshape(1, 1, -1)
                current_seq = np.concatenate([current_seq[:, 1:, :], new_input], axis=1)

        return predictions
