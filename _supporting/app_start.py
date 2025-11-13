from pathlib import Path
import subprocess, sys

ROOT = Path(__file__).resolve().parents[1]     # /app/_supporting -> /app
PROC = ROOT / "data" / "processed"
NEEDED = [PROC/"sku_forecast.csv", PROC/"sku_optimized.csv", PROC/"metrics.json"]

def run(cmd):
    print(f"? {cmd}")
    subprocess.check_call(cmd, shell=True)

# create if missing
if not all(p.exists() for p in NEEDED):
    run("python _supporting/data/make_sku_forecast.py")
    run("python _supporting/models/optimize_prices.py")
    run("python _supporting/reports/sanity_check.py")

# launch app
run("streamlit run _supporting/dashboards/forecast_dashboard.py --server.port=8501 --server.address=0.0.0.0")
