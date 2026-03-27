import random

history = []

def get_metrics():
    global history

    new_data = {
        "cpu": random.randint(10, 100),
        "memory": random.randint(20, 100),
        "requests_per_sec": random.randint(50, 2000)
    }

    history.append(new_data)

    # keep last 5 values
    if len(history) > 5:
        history.pop(0)

    # calculate average
    avg_cpu = sum(x["cpu"] for x in history) / len(history)
    avg_rps = sum(x["requests_per_sec"] for x in history) / len(history)

    return {
        "cpu": int(avg_cpu),
        "memory": new_data["memory"],
        "requests_per_sec": int(avg_rps)
    }