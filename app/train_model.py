import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
import joblib

# simulate data
data = []

for i in range(1000):
    cpu = np.random.randint(10, 100)
    rps = np.random.randint(50, 2000)
    
    # simulate future load (simple relation)
    future_rps = rps + np.random.randint(-200, 500)
    
    data.append([cpu, rps, future_rps])

df = pd.DataFrame(data, columns=["cpu", "rps", "future_rps"])

X = df[["cpu", "rps"]]
y = df["future_rps"]

model = LinearRegression()
model.fit(X, y)

# save model
joblib.dump(model, "app/model.pkl")

print("Model trained and saved 🚀")