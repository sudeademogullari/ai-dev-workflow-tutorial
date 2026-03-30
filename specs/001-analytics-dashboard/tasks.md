---
description: "Task list for E-Commerce Analytics Dashboard"
---

# Tasks: E-Commerce Analytics Dashboard

**Input**: Design documents from `specs/001-analytics-dashboard/`
**Prerequisites**: plan.md ✅ spec.md ✅ research.md ✅ data-model.md ✅ quickstart.md ✅

**Tests**: Smoke test tasks included (at end of implementation per user request).

**Organization**: Visual-first sequencing — get something on screen fast, then add
interactivity, data quality handling last. MVP = User Stories 1–3 (read-only dashboard).

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different sections of app.py or different files)
- **[Story]**: Which user story this task belongs to (US1–US4)
- File paths shown are relative to repository root

---

## Phase 1: Setup

**Purpose**: Create project files and directory structure.

- [x] T001 Create `app.py` at repository root with a Streamlit page config (title "ShopSmart Sales Dashboard", wide layout)
- [x] T002 Create `requirements.txt` at repository root with pinned versions: `streamlit`, `plotly`, `pandas`
- [x] T003 [P] Create `tests/test_smoke.py` at repository root with three empty test stubs: `test_data_loads`, `test_kpis_compute`, `test_charts_render`

---

## Phase 2: Foundational — Data Loading

**Purpose**: CSV loading and cleaning infrastructure that ALL user stories depend on.

**⚠️ CRITICAL**: No user story work can begin until this phase is complete.

- [x] T004 Implement `load_data()` function in `app.py` that reads `data/sales-data.csv` using pandas, validates all required columns are present (`date`, `order_id`, `category`, `region`, `quantity`, `unit_price`, `total_amount`), and raises a descriptive error if any column is missing (FR-008)
- [x] T005 Implement `clean_data(df)` function in `app.py` that imputes missing `total_amount` as `quantity × unit_price`, drops rows where imputation is impossible, and returns a tuple `(clean_df, rows_skipped)` (FR-007)

**Checkpoint**: `load_data()` and `clean_data()` work correctly — run `python -c "import app"` without errors before proceeding.

---

## Phase 3: User Story 1 — Executive KPI Overview (Priority: P1) 🎯

**Goal**: Four KPI scorecards visible in a single row with correct values from the full dataset.

**Independent Test**: Run the app, confirm all four KPI cards render with correct values
(Total Orders = 482, Total Sales $650K–$700K, AOV and Top Category non-zero).

### Implementation for User Story 1

- [x] T006 Implement `compute_kpis(df)` function in `app.py` that returns a dict with `total_sales`, `total_orders`, `avg_order_value`, and `top_category` (name + value) computed from the filtered DataFrame (FR-001)
- [x] T007 [P] [US1] Add Total Sales KPI card to `app.py` using `st.metric()` with currency formatting `$X,XXX,XXX.XX` (FR-002)
- [x] T008 [P] [US1] Add Total Orders KPI card to `app.py` using `st.metric()` with comma-separated integer formatting (FR-002)
- [x] T009 [P] [US1] Add Average Order Value KPI card to `app.py` using `st.metric()` with currency formatting `$X,XXX.XX` (FR-002)
- [x] T010 [P] [US1] Add Top Category KPI card to `app.py` using `st.metric()` showing category name as label and revenue as value (FR-002)
- [x] T011 [US1] Arrange all four KPI cards in a single horizontal row using `st.columns(4)` in `app.py`, positioned below the page title (FR-001)

**Checkpoint**: App loads and displays four KPI cards with correct values. MVP partial.

---

## Phase 4: User Story 2 — Sales Trend Over Time (Priority: P1)

**Goal**: Monthly line chart showing 12 months of sales data with interactive tooltips.

**Independent Test**: Confirm the line chart renders 12 data points (Jan–Dec 2024) with
correct monthly totals and currency-formatted y-axis.

### Implementation for User Story 2

- [x] T012 [US2] Implement `compute_monthly_trend(df)` function in `app.py` that groups transactions by calendar month, sums `total_amount`, sorts ascending, and returns a DataFrame with columns `month` and `total_sales` (FR-003)
- [x] T013 [US2] Implement `build_trend_chart(monthly_df)` function in `app.py` that returns a Plotly line chart with month-name x-axis labels, currency-formatted y-axis, and hover tooltips showing month and exact sales value (FR-003)
- [x] T014 [US2] Render the trend chart in `app.py` below the KPI row using `st.plotly_chart()` with `use_container_width=True` (FR-003)

**Checkpoint**: App displays trend line chart. Both P1 user stories complete. MVP partial.

---

## Phase 5: User Story 3 — Category & Regional Breakdowns (Priority: P2) 🏁 MVP

**Goal**: Two bar charts side by side — sales by category and sales by region, both sorted
descending with interactive tooltips.

**Independent Test**: Confirm category chart shows 5 bars and regional chart shows 4 bars,
both sorted highest to lowest with correct values from the full dataset.

### Implementation for User Story 3

- [x] T015 [P] [US3] Implement `compute_category_breakdown(df)` function in `app.py` that groups by `category`, sums `total_amount`, and sorts descending (FR-004)
- [x] T016 [P] [US3] Implement `compute_regional_breakdown(df)` function in `app.py` that groups by `region`, sums `total_amount`, and sorts descending (FR-005)
- [x] T017 [P] [US3] Implement `build_category_chart(category_df)` function in `app.py` that returns a Plotly horizontal bar chart with currency-formatted values and hover tooltips (FR-004)
- [x] T018 [P] [US3] Implement `build_regional_chart(regional_df)` function in `app.py` that returns a Plotly horizontal bar chart with currency-formatted values and hover tooltips (FR-005)
- [x] T019 [US3] Render category and regional charts side by side using `st.columns(2)` in `app.py`, each with `st.plotly_chart()` and `use_container_width=True` (FR-004, FR-005)

**Checkpoint**: Full read-only dashboard complete and shippable. ✅ MVP REACHED.
Stop here to validate and demo before proceeding to filters.

---

## Phase 6: User Story 4 — Interactive Filtering (Priority: P2)

**Goal**: Three-column filter bar above KPI row — date range, category multi-select, region
multi-select — that updates all charts and KPIs without a full page reload.

**Independent Test**: Set date range to Jan–Mar 2024, select one category; confirm all four
KPIs and all three charts update to reflect only matching transactions (FR-006).

### Implementation for User Story 4

- [x] T020 [US4] Add a three-column filter bar to `app.py` using `st.columns(3)` positioned above the KPI row, containing: (col1) `st.date_input` for date range with dataset min/max as defaults, (col2) `st.multiselect` for categories populated from distinct values in the data, (col3) `st.multiselect` for regions populated from distinct values in the data (FR-006)
- [x] T021 [US4] Implement `apply_filters(df, date_start, date_end, categories, regions)` function in `app.py` that filters the cleaned DataFrame by the active filter state (date range, then categories, then regions) and returns the filtered DataFrame (FR-006)
- [x] T022 [US4] Wire filter state into `app.py` main flow so that `apply_filters()` runs after `clean_data()` and the filtered DataFrame is passed to all KPI and chart functions (FR-006)

**Checkpoint**: Filters update all KPIs and charts correctly. All four user stories complete.

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Data quality transparency, empty states, and layout refinement.

- [x] T023 Add data quality banner to `app.py`: render `st.warning(f"{rows_skipped} row(s) excluded due to unrecoverable missing data.")` above the filter bar whenever `rows_skipped > 0` (FR-007)
- [x] T024 [P] Add empty-state handling to `app.py`: when the filtered DataFrame has zero rows, display `st.info("No data matches the selected filters.")` in place of all charts and show zero values in all KPI cards (FR-009)
- [x] T025 [P] Add dashboard header to `app.py`: `st.title("ShopSmart Sales Dashboard")` and a subtitle line showing the active date range of the loaded data

---

## Phase 8: Smoke Tests

**Purpose**: Verify the three required smoke test scenarios pass before deployment.

- [x] T026 Implement `test_data_loads` in `tests/test_smoke.py`: call `load_data()` and assert the returned DataFrame has 482 rows and all required columns present
- [x] T027 [P] Implement `test_kpis_compute` in `tests/test_smoke.py`: call `compute_kpis()` on the full dataset and assert `total_orders == 482`, `total_sales` is between 650000 and 700000, `avg_order_value > 0`, and `top_category` is a non-empty string
- [x] T028 [P] Implement `test_charts_render` in `tests/test_smoke.py`: call `build_trend_chart()`, `build_category_chart()`, and `build_regional_chart()` and assert each returns a Plotly Figure object with at least one trace

**Checkpoint**: Run `pytest tests/test_smoke.py -v` — all three tests pass before deploying.

---

## Phase 9: Deployment Validation

**Purpose**: Confirm the app is ready for Streamlit Community Cloud.

- [x] T029 Verify `requirements.txt` has pinned versions for all imports used in `app.py` (streamlit, plotly, pandas); add any missing packages (Constitution Principle IV)
- [x] T030 Run through the `specs/001-analytics-dashboard/quickstart.md` validation checklist manually — confirm all seven checkboxes pass with the sample CSV

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies — start immediately
- **Foundational (Phase 2)**: Depends on Phase 1 — BLOCKS all user stories
- **US1 (Phase 3)**: Depends on Foundational — no dependency on US2/US3/US4
- **US2 (Phase 4)**: Depends on Foundational — no dependency on US1/US3/US4
- **US3 (Phase 5)**: Depends on Foundational — no dependency on US1/US2/US4
- **US4 (Phase 6)**: Depends on US1+US2+US3 being complete (filters wrap all charts/KPIs)
- **Polish (Phase 7)**: Depends on US4 complete
- **Smoke Tests (Phase 8)**: Depends on Polish complete
- **Deployment (Phase 9)**: Depends on Smoke Tests passing

### User Story Dependencies

- **US1 (P1)** and **US2 (P1)**: Both can start independently after Foundational
- **US3 (P2)**: Can start after Foundational, independent of US1/US2
- **US4 (P2)**: Must wait for US1+US2+US3 (filters govern all charts and KPIs)

### Within Each User Story

- Compute functions before chart-building functions
- Chart-building functions before rendering calls
- All functions before wiring into main app flow

### Parallel Opportunities

- T007, T008, T009, T010 (KPI cards) — all touch different `st.metric()` calls
- T015, T016, T017, T018 (breakdown compute + chart functions) — all in separate functions
- T027, T028 (smoke test implementations) — independent test functions
- T023, T024, T025 (polish) — independent concerns

---

## Parallel Example: User Story 3

```bash
# Launch all four breakdown tasks simultaneously:
Task: "Implement compute_category_breakdown(df) in app.py"     # T015
Task: "Implement compute_regional_breakdown(df) in app.py"     # T016
Task: "Implement build_category_chart(category_df) in app.py"  # T017
Task: "Implement build_regional_chart(regional_df) in app.py"  # T018
# Then sequentially:
Task: "Render both charts side by side in app.py"              # T019
```

---

## Implementation Strategy

### MVP First (User Stories 1–3 only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL — blocks all stories)
3. Complete Phase 3: US1 — KPI cards visible ✅
4. Complete Phase 4: US2 — Trend chart visible ✅
5. Complete Phase 5: US3 — Category + regional charts visible ✅
6. **STOP AND VALIDATE**: Full read-only dashboard working — demo or deploy
7. Proceed to US4 (filters) only after MVP is confirmed

### Incremental Delivery

1. Setup + Foundational → data loads correctly
2. US1 → four KPI cards on screen (first visible output)
3. US2 → trend line chart added
4. US3 → breakdown charts added → **MVP complete**
5. US4 → filters added → full interactive feature
6. Polish + Tests + Deployment → production-ready

---

## Notes

- All tasks target a single file (`app.py`) — use function boundaries to keep sections navigable
- `[P]` tasks within a user story phase can be implemented in any order
- Each user story phase ends with a checkpoint — validate independently before moving on
- Smoke tests (Phase 8) MUST pass before deployment (Constitution Principle V)
- No secrets required — CSV-only data source means Streamlit Community Cloud deploy needs no configuration beyond pointing to `app.py`
