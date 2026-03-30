# Data Model: E-Commerce Analytics Dashboard

**Branch**: `001-analytics-dashboard` | **Date**: 2026-03-29

## Source Entity: Transaction

The raw record loaded from `data/sales-data.csv`. Each row represents one sales
transaction.

| Field | Type | Required | Validation | Notes |
|-------|------|----------|------------|-------|
| `date` | date | Yes | Parseable as YYYY-MM-DD | Used for monthly grouping and date filter |
| `order_id` | string | Yes | Non-empty | Used for order count (distinct) |
| `product` | string | No | — | Not used in Phase 1 charts |
| `category` | string | Yes | One of 5 known values | Used for category chart and filter |
| `region` | string | Yes | One of 4 known values | Used for regional chart and filter |
| `quantity` | integer | Yes | ≥ 1 | Used in imputation |
| `unit_price` | decimal | Yes | > 0 | Used in imputation |
| `total_amount` | decimal | Imputed | > 0 | Primary revenue field; derived if missing |

**Imputation rule**: If `total_amount` is null or missing, derive as `quantity × unit_price`.
If both `quantity` and `unit_price` are also missing, mark row as unrecoverable and skip.

**Required columns**: `date`, `order_id`, `category`, `region`, `quantity`,
`unit_price`, `total_amount`. If any required column is absent from the file header,
halt with a descriptive error (FR-008).

---

## Derived Entity: KPI

Four scorecards computed from the filtered transaction set.

| KPI | Formula | Format |
|-----|---------|--------|
| Total Sales | `SUM(total_amount)` | `$X,XXX,XXX.XX` |
| Total Orders | `COUNT(DISTINCT order_id)` | `X,XXX` (integer) |
| Average Order Value | `Total Sales ÷ Total Orders` | `$X,XXX.XX` |
| Top Category | `category WHERE SUM(total_amount) = MAX` | `"{name}: $X,XXX"` |

**Edge case**: If filtered dataset has zero rows, all KPIs display `$0.00` / `0` /
`$0.00` / `"No data"` respectively.

---

## Derived Entity: Chart Data

Three aggregated views computed from the filtered transaction set.

### Monthly Trend

| Field | Type | Notes |
|-------|------|-------|
| `month` | date (first of month) | X-axis; formatted as "Jan 2024", "Feb 2024", etc. |
| `total_sales` | decimal | Y-axis; currency formatted |

**Computation**: Group transactions by `year-month`, sum `total_amount`.
Sort ascending by month. All calendar months in the dataset's date range appear
(months with zero sales show as 0, not omitted).

### Category Breakdown

| Field | Type | Notes |
|-------|------|-------|
| `category` | string | X-axis (or bar label) |
| `total_sales` | decimal | Y-axis; currency formatted |

**Computation**: Group by `category`, sum `total_amount`. Sort descending by total_sales.

### Regional Breakdown

| Field | Type | Notes |
|-------|------|-------|
| `region` | string | X-axis (or bar label) |
| `total_sales` | decimal | Y-axis; currency formatted |

**Computation**: Group by `region`, sum `total_amount`. Sort descending by total_sales.

---

## Entity: Filter State

The user's active filter selections. All charts and KPIs are recomputed from the
filtered transaction DataFrame on each Streamlit rerun.

| Field | Type | Default | Behavior when default |
|-------|------|---------|-----------------------|
| `date_start` | date | Min date in dataset | No lower bound applied |
| `date_end` | date | Max date in dataset | No upper bound applied |
| `selected_categories` | list[string] | All categories | No category filter applied |
| `selected_regions` | list[string] | All regions | No region filter applied |

**Filter application order**:
1. Apply date range: `date_start ≤ transaction.date ≤ date_end`
2. Apply category filter (if not all selected): `transaction.category IN selected_categories`
3. Apply region filter (if not all selected): `transaction.region IN selected_regions`
4. Compute all KPIs and chart data from the resulting filtered DataFrame

---

## Data Quality State

Tracks rows excluded during loading and cleaning.

| Field | Type | Notes |
|-------|------|-------|
| `total_rows_read` | integer | Raw row count from CSV |
| `rows_imputed` | integer | Rows where `total_amount` was derived |
| `rows_skipped` | integer | Rows dropped (unrecoverable) |
| `clean_rows` | integer | `total_rows_read - rows_skipped` |

**Display rule**: If `rows_skipped > 0`, render `st.warning(f"{rows_skipped} rows were
excluded due to missing data and could not be recovered.")` above the KPI row.
