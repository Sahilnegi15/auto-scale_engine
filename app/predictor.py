import joblib
import numpy as np

model = joblib.load("app/model.pkl")

def predict_future_load(metrics):
    cpu = metrics["cpu"]
    rps = metrics["requests_per_sec"]

    prediction = model.predict([[cpu, rps]])

    return int(prediction[0])