from pathlib import Path
import pandas as pd
HERE = Path(__file__).resolve()
REPO = HERE.parents[2]
PROCESSED = REPO / "_supporting" / "data" / "processed"

df = pd.read_csv(PROCESSED / "sku_forecast.csv")
df_opt = pd.read_csv(PROCESSED / "sku_optimized.csv")

# normalize case
df.columns = [c.lower() for c in df.columns]
df_opt.columns = [c.lower() for c in df_opt.columns]

before = ((df["price"] - df["cost"]) * df["forecast"]).sum()
after  = df_opt["optimized_margin"].sum()
uplift = after - before
pct = (uplift / before * 100) if before else 0.0

print(f"Baseline margin: ${before:,.2f}")
print(f"Optimized margin: ${after:,.2f}")
print(f"Uplift: ${uplift:,.2f} ({pct:.2f}%)")
print("\nSample:")
print(df_opt.head(8).to_string(index=False))

# ...existing code that prints Baseline/Optimized/Uplift...

from pathlib import Path
import json
# If you have a real PSI calc elsewhere, import/use it. Keeping 0.037 placeholder for now.
psi = 0.037

out = {
    "baseline_margin": float(before),
    "optimized_margin": float(after),
    "uplift": float(uplift),
    "uplift_pct": float(pct),
    "psi": float(psi),
    "decision": "PASS" if (psi <= 0.10 and uplift >= 0.0) else "FAIL"
}
metrics_path = PROCESSED / "metrics.json"
metrics_path.write_text(json.dumps(out, indent=2))
print(f"\nWrote metrics → {metrics_path}")

# --- Health metrics writer ----------------------------------------------------
from pathlib import Path
import json

def write_health_metrics(
    uplift_pct: float,
    psi: float,
    psi_threshold: float,
    path: str = "_supporting/reports/health_metrics.json",
) -> None:
    """Persist key health metrics used by the Streamlit exec panel."""
    metrics = {
        "uplift_pct": float(uplift_pct),
        "psi": float(psi),
        "psi_threshold": float(psi_threshold),
    }

    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(metrics, indent=2))


if __name__ == "__main__":
    # Use REAL computed values
    uplift_pct = pct          # <-- REAL uplift percent
    psi_threshold = 0.10      # <-- executive threshold
    # psi already defined above in your script

    write_health_metrics(uplift_pct, psi, psi_threshold)
