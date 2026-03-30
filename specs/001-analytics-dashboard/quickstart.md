# Quickstart: E-Commerce Analytics Dashboard

**Branch**: `001-analytics-dashboard` | **Date**: 2026-03-29

## Prerequisites

- Python 3.11+
- `uv` package manager installed (`pip install uv` or via installer)
- Repository cloned and checked out to `001-analytics-dashboard` branch

## Setup

```bash
# Install dependencies
uv pip install -r requirements.txt
```

## Run the Dashboard

```bash
streamlit run app.py
```

The dashboard opens at `http://localhost:8501` in your default browser.

## Validate It Works

With `data/sales-data.csv` loaded (no filters applied), confirm:

- [ ] Four KPI cards visible in a row at the top
- [ ] Total Orders reads **482**
- [ ] Total Sales reads between **$650,000 and $700,000**
- [ ] Monthly trend line chart shows **12 data points** (Jan–Dec 2024)
- [ ] Category bar chart shows **5 bars**, sorted highest to lowest
- [ ] Regional bar chart shows **4 bars**, sorted highest to lowest
- [ ] No error messages or warnings displayed (assuming clean CSV)

## Test the Filters

1. Set the date range to **Jan 2024 – Mar 2024** → KPIs and all charts update to Q1 data
2. Select **Electronics** in the category filter → charts reflect Electronics only
3. Clear all filters → values return to full-dataset totals

## Run Smoke Tests

```bash
pytest tests/test_smoke.py -v
```

All three tests should pass:
- `test_data_loads` — CSV loads without error, returns correct row count
- `test_kpis_compute` — KPI functions return expected types and non-zero values
- `test_charts_render` — chart functions return valid Plotly figure objects

## Deploy to Streamlit Community Cloud

1. Push `app.py`, `requirements.txt`, and `data/sales-data.csv` to the `main` branch
2. Log in to [share.streamlit.io](https://share.streamlit.io)
3. Click **New app** → select this repository → set main file to `app.py` → deploy
4. No secrets required (CSV-only data source)

## Troubleshooting

| Symptom | Likely cause | Fix |
|---------|-------------|-----|
| `ModuleNotFoundError: streamlit` | Dependencies not installed | Run `uv pip install -r requirements.txt` |
| `FileNotFoundError: data/sales-data.csv` | Wrong working directory | Run `streamlit run app.py` from repo root |
| KPIs show $0 or 0 | Filter leaves no matching rows | Clear all filters and retry |
| Data quality banner appears | CSV has missing values | Expected behavior; banner reports skipped rows |
| Column missing error | CSV schema mismatch | Verify CSV has all required columns (see data-model.md) |
