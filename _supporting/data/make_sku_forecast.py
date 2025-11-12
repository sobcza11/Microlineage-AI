from pathlib import Path
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Resolve repo root from this file
HERE = Path(__file__).resolve()
REPO = HERE.parents[2]  # .../Microlineage-AI
DATA = REPO / "_supporting" / "data"
RAW = DATA / "raw"
PROCESSED = DATA / "processed"
PROCESSED.mkdir(parents=True, exist_ok=True)

out_path = PROCESSED / "sku_forecast.csv"

# Try to build from any plausible raw CSVs; otherwise synthesize a tiny sample.
candidates = list(RAW.glob("*.csv"))

def synthesize_sample(n_skus=6, days=14, seed=42):
    rng = np.random.default_rng(seed)
    start = datetime.today().date() - timedelta(days=days)
    rows = []
    for i in range(n_skus):
        sku = f"SKU-{i+1:03d}"
        base_price = rng.uniform(1.5, 6.0)
        cost = base_price * rng.uniform(0.5, 0.8)
        for d in range(days):
            date = start + timedelta(days=d)
            forecast = max(0, rng.normal(30, 8))
            actual = max(0, forecast + rng.normal(0, 5))
            rows.append([sku, str(date), round(cost, 2), round(base_price, 2), round(forecast, 2), round(actual, 2)])
    df = pd.DataFrame(rows, columns=["sku", "date", "cost", "price", "forecast", "actual"])
    return df

df_out = None

# Heuristic: if you already have something like forecasts or costs in RAW, try to merge.
try:
    # Look for any file that already has sku+date+forecast (or actual) columns
    useful = []
    for p in candidates:
        try:
            df = pd.read_csv(p)
            cols = {c.lower() for c in df.columns}
            if {"sku", "date"} <= cols and (("forecast" in cols) or ("actual" in cols)):
                useful.append((p, df))
        except Exception:
            pass

    if useful:
        # Take the first useful as base, and fill missing columns with defaults
        _, base = useful[0]
        base.columns = [c.lower() for c in base.columns]
        if "forecast" not in base.columns:
            base["forecast"] = base.get("actual", 20)
        if "actual" not in base.columns:
            base["actual"] = base["forecast"]
        if "price" not in base.columns:
            base["price"] = 3.99
        if "cost" not in base.columns:
            base["cost"] = base["price"] * 0.65
        keep = ["sku", "date", "cost", "price", "forecast", "actual"]
        df_out = base[keep].copy()
except Exception:
    df_out = None

if df_out is None:
    df_out = synthesize_sample()

df_out.to_csv(out_path, index=False)
print(f"✅ Wrote {out_path.relative_to(REPO)} with {len(df_out)} rows.")
