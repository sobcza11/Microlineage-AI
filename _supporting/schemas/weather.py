# _supporting/schemas/weather.py
from __future__ import annotations
import pandas as pd
import pandera as pa
from pandera.typing import Series
from pandera import Field

class Weather(pa.DataFrameModel):
    store_id: Series[int] = Field(ge=0)
    ts: Series[pd.Timestamp] = Field(coerce=True)  # tz-aware UTC
    temp_c: Series[float] = Field(ge=-60, le=60)
    precip_mm: Series[float] = Field(ge=0)
    is_holiday: Series[bool] = Field(nullable=True)
    event_id: Series[str] = Field(nullable=True)

    class Config:
        strict = True
        coerce = True

    @pa.dataframe_check
    def _utc_timestamp(cls, df: pd.DataFrame) -> bool:
        return (pd.api.types.is_datetime64tz_dtype(df["ts"])
                and str(df["ts"].dt.tz) == "UTC")
