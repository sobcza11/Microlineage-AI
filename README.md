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

Hyper-local retail demand forecasting & pricing optimization with **governance built in** — a small, opinionated sandbox for showing how CPMAI-aligned MLOps, drift monitoring, & lightweight model governance can work in practice.

> **Design intent:** Treat this repo as a **“micro-market control tower”** — small enough to reason about, rich enough to demonstrate real-world practices.

---

## What MicroLineage-AI Does

MicroLineage-AI is a governed analytics workflow for SKU-level retail:

- **Forecasts SKU demand** on a rolling horizon.
- **Optimizes prices & margin** from those forecasts.
- **Validates inputs & outputs** using Pandera schemas.
- **Monitors drift** (e.g., PSI) & surfaces a pass/fail policy gate.
- **Publishes a Streamlit dashboard** for interactive exploration.
- **Ships with CI & Docker**, so everything can be rebuilt deterministically.

It is intentionally structured as a **learning & demonstration environment**:

- Small, realistic pipeline.
- Clear governance hooks.
- Easy to extend with new models, features, or stores.

---

# 🔧 Project Layout

Root is intentionally kept lean: infra & entry-points at the top, everything else in `_supporting/`.

```text
Microlineage-AI/
│
├── .github/workflows/          # CI: lint, tests, Docker build/publish
├── tests/                      # Public tests
├── _supporting/                # Application code, models, data, reports
│   ├── assets/                 # Images/static assets
│   ├── ci/                     # CI helper scripts
│   ├── config/                 # Config (JSON/YAML)
│   ├── dashboard/              # Streamlit apps
│   │   ├── app_prototype.py
│   │   └── forecast_dashboard.py
│   ├── data/                   # Raw/interim/processed
│   │   └── processed/          # Forecast & optimization outputs
│   ├── governance/             # Policy gate & CPMAI logic
│   ├── models/                 # Model training & optimization
│   ├── reports/                # Drift & health metrics
│   ├── schemas/                # Pandera schemas for data contracts
│   ├── src/                    # Core logic utilities
│   └── tools/                  # CLIs & helper scripts
│
├── microlineage/               # Python package: schemas, pipelines, utils
│   ├── __init__.py
│   └── schemas.py
│
├── Dockerfile                  # Container build
├── Makefile                    # Lint, test, build targets
├── README.md                   # You are here
├── LICENSE                     # MIT
│
├── requirements.txt            # Runtime deps
├── requirements-dev.txt        # Dev/test deps
│
├── .gitignore
├── .gitattributes
├── .pre-commit-config.yaml
├── .ruffignore
├── pytest.ini
└── conftest.py

# 🧱 Architecture
flowchart LR
    subgraph DataSource[Micro-Market Data Sources]
        POS[POS / Transactions]
        Price[Price & Promo History]
        Catalog[SKU Catalog]
    end

    subgraph Ingest[Ingest & Preparation]
        IngestRaw[Load raw data\n(CSV / Parquet / DB)]
        Pandera[Validate with Pandera\n(Data Contract)]
        Features[Feature engineering\nlags, seasonality, covariates]
    end

    subgraph Modeling[Forecasting & Optimization Engine]
        ModelTrain[Train forecasting model\nSKU-level time-series]
        MLflow[Log runs & metrics\nMLflow Tracking]
        Forecast[Generate demand forecasts\nper SKU]
        Optimize[Optimization engine\nprice elasticity & margin lift]
    end

    subgraph Governance[Governance & Drift Monitoring]
        Tests[Pytest & CI]
        Drift[Data drift checks\nPSI & sanity]
        Policy[Policy Gate\nCPMAI-aligned]
    end

    subgraph Delivery[Delivery & Experience]
        Streamlit[Governed Dashboard]
        Reports[Forecast & drift reports]
    end

    subgraph Deploy[Deployability]
        Docker[Docker Image]
        CI[GitHub Actions: lint/tests/build]
    end

    POS --> IngestRaw
    Price --> IngestRaw
    Catalog --> IngestRaw

    IngestRaw --> Pandera --> Features --> ModelTrain --> Forecast --> Optimize
    ModelTrain --> MLflow

    Features --> Drift
    Drift --> Streamlit

    ModelTrain --> Tests
    Drift --> Tests
    Tests --> CI

    Forecast --> Streamlit
    Optimize --> Streamlit
    Streamlit --> Reports

    Streamlit --> Docker --> CI
