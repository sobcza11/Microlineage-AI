# _supporting/schema_contract.py

from __future__ import annotations

import pandas as pd
import pandera as pa
from typing import Any


def schema_to_contract_df(schema: pa.DataFrameSchema) -> pd.DataFrame:
    """
    Convert a Pandera DataFrameSchema into a contract table:
    column | dtype | nullable | checks | description
    """
    records: list[dict[str, Any]] = []

    for name, col in schema.columns.items():
        dtype = str(col.dtype)
        nullable = bool(col.nullable)

        checks = []
        for check in col.checks:
            try:
                checks.append(check.name or repr(check))
            except Exception:
                checks.append(repr(check))
        checks_str = "; ".join(checks) if checks else ""

        description = getattr(col, "description", "") or ""

        records.append(
            {
                "column": name,
                "dtype": dtype,
                "nullable": nullable,
                "checks": checks_str,
                "description": description,
            }
        )

    df = pd.DataFrame(records)
    return df[["column", "dtype", "nullable", "checks", "description"]]
