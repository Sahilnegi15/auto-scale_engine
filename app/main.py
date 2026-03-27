from fastapi import FastAPI
from app.metrics import get_metrics
from app.scaler import decide_scaling
from app.workers import start_workers, add_task
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def startup():
    start_workers(3)

@app.get("/")
def home():
    return {"message": "Auto Scaling Engine Running 🚀"}

@app.get("/metrics")
def metrics():
    return get_metrics()

@app.get("/scale")
def scale():
    metrics = get_metrics()
    decision = decide_scaling(metrics)
    return decision

@app.post("/generate-load")
def generate_load(n: int = 10):
    for i in range(n):
        add_task(f"task-{i}")
    return {"message": f"{n} tasks added"}