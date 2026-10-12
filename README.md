# Restaurant Demand & Inventory Intelligence Platform

Production-oriented foundation for restaurant demand forecasting, ingredient requirements, inventory intelligence, and purchase recommendations.

## Development contract

- Version-by-version delivery: implement → test → validate → document → commit → artifact.
- Raw data remains immutable.
- Item identity is always `item_id`; names are descriptive attributes, never merge keys.
- No random train/test split for forecasting.
- No fabricated external data, recipes, inventory, or accuracy.
- Point-in-time correctness is mandatory for features.
- Forecasts must degrade gracefully when history or required inputs are insufficient.

## Version status

| Version | Scope | Status |
|---|---|---|
| V0 | Environment & Foundation | **Complete scaffold** |
| V1 | Data Foundation | Not started |
| V2 | EDA & Business Intelligence | Not started |
| V3 | Data Integration & Feature Engine | Not started |
| V4 | Baseline & Modeling | Not started |
| V5 | Backtesting & Model Selection | Not started |
| V6 | Demand → Ingredient Engine | Not started |
| V7 | Inventory & Purchase Optimization | Not started |
| V8 | Production Forecasting API | Not started |
| V9 | Monitoring & MLOps | Not started |
| V10 | Production SaaS | Not started |

## V0 prerequisites

- Python 3.11+
- Git
- Docker Desktop (for local PostgreSQL)
- PostgreSQL 16-compatible client/server

## Windows setup

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
Copy-Item .env.example .env
docker compose up -d postgres
python scripts\health_check.py
pytest -q
```

If PowerShell blocks activation, run the health check with the venv Python directly:

```powershell
.\.venv\Scripts\python.exe scripts\health_check.py
```

## Linux/macOS

```bash
python3.11 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
cp .env.example .env
docker compose up -d postgres
python scripts/health_check.py
pytest -q
```

## V0 health check

The health check validates:

1. Python runtime
2. Required environment configuration
3. PostgreSQL connectivity
4. Database server version
5. Application logging initialization

The database password is never printed.

## Project structure

```text
restaurant-demand-inventory-intelligence/
├── configs/
├── data/
│   ├── raw/
│   ├── interim/
│   ├── normalized/
│   └── processed/
├── artifacts/
├── logs/
├── models/
├── scripts/
├── src/
│   └── restaurant_intelligence/
│       ├── config.py
│       ├── db.py
│       ├── logging_config.py
│       └── health.py
├── tests/
│   ├── unit/
│   └── integration/
├── .env.example
├── .gitignore
├── alembic.ini
├── docker-compose.yml
├── pyproject.toml
└── requirements.txt
```

## Data policy

The supplied SQL datasets are intentionally **not bundled into V0**. V1 will ingest the actual raw datasets without modifying them. Do not manufacture BOM, supplier, inventory, holiday, weather, or event records to fill gaps.

## Next gate: V1

V1 begins only after V0 passes the environment and health checks. It will create immutable raw ingestion, schema validation, duplicate analysis, null/type analysis, relationship analysis, and the first data contract.
