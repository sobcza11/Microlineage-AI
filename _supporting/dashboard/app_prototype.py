import numpy as np
import pandas as pd
import streamlit as st
from _supporting.drift_utils import compute_drift_metrics, summarize_drift
from microlineage.data import load_current_data, load_reference_data  # adjust import paths

# Inside main() or equivalent Streamlit layout function
st.markdown("### Data Drift Monitor")

# Load data
reference_df = load_reference_data()  # baseline / training-period data
current_df = load_current_data()      # latest batch used for forecasts

with st.spinner("Computing drift metrics..."):
    drift_df = compute_drift_metrics(reference_df, current_df)
    drift_summary = summarize_drift(drift_df)

col1, col2, col3 = st.columns(3)
with col1:
    st.metric(
        "Max PSI",
        f"{drift_summary['max_psi']:.3f}",
        help="Population Stability Index across numeric features.",
    )
with col2:
    st.metric(
        "Drifted Features",
        f"{drift_summary['drifted_features']} / {drift_summary['total_features']}",
        help="Number of features with PSI above threshold.",
    )
with col3:
    status = "Stable" if drift_summary["drifted_features"] == 0 else "Monitor"
    st.metric("Drift Status", status)

with st.expander("View feature-level drift table"):
    if drift_df.empty:
        st.info("No numeric features or insufficient data to compute PSI.")
    else:
        st.dataframe(drift_df, use_container_width=True)

        # Optional: let user pick a feature to inspect
        feature = st.selectbox(
            "Inspect feature distribution",
            options=drift_df["column"].tolist(),
            index=0,
        )

        if feature:
            c1, c2 = st.columns(2)
            with c1:
                st.caption(f"Reference distribution for `{feature}`")
                st.histogram(reference_df[feature].dropna(), use_container_width=True)
            with c2:
                st.caption(f"Current distribution for `{feature}`")
                st.histogram(current_df[feature].dropna(), use_container_width=True)



st.set_page_config(page_title="MicroLineage AI", layout="wide")
st.title("Market Health Index")

c1, c2, c3 = st.columns(3)
c1.metric("MAPE (7d)", "12.8%", "-1.1%")
c2.metric("PSI (features)", "0.08", "stable")
c3.metric("Backtest R²", "0.67", "+0.03")

st.subheader("Sample Forecast (placeholder)")
idx = pd.date_range("2025-11-03", periods=14, freq="D")
st.line_chart(pd.DataFrame({"forecast": np.random.randint(8, 16, size=14)}, index=idx))
