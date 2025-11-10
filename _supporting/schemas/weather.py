from __future__ import annotations

import pandas as pd
import pandera as pa
from pandera.typing import Series


class Weather(pa.DataFrameModel):
    # Keys / IDs (coerce when present; tolerate empty header-only)
    store_id: Series[object] = pa.Field(coerce=True, nullable=True)
    event_id: Series[object] = pa.Field(nullable=True)

    # Time (empty-safe + UTC); rule via @pa.check
    ts: Series[pd.Timestamp] = pa.Field(coerce=True, nullable=True)

    # Measures / flags
    temp_c: Series[object] = pa.Field(coerce=True, nullable=True)
    precip_mm: Series[object] = pa.Field(coerce=True, nullable=True)
    is_holiday: Series[object] = pa.Field(coerce=True, nullable=True, isin=[0, 1])

    @pa.check("ts")
    def ts_utc_or_empty(cls, ts: pd.Series) -> bool:
        if ts.empty:
            return True
        try:
            return getattr(ts.dt.tz, "key", None) == "UTC"
        except Exception:
            return False
