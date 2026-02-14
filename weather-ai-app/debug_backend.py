
import os
import sys
import traceback

# Add current directory to path so we can import app
sys.path.append(os.getcwd())

try:
    print("Importing Config...")
    from app.config import Config
    print("Config imported.")

    print("Importing PreprocessingService...")
    from app.services.preprocessing_service import PreprocessingService
    print("PreprocessingService imported.")

    print("Initializing PreprocessingService...")
    service = PreprocessingService.get_instance()
    print("PreprocessingService initialized.")
    
    print("Checking data...")
    if service._data is None or service._data.empty:
        print("ERROR: Data is empty!")
    else:
        print(f"Data loaded: {len(service._data)} rows")
        print(f"Columns: {service._data.columns.tolist()}")
        print(f"Head index: {service._data.index[0]}")

    print("Checking scaler...")
    if service._scaler is None:
        print("ERROR: Scaler is None!")
    else:
        print("Scaler is loaded.")

    print("Importing ForecastingService...")
    from app.services.forecasting_service import ForecastingService
    print("ForecastingService imported.")

    print("Initializing ForecastingService...")
    forecast_service = ForecastingService.get_instance()
    print("ForecastingService initialized.")

    print("Testing predictions...")
    pred = forecast_service.predict_next_hour('single')
    print(f"Next hour prediction (single): {pred}")

    pred_multi = forecast_service.predict_next_hour('multi')
    print(f"Next hour prediction (multi): {pred_multi}")

    print("Debug complete.")

except Exception:
    traceback.print_exc()
