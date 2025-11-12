# _supporting/schemas/ref.py
from __future__ import annotations

import pandera as pa
from pandera import Field
from pandera.typing import Series


class SKURef(pa.DataFrameModel):
    store_id: Series[int] = Field(ge=0)
    sku_id: Series[int] = Field(ge=0)
    category: Series[str]
    brand: Series[str] = Field(nullable=True)
    size: Series[str] = Field(nullable=True)  # e.g., "12oz", "500ml"
    cost: Series[float] = Field(ge=0)

    class Config:
        strict = True
        coerce = True
