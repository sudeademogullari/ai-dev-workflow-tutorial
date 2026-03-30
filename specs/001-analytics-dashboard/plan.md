# Implementation Plan: E-Commerce Analytics Dashboard

**Branch**: `001-analytics-dashboard` | **Date**: 2026-03-29 | **Spec**: [spec.md](spec.md)
**Input**: Feature specification from `specs/001-analytics-dashboard/spec.md`

## Summary

Build a single-page Streamlit dashboard that loads sales data from a CSV file, displays
four KPI scorecards (Total Sales, Total Orders, Average Order Value, Top Category), a
monthly sales trend line chart, category and regional bar charts, and a horizontal
filter bar (date range, category, region). The app is a single file (`app.py`) deployed
flat at the repository root to Streamlit Community Cloud.

## Technical Context

**Language/Version**: Python 3.11+
**Primary Dependencies**: Streamlit, Plotly, Pandas
**Storage**: CSV file (`data/sales-data.csv`) — no database
**Testing**: pytest (smoke tests only — app loads, charts render, data loads)
**Target Platform**: Streamlit Community Cloud (Linux, modern browsers)
**Project Type**: Single-file web application
**Performance Goals**: Dashboard interactive within 5 seconds; filter updates under 2 seconds
**Constraints**: No caching (CSV is small — 482 rows); no authentication; desktop-only (1280px+)
**Scale/Scope**: Single user session; ~482 transaction rows; 5 categories; 4 regions

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Status | Notes |
|-----------|--------|-------|
| I. Audience-First Design | ✅ PASS | All 4 user stories name a target audience (exec, CEO, marketing, regional, analysts) |
| II. Real-Time Data by Default | ⚠️ SCOPED OUT | Real-time DB integration is explicitly deferred to Phase 2 in spec. CSV-only is the graceful fallback mode. No caching chosen — acceptable for 482-row file. |
| III. Multi-Source Data Integrity | ✅ PASS | Single source (CSV) eliminates reconciliation risk; data quality banner required by FR-007 |
| IV. Public-Safe Deployment | ✅ PASS | No secrets needed (CSV only); flat root deployment to Streamlit Community Cloud |
| V. Minimal Testing Discipline | ✅ PASS | Smoke tests only; pytest verifies app loads, data loads, chart functions run |

**Gate decision**: Proceed. Principle II deviation is justified — real-time is Phase 2 scope.
Re-check after Phase 1 design confirms no new violations.

## Project Structure

### Documentation (this feature)

```text
specs/001-analytics-dashboard/
├── plan.md              # This file
├── research.md          # Phase 0 output
├── data-model.md        # Phase 1 output
├── quickstart.md        # Phase 1 output
├── checklists/
│   └── requirements.md  # Spec quality checklist
└── tasks.md             # Phase 2 output (/speckit.tasks — NOT created here)
```

### Source Code (repository root)

```text
app.py                   # Single-file Streamlit application (all UI + logic)
requirements.txt         # Pinned Python dependencies
data/
└── sales-data.csv       # Source dataset (482 rows, 12 months 2024)
tests/
└── test_smoke.py        # Smoke tests: data loads, KPIs compute, charts render
```

**Structure Decision**: Single flat root layout. `app.py` contains all Streamlit UI,
data loading, KPI calculations, chart rendering, and filter logic. No subdirectories
for source code — consistent with the single-file architecture choice and Streamlit
Community Cloud's default deploy-from-root convention.

## Complexity Tracking

| Deviation | Why Accepted | Simpler Alternative Rejected Because |
|-----------|-------------|--------------------------------------|
| No `@st.cache_data` | CSV is 482 rows; reload cost is negligible; avoids cache invalidation edge cases | Caching adds complexity with no measurable benefit at this data volume |
| Real-time data deferred | Phase 2 scope per spec; CSV fallback satisfies current stakeholder needs | Live API integration requires secrets, schema contracts, and reconciliation logic not yet designed |
