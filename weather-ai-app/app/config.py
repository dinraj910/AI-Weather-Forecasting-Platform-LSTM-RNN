
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev_secret_key'
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    MODEL_DIR = os.path.join(BASE_DIR, 'models')
    DATA_DIR = os.path.join(BASE_DIR, 'data')
    
    SCALER_PATH = os.path.join(MODEL_DIR, 'scaler.pkl')
    LSTM_MODEL_PATH = os.path.join(MODEL_DIR, 'weather_lstm_model.h5')
    MULTIVARIATE_MODEL_PATH = os.path.join(MODEL_DIR, 'multivariate_dynamic.h5')
    
    DATASET_PATH = os.path.join(DATA_DIR, 'jena_climate_2009_2016.csv')
    RECENT_DATA_PATH = os.path.join(DATA_DIR, 'recent_hourly.csv')

    WINDOW_SIZE = 72
    PREDICTION_STEPS_24H = 24
    PREDICTION_STEPS_7D = 168
