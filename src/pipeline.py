import os
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler

# Ensure output directories exist
os.makedirs('data/raw', exist_ok=True)
os.makedirs('data/processed', exist_ok=True)

def generate_mock_telemetry_data():
    print("📥 Extracting: Generating mock raw telemetry data...")
    np.random.seed(42)
    
    # Simulate 500 server status log snapshots
    rows = 500
    data = {
        'timestamp': pd.date_range(start='2026-07-16', periods=rows, freq='min'),
        'cpu_usage_pct': np.random.uniform(20.0, 95.0, size=rows),
        'memory_usage_pct': np.random.uniform(40.0, 90.0, size=rows),
        'network_latency_ms': np.random.exponential(scale=20.0, size=rows),
        # Intentionally inject some missing values (NaNs) to simulate real-world log corruption
        'error_count': np.random.choice([0, 1, 2, np.nan], size=rows, p=[0.8, 0.1, 0.05, 0.05])
    }
    
    df = pd.DataFrame(data)
    df.to_csv('data/raw/raw_telemetry.csv', index=False)
    print("💾 Raw data successfully saved to data/raw/raw_telemetry.csv")

def run_transform_and_load():
    print("⚙️ Transforming: Processing raw system logs...")
    
    # Load the raw data
    df = pd.read_csv('data/raw/raw_telemetry.csv')
    
    # 1. Handle Missing Data: Fill corrupted error counts with 0
    df['error_count'] = df['error_count'].fillna(0)
    
    # 2. Feature Engineering: Create a rolling average for CPU spikes
    df['cpu_rolling_avg'] = df['cpu_usage_pct'].rolling(window=5, min_periods=1).mean()
    
    # 3. Scaling: Normalize numerical columns between 0 and 1 for the ML model
    features_to_scale = ['cpu_usage_pct', 'memory_usage_pct', 'network_latency_ms', 'cpu_rolling_avg']
    scaler = MinMaxScaler()
    df[features_to_scale] = scaler.fit_transform(df[features_to_scale])
    
    # Drop timestamp for pure mathematical modeling, keeping target/features clean
    processed_df = df.drop(columns=['timestamp'])
    
    print("📤 Loading: Depositing clean data into the data warehouse layer...")
    processed_df.to_csv('data/processed/clean_telemetry.csv', index=False)
    print("✅ Pipeline executed successfully! Clean data saved to data/processed/clean_telemetry.csv")

if __name__ == "__main__":
    generate_mock_telemetry_data()
    run_transform_and_load()