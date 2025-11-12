from __future__ import annotations

import argparse
import json
import os
from dataclasses import dataclass

import numpy as np
import pandas as pd
import yaml

from _supporting.src.models.baselines.naive import Naive
from _supporting.src.models.baselines.seasonal_naive import SeasonalNaive


# ---------- metrics ----------
def smape(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    y_true = np.asarray(y_true, dtype=float)
    y_pred = np.asarray(y_pred, dtype=float)
    denom = (np.abs(y_true) + np.abs(y_pred))
    denom[denom == 0] = 1.0
    return float(np.mean(2.0 * np.abs(y_pred - y_true) / denom) * 100.0)

def rmse(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    y_true = np.asarray(y_true, dtype=float)
    y_pred = np.asarray(y_pred, dtype=float)
    return float(np.sqrt(np.mean((y_pred - y_true) ** 2)))


# ---------- config ----------
@dataclass
class BTConfig:
    horizon: int = 14
    folds: int = 4
    min_history_days: int = 120
    agg: str = "D"   # daily
    season: int = 7  # for SeasonalNaive

    @classmethod
    def from_yaml(cls, path: str) -> BTConfig:
        with open(path, encoding="utf-8") as f:
            raw = yaml.safe_load(f) or {}
        return cls(**{k: v for k, v in raw.items() if k in cls.__annotations__})


# ---------- data utils ----------
def load_pos(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)
    # expected columns: store_id, sku_id, ts, qty, price, promo_flag, stock_out_flag
    df["ts"] = pd.to_datetime(df["ts"], utc=True, errors="coerce")
    # keep only what's needed for demand
    return df[["store_id", "sku_id", "ts", "qty"]].dropna()

def make_series(df: pd.DataFrame, store_id: int, sku_id: int, agg: str) -> pd.Series:
    sdf = (df[(df["store_id"] == store_id) & (df["sku_id"] == sku_id)]
             .set_index("ts")
             .sort_index())
    # aggregate quantity per day, fill missing days with 0
    y = (sdf["qty"]
         .resample(agg)
         .sum()
         .asfreq(agg, fill_value=0.0))
    y.name = "qty"
    return y


# ---------- backtest core ----------
def rolling_splits(y: pd.Series, cfg: BTConfig) -> list[tuple[pd.DatetimeIndex, pd.DatetimeIndex]]:
    """Return list of (train_index, test_index) for expanding window + fixed horizon."""
    if len(y) < cfg.min_history_days:
        return []
    splits: list[tuple[pd.DatetimeIndex, pd.DatetimeIndex]] = []
    train_end_idxs = np.linspace(cfg.min_history_days, len(y) - cfg.horizon, num=cfg.folds, dtype=int)
    for tei in train_end_idxs:
        train_idx = y.index[:tei]
        test_idx = y.index[tei: tei + cfg.horizon]
        if len(test_idx) == cfg.horizon:
            splits.append((train_idx, test_idx))
    return splits


def run_backtest(y: pd.Series, cfg: BTConfig, out_dir: str, key: str) -> dict:
    models = [
        Naive(),
        SeasonalNaive(season=cfg.season),
    ]
    os.makedirs(out_dir, exist_ok=True)

    results = {
        "series_len": int(len(y)),
        "folds": [],
        "models": {m.name: {"rmse": [], "smape": []} for m in models},
    }

    splits = rolling_splits(y, cfg)
    if not splits:
        return {**results, "note": "not enough history for backtesting"}

    for fold_id, (tr_idx, ts_idx) in enumerate(splits, start=1):
        y_tr = y.loc[tr_idx]
        y_ts = y.loc[ts_idx]
        horizon = len(y_ts)
        fold_meta = {"fold": fold_id, "train_end": str(tr_idx[-1]), "test_start": str(ts_idx[0])}
        results["folds"].append(fold_meta)

        for m in models:
            m.fit(y_tr)
            fcst = m.forecast(horizon)
            fold_rmse = rmse(y_ts.values, fcst)
            fold_smape = smape(y_ts.values, fcst)
            results["models"][m.name]["rmse"].append(fold_rmse)
            results["models"][m.name]["smape"].append(fold_smape)

            # persist predictions per fold for inspection
            pred_df = pd.DataFrame({
                "ts": y_ts.index,
                "y_true": y_ts.values,
                "y_pred": fcst,
                "model": m.name,
                "fold": fold_id,
            })
            pred_path = os.path.join(out_dir, f"{key}__{m.name}__fold{fold_id}.csv")
            pred_df.to_csv(pred_path, index=False)

    # aggregate
    for name, d in results["models"].items():
        d["rmse_mean"] = float(np.mean(d["rmse"])) if d["rmse"] else None
        d["smape_mean"] = float(np.mean(d["smape"])) if d["smape"] else None
    return results


# ---------- CLI ----------
def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--pos", required=True, help="path to POS csv")
    ap.add_argument("--config", required=True, help="backtest yaml")
    ap.add_argument("--out_json", required=True, help="summary json path")
    ap.add_argument("--out_preds_dir", required=True, help="dir for per-fold predictions")
    ap.add_argument("--limit_pairs", type=int, default=20, help="max (store,sku) pairs to run (for speed)")
    args = ap.parse_args()

    cfg = BTConfig.from_yaml(args.config)
    df = load_pos(args.pos)

    # compute pairs (store, sku) in stable order
    pairs = (df[["store_id", "sku_id"]]
             .drop_duplicates()
             .sort_values(["store_id", "sku_id"])
             .itertuples(index=False, name=None))
    pairs = list(pairs)[: args.limit_pairs]

    summary = {
        "config": cfg.__dict__,
        "pairs": [],
    }

    for store_id, sku_id in pairs:
        key = f"store{store_id}_sku{sku_id}"
        y = make_series(df, store_id, sku_id, cfg.agg)
        res = run_backtest(y, cfg, args.out_preds_dir, key)
        summary["pairs"].append({"key": key, "store_id": int(store_id), "sku_id": int(sku_id), "result": res})

    os.makedirs(os.path.dirname(args.out_json), exist_ok=True)
    with open(args.out_json, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)
    print(f"Wrote backtest summary → {args.out_json}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
