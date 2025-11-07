from __future__ import annotations
import numpy as np
import pandas as pd

class Naive:
    name = "naive"

    def fit(self, y: pd.Series) -> "Naive":
        self.last = float(y.iloc[-1]) if len(y) else 0.0
        return self

    def forecast(self, horizon: int) -> np.ndarray:
        return np.full(horizon, self.last, dtype=float)
