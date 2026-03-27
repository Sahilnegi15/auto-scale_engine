import time
from app.predictor import predict_future_load
from app.workers import scale_workers


current_servers = 3
last_scaled_time = 0
COOLDOWN = 10  # seconds

def decide_scaling(metrics):
    global current_servers, last_scaled_time

    current_time = time.time()

    # ⛔ Cooldown check
    if current_time - last_scaled_time < COOLDOWN:
        return {
            "action": "cooldown",
            "servers": current_servers,
            "message": "Waiting before next scaling decision"
        }

    predicted_rps = predict_future_load(metrics)

    action = "no_change"

    if predicted_rps > 1500:
        current_servers += 1
        scale_workers(current_servers)
        action = "scale_up"
        last_scaled_time = current_time

    elif predicted_rps < 500 and current_servers > 1:
        current_servers -= 1
        scale_workers(current_servers)
        action = "scale_down"
        last_scaled_time = current_time

    return {
        "action": action,
        "servers": current_servers,
        "predicted_rps": predicted_rps,
        "metrics": metrics
    }