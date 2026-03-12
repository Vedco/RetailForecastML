from fastapi import FastAPI, Request
from pydantic import BaseModel
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
from starlette.responses import Response
import joblib
import pandas as pd
import os
import time
from datetime import datetime

# 👇 Optional: Pull latest model from DVC if you have that setup
try:
    from src.api.utils import pull_latest_model
    pull_latest_model()
except Exception as e:
    print(f"⚠️ Warning: Could not pull model from DVC. Using local copy. Error: {e}")

app = FastAPI(title="Retail Demand Forecast API", version="1.0")

# === 📊 Metrics Setup ===
REQUEST_COUNT = Counter("request_count_total", "Total number of API requests")
PREDICTION_COUNT = Counter("prediction_count_total", "Number of predictions made")
REQUEST_LATENCY = Histogram("request_latency_seconds", "Request latency in seconds")

# === 🧠 Load Model ===
MODEL_PATH = os.getenv("MODEL_PATH", "models/model.pkl")
model = joblib.load(MODEL_PATH)
print("✅ Model loaded successfully from", MODEL_PATH)

# === 📦 Data Model ===
class ForecastRequest(BaseModel):
    store: int
    item: int
    date: str  # Date is accepted but not used in prediction

# === ⚙️ Middleware for Metrics ===
@app.middleware("http")
async def add_metrics(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    REQUEST_LATENCY.observe(process_time)
    REQUEST_COUNT.inc()
    return response

# === 📈 Metrics Endpoint ===
@app.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)

# === 🚀 Root Endpoint ===
@app.get("/")
def root():
    return {"message": "Retail Demand Forecast API is running 🚀"}

# === 🔮 Prediction Endpoint ===
@app.post("/predict")
def predict(request: ForecastRequest):
    # Only the features used during training: store and item
    data_dict = {
        "store": request.store,
        "item": request.item,
    }

    input_df = pd.DataFrame([data_dict])
    prediction = model.predict(input_df)[0]
    PREDICTION_COUNT.inc()

    return {"predicted_sales": float(prediction)}
