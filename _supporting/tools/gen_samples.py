# _supporting/tools/gen_samples.py
from __future__ import annotations

import os
from datetime import UTC, datetime, timedelta

import numpy as np
import pandas as pd

ROOT = "_supporting/data/samples"
os.makedirs(ROOT, exist_ok=True)

# --- config ---
start = datetime.now(UTC) - timedelta(days=200)
days = 180  # >= min_history_days (120) so backtest runs
stores = [1]
skus = [101, 102]  # two SKUs
rng = np.random.default_rng(42)

# --- POS ---
rows = []
for store_id in stores:
    for sku_id in skus:
        base = 10 if sku_id == 101 else 6
        for d in range(days):
            ts = start + timedelta(days=d)
            # weekly seasonality + noise
            weekday = ts.weekday()
            seasonal = 1.2 if weekday in (4,5) else 0.9  # Fri/Sat bump
            promo_flag = rng.random() < 0.1
            price = 3.49 if sku_id == 101 else 2.29
            price = price * (0.9 if promo_flag else 1.0)
            qty = max(0, rng.normal(base * seasonal * (1.15 if promo_flag else 1.0), 1.5))
            stock_out_flag = False
            rows.append([store_id, sku_id, ts.isoformat(), round(qty, 2), round(price, 2), bool(promo_flag), stock_out_flag])

pos = pd.DataFrame(rows, columns=["store_id","sku_id","ts","qty","price","promo_flag","stock_out_flag"])
pos.to_csv(f"{ROOT}/pos.csv", index=False)

# --- Weather ---
wrows = []
for store_id in stores:
    for d in range(days):
        ts = start + timedelta(days=d)
        temp_c = 18 + 10*np.sin(2*np.pi*d/365) + rng.normal(0, 2)
        precip_mm = max(0, rng.normal(1.2, 1.0))
        is_holiday = (ts.month, ts.day) in {(1,1), (7,4), (12,25)}
        event_id = ""  # blank ok
        wrows.append([store_id, ts.isoformat(), round(temp_c,2), round(precip_mm,2), bool(is_holiday), event_id])

weather = pd.DataFrame(wrows, columns=["store_id","ts","temp_c","precip_mm","is_holiday","event_id"])
weather.to_csv(f"{ROOT}/weather.csv", index=False)

# --- SKU Ref ---
sku_ref = pd.DataFrame([
    [1, 101, "Beverages", "BrandA", "500ml", 1.20],
    [1, 102, "Beverages", "BrandB", "330ml", 0.80],
], columns=["store_id","sku_id","category","brand","size","cost"])
sku_ref.to_csv(f"{ROOT}/sku_ref.csv", index=False)

print(f"Wrote samples to {ROOT}")
