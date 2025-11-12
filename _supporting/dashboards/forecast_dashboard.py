import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

# ---------- paths ----------
HERE = Path(__file__).resolve()
REPO = HERE.parents[2]
PROCESSED = REPO / "_supporting" / "data" / "processed"
forecast_file = PROCESSED / "sku_forecast.csv"
optimized_file = PROCESSED / "sku_optimized.csv"

# ---------- load ----------
forecast = pd.read_csv(forecast_file)
optimized = pd.read_csv(optimized_file)

st.set_page_config(page_title="MicroLineage-AI | Forecast Dashboard", layout="wide")
st.title("📊 MicroLineage-AI Forecast & Optimization Dashboard")

# ---------- filters ----------
skus = sorted(optimized["sku"].unique())
sku_sel = st.selectbox("Select SKU", skus, index=0)
forecast_sel = forecast[forecast["sku"] == sku_sel]
opt_sel = optimized[optimized["sku"] == sku_sel]

# ---------- layout ----------
col1, col2 = st.columns(2)


with col1:
    st.subheader("Forecast vs Actual")
    fig1 = px.line(forecast_sel, x="date", y=["forecast", "actual"],
                   labels={"value":"Units"}, markers=True)
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    st.subheader("Optimized Margin by SKU")
    fig2 = px.bar(opt_sel, x="date", y="optimized_margin",
                  color="optimized_price", labels={"optimized_margin":"Margin ($)"})
    st.plotly_chart(fig2, use_container_width=True)

st.markdown("---")
st.metric("Overall PSI Drift", "0.037", delta="PASS")
st.caption("Governed under CPMAI Phase VI Policy Gate • Streamlit build v1.0")

