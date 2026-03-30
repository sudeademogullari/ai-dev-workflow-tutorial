# Research: E-Commerce Analytics Dashboard

**Branch**: `001-analytics-dashboard` | **Date**: 2026-03-29
**Phase**: 0 — Technology decisions and architectural research

## Decision Log

### 1. Project Structure

**Decision**: Single file (`app.py`) at repository root.

**Rationale**: The dashboard has one screen, one data source, and four chart components.
A single file eliminates import complexity, is the conventional Streamlit starting point,
and makes the codebase immediately readable for the tutorial audience. Refactoring to
modules is straightforward if the file grows beyond ~300 lines.

**Alternatives considered**:
- Two files (`app.py` + `data.py`): adds value only once data logic exceeds ~50 lines;
  premature for Phase 1.
- Modular layout (`components/`, `data/`): appropriate for multi-page apps; overkill here.
- Full Python package (`src/` layout): adds packaging overhead with no runtime benefit
  for a Streamlit app.

---

### 2. Data Caching

**Decision**: No caching — CSV reloaded on each Streamlit rerun.

**Rationale**: The dataset is 482 rows (~50KB). On modern hardware, Pandas reads this
in under 50ms. Adding `@st.cache_data` introduces cache-invalidation edge cases (stale
data after file changes) with no perceptible performance benefit at this scale.

**Alternatives considered**:
- `@st.cache_data` (standard): correct choice for larger datasets or remote data sources;
  unnecessary overhead here.
- `st.session_state` manual caching: more complex than `@st.cache_data`, no advantage.
- TTL cache (5-minute refresh): only relevant when a live data source exists (Phase 2).

**Revisit trigger**: If dataset grows beyond ~10,000 rows or a live API is introduced
(Phase 2), add `@st.cache_data(ttl=300)` to the load function.

---

### 3. Filter Panel Layout

**Decision**: Horizontal filter bar in a single row above the KPI cards (top bar).

**Rationale**: A top-bar layout keeps the full main area available for charts and KPIs,
avoids the sidebar taking permanent horizontal space, and matches the PRD's wireframe
intent of a clean executive-facing layout. Three filter controls (date range, category
multi-select, region multi-select) fit comfortably in a 3-column Streamlit row.

**Implementation**: Use `st.columns(3)` to place date range, category, and region
selectors side by side above `st.columns(2)` for the KPI row.

**Alternatives considered**:
- Sidebar: reduces main area width; acceptable for analyst tools but not ideal for
  executive dashboards meant to be projected.
- Inline per-chart filters: adds cognitive load; user must hunt for filter controls.
- Collapsible top panel: adds interaction step before filtering is possible.

---

### 4. Deployment Layout

**Decision**: Flat root — `app.py`, `requirements.txt`, `data/sales-data.csv` at
repository root.

**Rationale**: Streamlit Community Cloud defaults to discovering `app.py` at the repo
root with no configuration. A flat layout requires zero deploy configuration and matches
the tutorial's goal of a frictionless deployment experience.

**Alternatives considered**:
- `dashboard/` subdirectory: requires setting a custom main file path in Streamlit deploy
  settings — adds a configuration step with no structural benefit.
- Separate repo: cleanest separation but requires participants to manage two repos;
  increases setup friction for a tutorial audience.

---

### 5. Data Quality Handling

**Decision**: Best-effort imputation (`total_amount = quantity × unit_price` when
`total_amount` is missing), skip unrecoverable rows, display banner with skip count.

**Rationale**: Aligns with FR-007. Imputation recovers the most common data gap (missing
computed column) without introducing statistical bias. Transparent skip reporting
satisfies Constitution Principle III (no silent data failures).

**Implementation**: Apply imputation in a dedicated `clean_data(df)` function within
`app.py`. Count skipped rows, store in a variable, render `st.warning()` banner if
count > 0.

---

### 6. Testing Approach

**Decision**: pytest smoke tests in `tests/test_smoke.py`.

**Rationale**: Constitution Principle V mandates smoke tests only. Three tests cover
the required surface: (1) CSV loads without error, (2) KPI computation functions return
expected types/values, (3) chart-building functions return Plotly figure objects.

**Alternatives considered**:
- No tests: violates Constitution Principle V.
- Full unit test suite: over-engineered for a single-file app at this stage.
- Playwright/Selenium UI tests: appropriate for integration testing but far exceeds
  the smoke test mandate.
