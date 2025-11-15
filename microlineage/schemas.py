# microlineage/schemas.py

from __future__ import annotations

import pandera as pa
from pandera import Column, Check, DataFrameSchema


# Canonical data contract for the main forecasting input
RetailSchema: DataFrameSchema = DataFrameSchema(
    {
        # IDs / keys
        "store_id": Column(
            pa.String,
            nullable=False,
            description="Micro-market or store identifier.",
        ),
        "sku_id": Column(
            pa.String,
            nullable=False,
            description="SKU identifier.",
        ),
        "date": Column(
            pa.DateTime,
            nullable=False,
            description="Transaction or observation date.",
        ),

        # Core signal
        "units_sold": Column(
            pa.Float,
            nullable=False,
            checks=[Check.ge(0)],
            description="Units sold for the given store, SKU, and date.",
        ),

        # Price & margin levers
        "price": Column(
            pa.Float,
            nullable=False,
            checks=[Check.gt(0)],
            description="Unit price in local currency.",
        ),
        "promo_flag": Column(
            pa.Int,
            nullable=False,
            checks=[Check.isin([0, 1])],
            description="1 if promotion active, 0 otherwise.",
        ),
        "cost": Column(
            pa.Float,
            nullable=True,
            checks=[Check.ge(0)],
            description="Unit cost used for margin calculations.",
        ),

        # Optional demand drivers
        "day_of_week": Column(
            pa.Int,
            nullable=True,
            checks=[Check.isin(list(range(7)))],
            description="Day of week encoded as 0–6.",
        ),
        "holiday_flag": Column(
            pa.Int,
            nullable=True,
            checks=[Check.isin([0, 1])],
            description="1 if date is holiday, 0 otherwise.",
        ),
    },
    strict=False,  # allow additional engineered features
    name="RetailSchema",
    description="Canonical retail forecast input schema for MicroLineage-AI.",
)
