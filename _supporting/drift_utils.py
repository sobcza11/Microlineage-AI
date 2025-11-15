# _supporting/drift_utils.py

import numpy as np
import pandas as pd
from typing import Dict


def _psi_single(expected: np.ndarray, actual: np.ndarray, buckets: int = 10) -> float:
    """Population Stability Index for numeric distributions."""
    expected = np.array(expected, dtype=float)
    actual = np.array(actual, dtype=float)

    # Guard: no variance or too few points
    if len(np.unique(expected)) == 1 or len(np.unique(actual)) == 1:
        return 0.0

    quantiles = np.linspace(0, 100, buckets + 1)
    cuts = np.unique(np.percentile(expected, quantiles))
    expected_counts, _ = np.histogram(expected, bins=cuts)
    actual_counts, _ = np.histogram(actual, bins=cuts)

    # Avoid zero division
    expected_perc = np.where(expected_counts == 0, 1e-6, expected_counts) / expected_counts.sum()
    actual_perc = np.where(actual_counts == 0, 1e-6, actual_counts) / actual_counts.sum()

    psi_values = (actual_perc - expected_perc) * np.log(actual_perc / expected_perc)
    return float(np.sum(psi_values))


def compute_drift_metrics(
    reference_df: pd.DataFrame,
    current_df: pd.DataFrame,
    numeric_cols: list | None = None,
    psi_threshold: float = 0.2,
) -> pd.DataFrame:
    """
    Compute PSI per numeric column & flag drift.
    Returns a DataFrame: column | psi | drift_flag.
    """
    if numeric_cols is None:
        numeric_cols = reference_df.select_dtypes(include=["int", "float", "number"]).columns.tolist()

    records: list[Dict] = []
    for col in numeric_cols:
        if col not in reference_df.columns or col not in current_df.columns:
            continue

        ref = reference_df[col].dropna()
        cur = current_df[col].dropna()
        if len(ref) < 50 or len(cur) < 50:
            # Not enough data to be meaningful; skip or mark as 0.
            psi = 0.0
        else:
            psi = _psi_single(ref, cur)

        records.append(
            {
                "column": col,
                "psi": round(psi, 4),
                "drift_flag": psi >= psi_threshold,
            }
        )

    df_psi = pd.DataFrame(records).sort_values("psi", ascending=False)
    return df_psi.reset_index(drop=True)


def summarize_drift(df_psi: pd.DataFrame) -> Dict[str, float | int]:
    if df_psi.empty:
        return {
            "max_psi": 0.0,
            "drifted_features": 0,
            "total_features": 0,
        }
    return {
        "max_psi": float(df_psi["psi"].max()),
        "drifted_features": int(df_psi["drift_flag"].sum()),
        "total_features": int(len(df_psi)),
    }
