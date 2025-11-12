# _supporting/src/data/validate.py
"""
Validate MicroLineage data against schemas and emit a freshness report.

Usage:
  python -m _supporting.src.data.validate \
    --pos _supporting/data/samples/pos.csv \
    --weather _supporting/data/samples/weather.csv \
    --sku_ref _supporting/data/samples/sku_ref.csv \
    --out _supporting/reports/data_freshness.json
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from datetime import UTC, datetime
from pathlib import Path

import pandas as pd

# --- Ensure repo root is on sys.path even if launched oddly (e.g., direct .py call)
try:
    REPO_ROOT = Path(__file__).resolve().parents[2]
    if str(REPO_ROOT) not in sys.path:
        sys.path.insert(0, str(REPO_ROOT))
except Exception:
    pass

# --- Import schemas from _supporting
from _supporting.schemas.pos import POS, coerce_utc
from _supporting.schemas.ref import SKURef
from _supporting.schemas.weather import Weather


# ---------- I/O helpers ----------
def _read_table(path: str) -> pd.DataFrame:
    """Read CSV/Parquet with friendly errors."""
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(f"Missing file: {p}")
    try:
        if p.suffix.lower() == ".parquet":
            return pd.read_parquet(p)
        return pd.read_csv(p)
    except Exception as e:
        raise RuntimeError(f"Failed to load {p}: {e}") from e


def _safe_write_json(obj: dict, out_path: str) -> None:
    """Atomically write JSON and log the absolute path."""
    out = Path(out_path).resolve()
    out.parent.mkdir(parents=True, exist_ok=True)
    tmp = out.with_suffix(out.suffix + ".tmp")
    with tmp.open("w", encoding="utf-8") as f:
        json.dump(obj, f, indent=2)
        f.flush()
        os.fsync(f.fileno())
    tmp.replace(out)
    print(f"[validate] wrote → {out}")


# ---------- validators ----------
def validate_pos(path: str) -> dict:
    df = _read_table(path)
    df = coerce_utc(df, "ts")
    POS.validate(df)
    latest_ts = pd.to_datetime(df["ts"]).max() if len(df) else pd.NaT
    return {
        "rows": int(len(df)),
        "min_ts": (str(pd.to_datetime(df["ts"]).min()) if len(df) else None),
        "max_ts": (str(latest_ts) if len(df) else None),
        "stores": int(df["store_id"].nunique()) if "store_id" in df else 0,
        "skus": int(df["sku_id"].nunique()) if "sku_id" in df else 0,
    }


def validate_weather(path: str) -> dict:
    df = _read_table(path)
    if "ts" in df.columns:
        df["ts"] = pd.to_datetime(df["ts"], utc=True, errors="coerce")
    Weather.validate(df)
    return {
        "rows": int(len(df)),
        "min_ts": (str(pd.to_datetime(df["ts"]).min()) if len(df) else None),
        "max_ts": (str(pd.to_datetime(df["ts"]).max()) if len(df) else None),
        "stores": int(df["store_id"].nunique()) if "store_id" in df else 0,
    }


def validate_sku_ref(path: str) -> dict:
    df = _read_table(path)
    SKURef.validate(df)
    return {
        "rows": int(len(df)),
        "stores": int(df["store_id"].nunique()) if "store_id" in df else 0,
        "skus": int(df["sku_id"].nunique()) if "sku_id" in df else 0,
        "categories": int(df["category"].nunique()) if "category" in df else 0,
    }


# ---------- CLI ----------
def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--pos", required=True, help="path to POS csv/parquet")
    ap.add_argument("--weather", required=True, help="path to weather csv/parquet")
    ap.add_argument("--sku_ref", required=True, help="path to sku_ref csv/parquet")
    ap.add_argument("--out", required=True, help="path to output JSON report")
    args = ap.parse_args()

    # Explicitly log the out path we will use
    print(f"[validate] out = {args.out}")

    report: dict = {
        "generated_at_utc": datetime.now(UTC).isoformat(),
        "status": "success",
        "checks": {},
    }

    try:
        report["checks"]["pos"] = validate_pos(args.pos)
        report["checks"]["weather"] = validate_weather(args.weather)
        report["checks"]["sku_ref"] = validate_sku_ref(args.sku_ref)
        _safe_write_json(report, args.out)
        return 0
    except Exception as e:
        # Still persist a useful failure report
        report["status"] = "fail"
        report["error"] = f"{type(e).__name__}: {e}"
        _safe_write_json(report, args.out)
        print(f"[validate] ERROR: {report['error']}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
