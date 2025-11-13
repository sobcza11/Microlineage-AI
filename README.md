<p align="center">
  <img src="_supporting/assets/main_phto.png" alt="MicroLineage AI Banner" width="600" height="600">
</p>

<h1 align="center"><code>Micro</code>Lineage AI</h1>

<p align="center">
  <img src="https://img.shields.io/badge/Policy_Gate-PASS-brightgreen" alt="Policy Gate"/>
  <a href="https://github.com/sobcza11/Microlineage-AI/actions/workflows/ci.yml">
    <img src="https://github.com/sobcza11/Microlineage-AI/actions/workflows/ci.yml/badge.svg" alt="CI Status">
  </a>
  <img src="https://img.shields.io/badge/License-MIT-green" alt="MIT License"/>
  <br>
  <em>Economy 4.0 Forecasting & Governance Framework</em>
</p>

---

# 🧭 Overview

**MicroLineage-AI** models how localized data ecosystems reshape economic forecasting in the **Economy 4.0** era.

Built as a micro-economy “digital twin,” it blends:

- real-time POS data
- weather & mobility context
- SKU-level demand forecasting
- price-elasticity optimization
- drift monitoring (PSI)
- CPMAI Phase VI policy gates

The outcome: a transparent, uplift-oriented pricing & forecasting system that quantifies **consumption resilience, elasticity, and signal économique** within hyper-local markets.

---

# 🚀 Run & Governance Model

MicroLineage-AI is structured around a **governed delivery flow**:

1. **Forecast Generation**
2. **Price Optimization**
3. **Sanity Check (Margin, Uplift, PSI)**
4. **Policy Gate (CPMAI Phase VI)**
5. **Dashboard Deployment**

A release is considered *safe-to-show* when:

| Condition | Meaning |
|----------|---------|
| **Uplift ≥ 0%** | Optimization never reduces baseline margin |
| **PSI ≤ threshold** | No harmful distribution drift |
| **Decision Gate: PASS** | Ready for executive consumption |

---

## Run with Docker (one-line)

If you have Docker installed, you can run the full MicroLineage-AI stack with:

```bash
docker run --rm -p 8501:8501 sobcza11/microlineage-ai:latest

---

# 💻 Local Run (Windows PowerShell)

From the repo root:

```powershell
# 1) Activate virtual environment
.\.venv\Scripts\Activate.ps1

# 2) Install dependencies
pip install -r requirements.txt

# 3) Launch dashboard (local dev)
streamlit run _supporting/dashboards/forecast_dashboard.py `
  --server.port=8502 `
  --server.address=127.0.0.1
