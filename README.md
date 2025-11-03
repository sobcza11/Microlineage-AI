# MicroLineage AI

<p align="center">
  <img src="assets/main_phto.png" alt="MicroLineage AI Banner" width="100%">
</p>

# MicroLineage AI


**Economy 4.0** forecasting & optimization, governed by DriftOps principles.  
Forecast SKU-level demand from POS + external signals (weather, events, mobility, web trends) and enforce **policy-as-code** for explainability, drift, and deployment.

**Highlights**
- Time-series: ARIMA • Prophet • LSTM/GRU (extensible)
- Optimization: pricing & replenishment (linear/integer programming)
- Governance: drift (PSI/KS), SHAP/LIME, policy gates
- Delivery: FastAPI service + Dashboard

[![CI](https://github.com/sobcza11/Microlineage-AI/actions/workflows/ci.yml/badge.svg)](https://github.com/sobcza11/Microlineage-AI/actions)

## Dev quickstart
```bash
python -m pip install --upgrade pip
pip install -e .
# API
uvicorn src.api.app:app --reload
# Dashboard
streamlit run dashboard/app.py
