import os
import pandas as pd
import numpy as np

def generate_network_data():
    print("📥 Phase 1: Initiating Network Traffic Extraction (ETL) Pipeline...")
    np.random.seed(101)
    sample_size = 1500
    
    # Simulating features: packet_length_var, sync_flags, duration_ms, byte_rate
    duration = np.random.exponential(scale=200, size=sample_size) # Normal traffic is fast, attacks can linger
    packet_length_var = np.random.normal(loc=500, scale=150, size=sample_size).clip(50, 2000)
    sync_flags = np.random.poisson(lam=1.2, size=sample_size)
    byte_rate = np.random.uniform(100, 50000, size=sample_size)
    
    # Intrusion Logic: Massive packet length variance + flooded sync flags = highly likely attack
    intrusion_prob = 1 / (1 + np.exp(-(-3.5 + 0.003*packet_length_var + 1.2*sync_flags + 0.001*duration)))
    is_intrusion = (np.random.uniform(0, 1, size=sample_size) < intrusion_prob).astype(int)
    
    df = pd.DataFrame({
        'packet_len_var': np.round(packet_length_var, 2),
        'sync_flag_count': sync_flags,
        'duration_ms': np.round(duration, 2),
        'byte_transfer_rate': np.round(byte_rate, 2),
        'is_malicious': is_intrusion
    })
    
    os.makedirs('data', exist_ok=True)
    df.to_csv('data/network_traffic.csv', index=False)
    print(f"✅ Network ETL Complete. Formatted {sample_size} packet streams into 'data/network_traffic.csv'.")

if __name__ == "__main__":
    generate_network_data()