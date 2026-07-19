import sys
import json
import os
import joblib
import numpy as np

def run_inference():
    # Make sure we got our 4 input metrics from the Node server arguments
    if len(sys.argv) < 5:
        print(json.dumps({"error": "Insufficient parameters passed for model feature tracking arrays."}))
        sys.exit(1)

    # Load features from CLI arguments
    cpu = float(sys.argv[1])
    mem = float(sys.argv[2])
    net = float(sys.argv[3])
    roll = float(sys.argv[4])

    # 🛠️ FIXED: Safely resolve the absolute workspace root relative to this script's location
    # Since this script lives in /app/src/ (or /workspace/src/), going up one level gets us to /app/
    script_dir = os.path.dirname(os.path.abspath(__file__))
    workspace_root = os.path.abspath(os.path.join(script_dir, ".."))
    model_path = os.path.join(workspace_root, 'models', 'anomaly_detector.pkl')
    
    if not os.path.exists(model_path):
        print(json.dumps({"error": f"Model artifact not found at {model_path}."}))
        sys.exit(1)

    model = joblib.load(model_path)
    
    # Reshape input features into standard 2D array matrix for scikit-learn
    features = np.array([[cpu, mem, net, roll]])
    
    # Generate prediction (0 or 1) and raw probability scores
    prediction = int(model.predict(features)[0])
    probability = float(model.predict_proba(features)[0][1])

    # Echo out back to stdout for Node.js child_process extraction layer
    print(json.dumps({
        "prediction": prediction,
        "probability": round(probability, 4)
    }))

if __name__ == "__main__":
    run_inference()