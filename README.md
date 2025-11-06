<p align="center">
  <img src="_supporting/assets/main_phto.png" alt="MicroLineage AI Banner" width="600" height="600">
</p>

<h1 align="center">
  <span style="background-color:#f0f0f0; padding:4px 8px; border-radius:6px;">Micro</span>Lineage AI
</h1>

<p align="center">
  <strong>CI Status</strong><br>
  <a href="https://github.com/sobcza11/Microlineage-AI/actions">
    <img src="https://github.com/sobcza11/Microlineage-AI/actions/workflows/ci.yml/badge.svg?branch=main" alt="CI Status Badge">
  </a>
</p>

---

**Economy 4.0** forecasting & optimization governed by **DriftOps** principles.  
Forecast SKU-level demand from POS + external signals (weather, events, mobility, web trends)  
and enforce **policy-as-code** for explainability, drift, and deployment integrity.

---

## 🧭 Overview
**MicroLineage AI** extends the *DriftOps governance framework* into retail and economic forecasting.  
It fuses time-series modeling, optimization, and explainable AI to help organizations translate data lineage  
into **market lineage** — ensuring transparent, measurable value in **Economy 4.0**.

### 🎯 Core Goals
- Forecast hyper-local demand at SKU or neighborhood level  
- Automate pricing, replenishment, and scenario simulations  
- Maintain full data + model lineage across CI/CD pipelines  
- Audit fairness, drift, and ROI continuously with policy gates  

---

## ⚙️ Architecture Snapshot
Microlineage-AI/
│
├── LICENSE
├── README.md
├── .github/
│ └── workflows/
│ └── ci.yml
└── _supporting/
├── src/
│ ├── api/app.py
│ ├── models/
│ ├── optimization/
│ ├── monitoring/gates.py
│ └── ui/
├── dashboard/app.py
├── assets/main_phto.png
├── policy.yaml
├── pyproject.toml
└── tests/test_smoke.py


---

## 🚀 Dev Quickstart

```bash
cd _supporting
python -m pip install --upgrade pip
pip install -e .
# Run API
uvicorn src.api.app:app --reload
# Run Dashboard
streamlit run dashboard/app.py


