from fastapi import FastAPI
from pydantic import BaseModel
from typing import Dict

app = FastAPI(title="MicroLineage AI")

class ForecastRequest(BaseModel):
    store_id: str
    sku_id: str
    horizon_days: int = 14
    context: Dict = {}

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/forecast")
def forecast(req: ForecastRequest):
    # TODO: wire real model(s)
    baseline = [12, 13, 12, 14, 15, 14, 13, 12, 12, 13, 14, 13, 12, 11]
    return {
        "store_id": req.store_id,
        "sku_id": req.sku_id,
        "horizon_days": req.horizon_days,
        "daily_units": baseline[: req.horizon_days]
    }
