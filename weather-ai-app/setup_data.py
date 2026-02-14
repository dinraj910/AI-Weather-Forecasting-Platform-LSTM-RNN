
import os
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
import joblib

def setup_data():
    # Paths
    base_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(base_dir, 'data', 'jena_climate_2009_2016.csv')
    models_dir = os.path.join(base_dir, 'models')
    scaler_path = os.path.join(models_dir, 'scaler.pkl')

    print(f"Loading data from {data_path}...")
    df = pd.read_csv(data_path)

    # Date conversion
    print("Formatting dates...")
    df['Date Time'] = pd.to_datetime(df['Date Time'], format='%d.%m.%Y %H:%M:%S')
    df.set_index('Date Time', inplace=True)

    # Resample to hourly
    print("Resampling to hourly mean...")
    df_hourly = df.resample('1H').mean()

    # Handle missing values
    print("Interpolating missing values...")
    df_hourly = df_hourly.interpolate(method='time')
    df_hourly = df_hourly.dropna()

    # Train-test split (80/20)
    train_size = int(len(df_hourly) * 0.8)
    train_df = df_hourly.iloc[:train_size]
    
    # Fit scaler
    print("Fitting MinMaxScaler on training data...")
    scaler = MinMaxScaler()
    scaler.fit(train_df)

    # Save scaler
    print(f"Saving scaler to {scaler_path}...")
    if not os.path.exists(models_dir):
        os.makedirs(models_dir)
    joblib.dump(scaler, scaler_path)
    
    # Save a small buffer of recent data for quick app startup/demo if needed
    # (Optional, but good for performance)
    recent_path = os.path.join(base_dir, 'data', 'recent_hourly.csv')
    print(f"Saving recent data buffer to {recent_path}...")
    df_hourly.tail(1000).to_csv(recent_path)

    print("Setup complete.")

if __name__ == "__main__":
    setup_data()
