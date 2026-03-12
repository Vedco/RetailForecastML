import pandas as pd
import joblib, json
from xgboost import XGBRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error
import numpy as np
import os
from datetime import datetime
import random

# 1️⃣ Load new data
data_path = "data/processed/cleaned_data.csv"
df = pd.read_csv(data_path, parse_dates=['date'])

# 2️⃣ Feature prep (reuse logic)
X = df.drop(['sales', 'date'], axis=1)
y = df['sales']

# **Handle zero values in y**
epsilon = 1e-6  # Small constant to avoid division by zero
y = y.replace(0, epsilon)  # Replace 0's with epsilon (1e-6)

# 3️⃣ Randomize hyperparameters for model
n_estimators = random.randint(100, 500)  # Randomly choose n_estimators between 100 and 500
learning_rate = random.uniform(0.01, 0.3)  # Randomly choose learning rate between 0.01 and 0.3
max_depth = random.randint(3, 15)  # Randomly choose max_depth between 3 and 15


# 4️⃣ Train new model
model = XGBRegressor(
    n_estimators=n_estimators, 
    learning_rate=learning_rate, 
    max_depth=max_depth, 
    random_state=42
)
model.fit(X, y)

# 5️⃣ Evaluate (train performance only, for simplicity)
y_pred = model.predict(X)
mae = mean_absolute_error(y, y_pred)
rmse = np.sqrt(mean_squared_error(y, y_pred))

# MAPE calculation with epsilon added to avoid division by zero
mape = np.mean(np.abs((y - y_pred) / (y + epsilon))) * 100

metrics = {"mae": mae, "rmse": rmse, "mape": mape}

# 6️⃣ Save new artifacts
timestamp = datetime.now().strftime("%Y%m%d_%H%M")
model_path = "models/model.pkl"

joblib.dump(model, model_path)
json.dump(metrics, open("models/metrics.json", "w"), indent=2)

print("✅ Model retrained and saved:", model_path) 
print("📊 Metrics:", metrics)

# 7️⃣ Log retraining details
with open("logs/retrain_logs.log", "a") as f:
    f.write(f"{timestamp}: retrain completed with MAPE={mape:.2f}\n")
