import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.metrics import roc_auc_score
import joblib
import os
import sys

def train_network_pipeline():
    print("🚀 Phase 2: Launching Network Security Optimization Engine...")
    
    if not os.path.exists('data/network_traffic.csv'):
        print("❌ Error: Missing 'data/network_traffic.csv'. Run the ETL script first.")
        sys.exit(1)
        
    df = pd.read_csv('data/network_traffic.csv')
    X = df.drop(columns=['is_malicious'])
    y = df['is_malicious']
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=101)
    
    # Train the Gradient Boosting structure
    model = GradientBoostingClassifier(n_estimators=80, learning_rate=0.1, max_depth=4, random_state=101)
    model.fit(X_train, y_train)
    
    # Performance Evaluation via ROC-AUC Vector Mapping
    probs = model.predict_proba(X_test)[:, 1]
    auc_score = roc_auc_score(y_test, probs)
    print(f"📊 Cybersecurity Validation Metric -> ROC-AUC: {auc_score:.4f}")
    
    # MLOps Quality Guardrail
    MINIMUM_AUC_THRESHOLD = 0.85
    if auc_score < MINIMUM_AUC_THRESHOLD:
        print(f"🛑 CRITICAL GUARDRAIL TRIGGERED: ROC-AUC ({auc_score:.4f}) below safe threshold ({MINIMUM_AUC_THRESHOLD}). Aborting binary serialization.")
        sys.exit(1)
    
    # Thesis-Level Model Interpretability Extraction
    print("\n🔍 Model Interpretability Diagnostics (Feature Importances):")
    for feature, importance in zip(X.columns, model.feature_importances_):
        print(f" ──> {feature}: {importance:.4f}")
        
    os.makedirs('models', exist_ok=True)
    joblib.dump(model, 'models/intrusion_model.pkl')
    print("\n💾 Guardrail Passed! 'models/intrusion_model.pkl' written cleanly to disk.")

if __name__ == "__main__":
    train_network_pipeline()