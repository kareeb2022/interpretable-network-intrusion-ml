import sys
import joblib
import pandas as pd
import numpy as np

def make_prediction():
    # Expecting: cpu_usage_pct, memory_usage_pct, network_latency_ms, cpu_rolling_avg
    if len(sys.argv) < 5:
        print("ERROR: Missing arguments")
        sys.exit(1)
        
    try:
        # Read the raw inputs forwarded from the web server
        inputs = [float(arg) for arg in sys.argv[1:5]]
        
        # Load our trained model binary
        model = joblib.load('models/anomaly_detector.pkl')
        
        # Format the data structural array for scikit-learn
        features = np.array([inputs])
        
        # Get live predictions
        prediction = model.predict(features)[0]
        probabilities = model.predict_proba(features)[0]
        risk_score = probabilities[1] # Probability of anomaly class (1)
        
        # Output result format so Node.js can read it easily
        print(f"RESULT:{prediction},{risk_score:.4f}")
        
    except Exception as e:
        print(f"ERROR: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    make_prediction()