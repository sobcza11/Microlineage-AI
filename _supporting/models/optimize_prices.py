from pathlib import Path
import pandas as pd
import numpy as np
from scipy.optimize import linprog

# add at top
import mlflow

# ... after reading df and before writing CSV:
mlflow.set_tracking_uri("file://" + str((REPO / "mlruns").resolve()))
mlflow.set_experiment("MicroLineage-PriceOptimization")

with mlflow.start_run(run_name="optimize_prices"):
    mlflow.log_param("bounds_pct", 0.10)
    mlflow.log_param("avg_price_cap_pct", 0.05)
    # metrics known only after optimize—log later
    # run optimization...
    # after creating 'optimized':
    uplift_before = ((df["price"] - df["cost"]) * df["forecast"]).sum()
    uplift_after = optimized["optimized_margin"].sum()
    mlflow.log_metric("baseline_margin", float(uplift_before))
    mlflow.log_metric("optimized_margin", float(uplift_after))
    mlflow.log_metric("uplift", float(uplift_after - uplift_before))
    # artifacts
    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    optimized.to_csv(OUT_CSV, index=False)
    mlflow.log_artifact(str(OUT_CSV), artifact_path="artifacts")


HERE = Path(__file__).resolve()
REPO = HERE.parents[2]  # .../Microlineage-AI
DATA = REPO / "_supporting" / "data"
PROCESSED = DATA / "processed"
IN_CSV = PROCESSED / "sku_forecast.csv"
OUT_CSV = PROCESSED / "sku_optimized.csv"

def optimize_prices(df, cost_col='cost', price_col='price', demand_col='forecast'):
    """
    Maximize total margin = sum_i (price_i - cost_i) * demand_i
    subject to:
      - price bounds (±10% around current price)
      - optional gentle regularization to avoid extreme price jumps (as inequality)
    """
    n = len(df)
    price = df[price_col].to_numpy(dtype=float)
    cost = df[cost_col].to_numpy(dtype=float)
    demand = df[demand_col].to_numpy(dtype=float)

    # Objective: maximize -> minimize negative
    c = -1.0 * (price - cost) * demand

    # Bounds: +/-10% around current price
    bounds = [(0.9 * p, 1.1 * p) for p in price]

    # No equality constraints required for basic margin maximization
    A_eq, b_eq = None, None

    # Optional mild cap on average price inflation (<= +5% on avg)
    A_ub = [np.ones(n) / n]
    b_ub = [1.05 * price.mean()]

    res = linprog(c, A_ub=A_ub, b_ub=b_ub, A_eq=A_eq, b_eq=b_eq,
                  bounds=bounds, method='highs')

    if not res.success:
        return None, res

    opt_price = res.x
    df = df.copy()
    df["optimized_price"] = np.round(opt_price, 2)
    df["optimized_margin"] = np.round((df["optimized_price"] - cost) * demand, 2)
    return df, res

if __name__ == "__main__":
    if not IN_CSV.exists():
        raise FileNotFoundError(
            f"Missing input: {IN_CSV.relative_to(REPO)}\n"
            f"Run: python .\\_supporting\\data\\make_sku_forecast.py"
        )

    df = pd.read_csv(IN_CSV)
    required = {"sku","date","cost","price","forecast"}
    missing = required - {c.lower() for c in df.columns}
    if missing:
        raise ValueError(f"{IN_CSV.name} missing columns: {missing}")

    # Normalize column case
    df.columns = [c.lower() for c in df.columns]

    optimized, res = optimize_prices(df, cost_col="cost", price_col="price", demand_col="forecast")
    if optimized is None:
        raise RuntimeError(f"Optimization failed: {res.message}")

    PROCESSED.mkdir(parents=True, exist_ok=True)
    optimized.to_csv(OUT_CSV, index=False)
    print(f"✅ Optimization complete. Wrote {OUT_CSV.relative_to(REPO)} ({len(optimized)} rows).")

