# `Micro`Lineage AI

<p align="center">
  <img src="_supporting/assets/main_phto.png" alt="MicroLineage AI Banner" width="400" height="400">
</p>

<<<<<<< HEAD
# `Micro`Lineage AI
=======
<h1 align="center">MicroLineage AI</h1>

# MicroLineage AI
>>>>>>> 8c9d8fd (docs: resize README banner to 400x400 and clean header)

**Economy 4.0** forecasting and optimization are orchestrated and governed by the rigorous principles of DriftOps.

I **forge SKU-level demand vision**, synthesizing the essence of Point-of-Sale data with the vast **external symphony** of **exogenous signals**—*weather, mobility, events, & web trends*—to **assure unshakeable revenue predictability**.

*Ce Stratégique* rests upon "**Policy-as-Code**", a **fundamental commitment** that **transmutes the chaotic swell of data** into **reliable, governed strategic light**, imposing non-negotiable standards for explainability, drift, & secure deployment at the enterprise scale

<<<<<<< HEAD
----

# **Highlights**
- **Time-series**: ARIMA • Prophet • LSTM/GRU (extensible)
- **Optimization**: pricing & replenishment (linear/integer programming)
- **Governance**: drift (PSI/KS), SHAP/LIME, policy gates
- **Delivery**: FastAPI service + Dashboard
----
=======

>>>>>>> 8c9d8fd (docs: resize README banner to 400x400 and clean header)

## Dev quickstart
```bash
cd _supporting
python -m pip install --upgrade pip
pip install -e .
# Run API
uvicorn src.api.app:app --reload
# Run Dashboard
streamlit run dashboard/app.py

