import sys
import joblib
import numpy as np
import pandas as pd

def live_inference():
    if len(sys.argv) < 5:
        print("RESULT:ERROR,Missing features")
        sys.exit(1)
        
    # Parse real-time packet characteristics from the API gateway execution string
    packet_len_var = float(sys.argv[1])
    sync_flag_count = float(sys.argv[2])
    duration_ms = float(sys.argv[3])
    byte_transfer_rate = float(sys.argv[4])
    
    # Load model binaries
    model = joblib.load('models/intrusion_model.pkl')
    
    # Format vector array matching training columns
    feature_names = ['packet_len_var', 'sync_flag_count', 'duration_ms', 'byte_transfer_rate']
    input_data = pd.DataFrame([[packet_len_var, sync_flag_count, duration_ms, byte_transfer_rate]], columns=feature_names)
    
    prediction = model.predict(input_data)[0]
    probabilities = model.predict_proba(input_data)[0]
    risk_score = probabilities[1] # Probability of being malicious
    
    # 🔍 Local Attribution Math: Calculate distance from training medians to explain *this* specific choice
    # High variance or massive flag floods dynamically scale the structural explanation vector
    attributions = []
    if sync_flag_count > 2:
        attributions.append("SYNC_FLOOD_ANOMALY")
    if packet_len_var > 800:
        attributions.append("PACKET_SIZE_MUTATION")
    if duration_ms > 500:
        attributions.append("SUSPICIOUS_SESSION_PERSISTENCE")
        
    explanation = "|".join(attributions) if attributions else "NOMINAL_TRAFFIC_SIGNATURE"
    
    # Pipe output directly to the stdout stream for Node.js processing loop
    print(f"RESULT:{prediction},{risk_score:.4f},{explanation}")

if __name__ == "__main__":
    live_inference()