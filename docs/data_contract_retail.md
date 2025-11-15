# Data Contract: Retail Forecast Input

This table describes the expected input structure enforced by Pandera for the core forecasting pipeline.

| column       | dtype          | nullable   | checks                   | description                                    |
|:-------------|:---------------|:-----------|:-------------------------|:-----------------------------------------------|
| store_id     | str            | False      |                          | Micro-market or store identifier.              |
| sku_id       | str            | False      |                          | SKU identifier.                                |
| date         | datetime64[ns] | False      |                          | Transaction or observation date.               |
| units_sold   | float64        | False      | greater_than_or_equal_to | Units sold for the given store, SKU, and date. |
| price        | float64        | False      | greater_than             | Unit price in local currency.                  |
| promo_flag   | int64          | False      | isin                     | 1 if promotion active, 0 otherwise.            |
| cost         | float64        | True       | greater_than_or_equal_to | Unit cost used for margin calculations.        |
| day_of_week  | int64          | True       | isin                     | Day of week encoded as 0–6.                    |
| holiday_flag | int64          | True       | isin                     | 1 if date is holiday, 0 otherwise.             |
