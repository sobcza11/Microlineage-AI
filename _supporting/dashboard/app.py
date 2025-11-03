import streamlit as st, pandas as pd, numpy as np

st.set_page_config(page_title="MicroLineage AI", layout="wide")
st.title("Market Health Index")

c1, c2, c3 = st.columns(3)
c1.metric("MAPE (7d)", "12.8%", "-1.1%")
c2.metric("PSI (features)", "0.08", "stable")
c3.metric("Backtest R²", "0.67", "+0.03")

st.subheader("Sample Forecast (placeholder)")
idx = pd.date_range("2025-11-03", periods=14, freq="D")
st.line_chart(pd.DataFrame({"forecast": np.random.randint(8, 16, size=14)}, index=idx))
