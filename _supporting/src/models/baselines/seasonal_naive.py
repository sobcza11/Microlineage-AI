from __future__ import annotations

import numpy as np
import pandas as pd


class SeasonalNaive:
    name = "seasonal_naive"

    def __init__(self, season: int = 7):
        self.season = season

    def fit(self, y: pd.Series) -> SeasonalNaive:
        self.y = y.astype(float)
        return self

    def forecast(self, horizon: int) -> np.ndarray:
        if len(self.y) == 0:
            return np.zeros(horizon, dtype=float)
        # repeat the last `season` values forward
        tail = self.y.iloc[-self.season:] if len(self.y) >= self.season else self.y
        reps = int(np.ceil(horizon / len(tail)))
        return np.tile(tail.values, reps)[:horizon]
