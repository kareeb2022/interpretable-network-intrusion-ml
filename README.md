# Interpretable Network Intrusion & Anomaly Classification Engine

A high-performance Machine Learning pipeline designed to classify malicious network packets (such as intrusion or flooding attempts) using real-time traffic metric streams. Built with an emphasis on **Model Interpretability and MLOps operational guardrails**, this pipeline processes traffic arrays and extracts feature signatures to explain decision matrices.

## 🏗️ Core Architecture Layout

- **`src/network_etl.py`** -> Data simulation engine that models multi-metric network flows (packet length variance, sync flags, duration, and transfer rates) into data matrices.
- **`src/train_network.py`** -> Training suite that optimizes a Gradient Boosting Classifier, enforces performance validation loops, and prints structural feature weight charts.
- **`src/predict_network.py`** -> Inline inference layer that parses network metrics and exposes explainable risk telemetry (e.g., separating standard flows from threat flags).
- **`src/network_api.py`** -> Lightweight, highly stable native service acting as the gateway for evaluating runtime packet streams.

## 🚀 Getting Started

### Prerequisites
Install the core data science and machine learning dependencies:
```bash
pip install pandas numpy scikit-learn joblib
