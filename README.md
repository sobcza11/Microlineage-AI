# `Micro`Lineage AI

<p align="center">
  <img src="_supporting/assets/main_phto.png" alt="MicroLineage AI Banner" width="100%">
</p>

# MicroLineage AI

**Economy 4.0** forecasting & optimization, **governed by DriftOps principles**.  

Forecast SKU-level demand from POS + external signals (weather, events, mobility, web trends) and enforce **policy-as-code** for explainability, drift, and deployment.


**Economy 4.0** forecasting and optimization are orchestrated and governed by the rigorous principles of DriftOps.

I **forge SKU-level demand vision**, synthesizing the essence of Point-of-Sale data with the vast **external symphony** of **exogenous signals**—*weather, mobility, events, and web trends*—to **assure unshakeable revenue predictability**.

*Ce Stratégique* rests upon "**Policy-as-Code**", a **fundamental commitment** that **transmutes the chaotic swell of data** into **reliable, governed strategic light**, imposing non-negotiable standards for explainability, drift, and secure deployment at the enterprise scale

----

**Highlights**
- Time-series: ARIMA • Prophet • LSTM/GRU (extensible)
- Optimization: pricing & replenishment (linear/integer programming)
- Governance: drift (PSI/KS), SHAP/LIME, policy gates
- Delivery: FastAPI service + Dashboard
----

## Dev quickstart
```bash
python -m pip install --upgrade pip
pip install -e .
# API
uvicorn src.api.app:app --reload
# Dashboard
streamlit run dashboard/app.py
