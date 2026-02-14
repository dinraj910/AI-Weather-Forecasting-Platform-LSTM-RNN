
import pandas as pd
import numpy as np
import joblib
from app.config import Config

class PreprocessingService:
    _instance = None
    _scaler = None
    _data = None
    _target_index = 1 # T (degC) is typically index 1 in Jena dataset

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = PreprocessingService()
        return cls._instance

    def __init__(self):
        self.load_scaler()
        self.load_recent_data()

    def load_scaler(self):
        try:
            self._scaler = joblib.load(Config.SCALER_PATH)
            print("Scaler loaded successfully.")
        except Exception as e:
            print(f"Error loading scaler: {e}")
            self._scaler = None

    def load_recent_data(self):
        """Loads the most recent data for initial dashboard state."""
        try:
            # Prefer recent buffer if available for speed
            if os.path.exists(Config.RECENT_DATA_PATH):
                self._data = pd.read_csv(Config.RECENT_DATA_PATH, index_col=0, parse_dates=True)
            else:
                self._data = pd.read_csv(Config.DATASET_PATH, index_col='Date Time', parse_dates=True) # Fallback to full
                self._data = self._data.resample('1H').mean().interpolate(method='time').dropna().tail(1000)
            print(f"Loaded {len(self._data)} rows of recent data.")
        except Exception as e:
            print(f"Error loading data: {e}")
            self._data = pd.DataFrame()

    def get_recent_data(self, window_size=72):
         """Returns the last `window_size` scaled data points for prediction."""
         if self._data.empty:
             return None
         
         raw_tail = self._data.tail(window_size)
         if len(raw_tail) < window_size:
             return None # Not enough data
             
         scaled_tail = self._scaler.transform(raw_tail)
         return np.array([scaled_tail]) # Shape (1, window_size, features)

    def inverse_transform_prediction(self, prediction, is_multivariate=False):
        """
        Inverse transforms prediction.
        
        Args:
            prediction: Numpy array of shape (steps, features) or (steps, 1)
            is_multivariate: Boolean
        
        Returns:
            Inverse transformed array
        """
        if self._scaler is None:
            return prediction

        if is_multivariate:
            # Prediction has shape (n_samples, n_features) matching scaler
            return self._scaler.inverse_transform(prediction)
        
        else:
            # Manual inverse for single target (T degC)
            # Notebook logic: y * (max - min) + min
            # Or use scaler.scale_ and scaler.min_
            
            # scaler.data_min_ is the min of the data
            # scaler.data_max_ is the max of the data
            # range = data_max_ - data_min_
            
            temp_min = self._scaler.data_min_[self._target_index]
            temp_max = self._scaler.data_max_[self._target_index]
            
            # Ensure prediction is 1D or reshape if needed
            pred_flat = prediction.flatten()
            return pred_flat * (temp_max - temp_min) + temp_min

    def get_data_for_charts(self, hours=120): # 5 days
        """Returns raw historical data for plotting."""
        if self._data.empty:
            return [], [], []
        
        tail = self._data.tail(hours)
        return tail.index.tolist(), tail['T (degC)'].values.tolist(), tail.to_dict('records')

