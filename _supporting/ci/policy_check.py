import sys, json, yaml
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
PROCESSED = REPO / "_supporting" / "data" / "processed"
POLICY = REPO / "_supporting" / "governance" / "policy_gate.yaml"
METRICS = PROCESSED / "metrics.json"

if not METRICS.exists():
    print("? metrics.json not found. Did you run sanity_check.py?")
    sys.exit(2)

metrics = json.loads(METRICS.read_text())
policy = yaml.safe_load(POLICY.read_text())

psi_max = float(policy["thresholds"]["psi_max"])
uplift_min = float(policy["thresholds"]["uplift_min"])

psi = float(metrics["psi"])
uplift = float(metrics["uplift"])

ok_drift = psi <= psi_max
ok_uplift = uplift >= uplift_min

print(f"PSI={psi} (max {psi_max}) ? {'OK' if ok_drift else 'FAIL'}")
print(f"Uplift={uplift} (min {uplift_min}) ? {'OK' if ok_uplift else 'FAIL'}")

if ok_drift and ok_uplift:
    print("? Policy gate: PASS")
    sys.exit(0)
else:
    print("? Policy gate: FAIL")
    sys.exit(1)
