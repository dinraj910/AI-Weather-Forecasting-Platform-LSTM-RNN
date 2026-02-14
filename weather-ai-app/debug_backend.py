
import os
import sys
import pandas as pd
from app.config import Config
from app.services.preprocessing_service import PreprocessingService
from app.services.forecasting_service import ForecastingService

# Force unbuffered output
sys.stdout.reconfigure(line_buffering=True)

print(f"Current CWD: {os.getcwd()}")
print(f"Config RECENT_DATA_PATH: {Config.RECENT_DATA_PATH}")
print(f"File exists? {os.path.exists(Config.RECENT_DATA_PATH)}")

try:
    print("Testing direct pandas read...")
    df = pd.read_csv(Config.RECENT_DATA_PATH, index_col=0, parse_dates=True)
    print(f"Direct read shape: {df.shape}")
    print(f"Direct read head index: {df.index[0]}")
except Exception as e:
    print(f"Direct read failed: {e}")

print("Initializing PreprocessingService...")
service = PreprocessingService.get_instance()
if service._data is None or service._data.empty:
    print("Preproc Service data is EMPTY")
else:
    print(f"Preproc Service data shape: {service._data.shape}")

print("Initializing ForecastingService...")
forecast = ForecastingService.get_instance()

print("Testing Prediction...")
pred = forecast.predict_next_hour('single')
print(f"Prediction result: {pred}")
