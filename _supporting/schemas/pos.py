from __future__ import annotations

import pandas as pd
import pandera as pa
from pandera.typing import Series


class POS(pa.DataFrameModel):
    # Keys (coerce numeric when present; tolerate empty header-only)
    store_id: Series[object] = pa.Field(coerce=True, nullable=True)
    sku_id: Series[object] = pa.Field(coerce=True, nullable=True)

    # Time (empty-safe + UTC); timestamp rule via @pa.check
    ts: Series[pd.Timestamp] = pa.Field(coerce=True, nullable=True)

    # Measures
    qty: Series[object] = pa.Field(coerce=True, nullable=True, ge=0)
    price: Series[object] = pa.Field(coerce=True, nullable=True, ge=0)
    promo_flag: Series[object] = pa.Field(coerce=True, nullable=True, isin=[0, 1])
    stock_out_flag: Series[object] = pa.Field(coerce=True, nullable=True, isin=[0, 1])

    @pa.check("ts")
    def ts_utc_or_empty(cls, ts: pd.Series) -> bool:
        if ts.empty:
            return True
        try:
            return getattr(ts.dt.tz, "key", None) == "UTC"
        except Exception:
            return False


def coerce_utc(df: pd.DataFrame, col: str) -> pd.DataFrame:
    """Ensure column is tz-aware UTC even for empty frames."""
    df[col] = pd.to_datetime(df[col], utc=True, errors="coerce")
    if df.empty or df[col].isna().all():
        df[col] = df[col].astype("datetime64[ns, UTC]")
    return df
