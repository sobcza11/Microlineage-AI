# _supporting/schemas/pos.py
from __future__ import annotations
import pandas as pd
import pandera as pa
from pandera.typing import Series
from pandera import Field

class POS(pa.DataFrameModel):
    # Keys
    store_id: Series[int] = Field(ge=0)
    sku_id: Series[int] = Field(ge=0)

    # Timestamp (tz-aware UTC)
    ts: Series[pd.Timestamp] = Field(coerce=True)

    # Measures
    qty: Series[float] = Field(ge=0)
    price: Series[float] = Field(gt=0)
    promo_flag: Series[bool]
    stock_out_flag: Series[bool]

    class Config:
        strict = True
        coerce = True

    @pa.check("qty")
    def _finite_qty(cls, s: Series[float]) -> Series[bool]:
        return s.notna() & ~s.isin([float("inf"), float("-inf")])

    @pa.dataframe_check
    def _utc_timestamp(cls, df: pd.DataFrame) -> bool:
        return (pd.api.types.is_datetime64tz_dtype(df["ts"])
                and str(df["ts"].dt.tz) == "UTC")

    @pa.dataframe_check
    def _unique_key(cls, df: pd.DataFrame) -> bool:
        return ~df.duplicated(subset=["store_id", "sku_id", "ts"]).any()

def coerce_utc(df: pd.DataFrame, ts_col: str = "ts") -> pd.DataFrame:
    df[ts_col] = pd.to_datetime(df[ts_col], utc=True, errors="coerce")
    return df
