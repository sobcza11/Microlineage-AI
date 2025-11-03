import json, pathlib, yaml

def validate_against_policy(metrics_path="artifacts/metrics.json", policy_path="policy.yaml"):
    pol = yaml.safe_load(open(policy_path))
    m = json.load(open(metrics_path)) if pathlib.Path(metrics_path).exists() else {}
    errs = []
    if m.get("backtest_r2", 1) < pol["min_backtest_r2"]:
        errs.append(f"R2 {m.get('backtest_r2')} < {pol['min_backtest_r2']}")
    if m.get("mape", 0) > (1 - pol["min_forecast_mape"]):
        errs.append(f"MAPE {m.get('mape')} > {(1 - pol['min_forecast_mape'])}")
    if m.get("psi", 0) > pol["max_drift_psi"]:
        errs.append(f"PSI {m.get('psi')} > {pol['max_drift_psi']}")
    if errs:
        raise SystemExit("Policy gate failed:\n- " + "\n- ".join(errs))
    print("Policy gate passed.")
