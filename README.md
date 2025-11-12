<p align="center">
  <img src="_supporting/assets/main_phto.png" alt="MicroLineage AI Banner" width="600" height="600">
</p>

<h1 align="center"><code>Micro</code>Lineage AI</h1>

<p align="center">
  <a href="https://github.com/sobcza11/Microlineage-AI/actions/workflows/ci.yml">
    <img src="https://github.com/sobcza11/Microlineage-AI/actions/workflows/ci.yml/badge.svg" alt="CI Status">
  </a>
  <br>
  <em>Economy 4.0 Forecasting & Governance Framework</em>
</p>

![Policy Gate](https://img.shields.io/badge/Policy_Gate-PASS-brightgreen)

---

**MicroLineage-AI** explores how localized data ecosystems reshape **economic forecasting** in the **Economy 4.0** era.
By combining real-time POS data, external context (weather & mobility), and machine-learning forecasting,
it models supply-demand dynamics at the neighborhood level.

The framework functions as a **digital twin for micro-economies**, quantifying price elasticity, consumption resilience, and demand drift across local markets.

This system demonstrates how AI-driven micro-analytics can inform fiscal planning & private-sector agility — translating raw data into **signal économique**.

---

![CI](https://img.shields.io/github/actions/workflow/status/sobcza11/Microlineage-AI/policy_check.yml?branch=main)
![Policy Gate](https://img.shields.io/badge/Policy_Gate-PASS-brightgreen)
![License](https://img.shields.io/badge/License-MIT-green)

## Quickstart (Windows PowerShell)

```powershell
# 1) Create forecast input
python .\_supporting\data\make_sku_forecast.py

# 2) Optimize prices (writes _supporting/data/processed/sku_optimized.csv)
python .\_supporting\models\optimize_prices.py

# 3) Sanity report (prints margins, writes metrics.json)
python .\_supporting\reports\sanity_check.py

# 4) Policy gate (fails if psi>0.10 or uplift<0.0)
python .\_supporting\ci\policy_check.py

# 5) Run dashboard (local)
streamlit run .\_supporting\dashboards\forecast_dashboard.py
