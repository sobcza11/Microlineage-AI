from pathlib import Path
import numpy as np
import pandas as pd
from scipy.optimize import linprog
import mlflow  # <-- import before using

# ---------- paths ----------
HERE = Path(__file__).resolve()
REPO = HERE.parents[2]  # .../Microlineage-AI
DATA = REPO / "_supporting" / "data"
PROCESSED = DATA / "processed"
IN_CSV = PROCESSED / "sku_forecast.csv"
OUT_CSV = PROCESSED / "sku_optimized.csv"

# ---------- mlflow tracking (configure once) ----------
mlflow.set_tracking_uri("sqlite:///mlflow.db")
mlflow.set_experiment("MicroLineage-PriceOptimization")

# ---------- core logic ----------
def optimize_prices(df, cost_col="cost", price_col="price", demand_col="forecast"):
    """
    Maximize total margin = Σ (price_i - cost_i) * demand_i
    subject to:
      - price bounds (±10% around current price)
      - average price cap (<= +5% vs current average)
    """
    n = len(df)
    price = df[price_col].to_numpy(dtype=float)
    cost = df[cost_col].to_numpy(dtype=float)
    demand = df[demand_col].to_numpy(dtype=float)

    # minimize -margin to maximize margin
    c = -1.0 * (price - cost) * demand

    bounds = [(0.9 * p, 1.1 * p) for p in price]  # ±10%
    A_eq, b_eq = None, None

    # Average price cap: mean(new_price) <= 1.05 * mean(old_price)
    A_ub = [np.ones(n) / n]
    b_ub = [1.05 * price.mean()]

    res = linprog(c, A_ub=A_ub, b_ub=b_ub, A_eq=A_eq, b_eq=b_eq, bounds=bounds, method="highs")
    if not res.success:
        return None, res

    opt_price = res.x
    out = df.copy()
    out["optimized_price"] = np.round(opt_price, 2)
    out["optimized_margin"] = np.round((out["optimized_price"] - cost) * demand, 2)
    return out, res

if __name__ == "__main__":
    if not IN_CSV.exists():
        raise FileNotFoundError(
            f"Missing input: {IN_CSV.relative_to(REPO)}. "
            f"Run: python .\\_supporting\\data\\make_sku_forecast.py"
        )

    df = pd.read_csv(IN_CSV)
    df.columns = [c.lower() for c in df.columns]
    for col in ["sku", "date", "cost", "price", "forecast"]:
        if col not in df.columns:
            raise ValueError(f"{IN_CSV.name} missing column: {col}")

    optimized, res = optimize_prices(df, "cost", "price", "forecast")
    if optimized is None:
        raise RuntimeError(f"Optimization failed: {res.message}")

    # ---------- MLflow lineage (best-effort; still write CSV if logging fails) ----------
    baseline = float(((df["price"] - df["cost"]) * df["forecast"]).sum())
    after = float(optimized["optimized_margin"].sum())
    uplift = after - baseline

    PROCESSED.mkdir(parents=True, exist_ok=True)

    try:
        with mlflow.start_run(run_name="optimize_prices"):
            mlflow.log_param("bounds_pct", 0.10)
            mlflow.log_param("avg_price_cap_pct", 0.05)
            mlflow.log_metric("baseline_margin", baseline)
            mlflow.log_metric("optimized_margin", after)
            mlflow.log_metric("uplift", uplift)

            optimized.to_csv(OUT_CSV, index=False)
            mlflow.log_artifact(str(OUT_CSV), artifact_path="artifacts")
    except Exception:
        # Fallback: write CSV even if MLflow not configured
        optimized.to_csv(OUT_CSV, index=False)

    print(f"✅ Optimization complete. Wrote {OUT_CSV.relative_to(REPO)} ({len(optimized)} rows).")
