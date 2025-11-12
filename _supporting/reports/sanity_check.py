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

