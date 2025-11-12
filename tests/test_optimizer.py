from pathlib import Path
import pandas as pd, json, subprocess, sys

REPO = Path(__file__).resolve().parents[1]

def test_optimizer_and_metrics():
    subprocess.check_call([sys.executable, str(REPO/"_supporting/data/make_sku_forecast.py")])
    subprocess.check_call([sys.executable, str(REPO/"_supporting/models/optimize_prices.py")])
    subprocess.check_call([sys.executable, str(REPO/"_supporting/reports/sanity_check.py")])

    out_csv = REPO/"_supporting/data/processed/sku_optimized.csv"
    met = REPO/"_supporting/data/processed/metrics.json"
    assert out_csv.exists() and met.exists()

    df = pd.read_csv(out_csv)
    cols = {c.lower() for c in df.columns}
    assert {"optimized_price","optimized_margin"}.issubset(cols)

    m = json.loads(met.read_text())
    for k in ["baseline_margin","optimized_margin","uplift","psi","decision"]:
        assert k in m
    assert m["uplift"] >= 0.0
    assert m["psi"] <= 0.10
