import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(
    page_title="ShopSmart Sales Dashboard",
    layout="wide",
)

REQUIRED_COLUMNS = {
    "date", "order_id", "category", "region",
    "quantity", "unit_price", "total_amount",
}


def load_data() -> pd.DataFrame:
    """Load sales-data.csv and validate required columns are present (FR-008)."""
    df = pd.read_csv("data/sales-data.csv")
    missing = REQUIRED_COLUMNS - set(df.columns)
    if missing:
        raise ValueError(
            f"CSV is missing required column(s): {', '.join(sorted(missing))}. "
            "Please check your data/sales-data.csv file."
        )
    df["date"] = pd.to_datetime(df["date"])
    return df


def clean_data(df: pd.DataFrame) -> tuple[pd.DataFrame, int]:
    """Impute missing total_amount and drop unrecoverable rows (FR-007).

    Returns:
        clean_df: DataFrame with total_amount populated for all rows.
        rows_skipped: Count of rows dropped due to unrecoverable missing data.
    """
    df = df.copy()
    missing_amount = df["total_amount"].isna()
    df.loc[missing_amount, "total_amount"] = (
        df.loc[missing_amount, "quantity"] * df.loc[missing_amount, "unit_price"]
    )
    unrecoverable = df["total_amount"].isna()
    rows_skipped = int(unrecoverable.sum())
    clean_df = df[~unrecoverable].reset_index(drop=True)
    return clean_df, rows_skipped


def compute_kpis(df: pd.DataFrame) -> dict:
    """Compute the four KPI values from the (filtered) DataFrame (FR-001)."""
    if df.empty:
        return {
            "total_sales": 0.0,
            "total_orders": 0,
            "avg_order_value": 0.0,
            "top_category_name": "No data",
            "top_category_value": 0.0,
        }
    total_sales = df["total_amount"].sum()
    total_orders = df["order_id"].nunique()
    avg_order_value = total_sales / total_orders if total_orders else 0.0
    category_sales = df.groupby("category")["total_amount"].sum()
    top_category_name = category_sales.idxmax()
    top_category_value = category_sales.max()
    return {
        "total_sales": total_sales,
        "total_orders": total_orders,
        "avg_order_value": avg_order_value,
        "top_category_name": top_category_name,
        "top_category_value": top_category_value,
    }


def compute_monthly_trend(df: pd.DataFrame) -> pd.DataFrame:
    """Group transactions by calendar month and sum total_amount (FR-003).

    Returns a DataFrame with columns 'month' (period start) and 'total_sales',
    sorted ascending. Months with zero sales are included (filled with 0).
    """
    if df.empty:
        return pd.DataFrame(columns=["month", "total_sales"])
    monthly = (
        df.groupby(pd.Grouper(key="date", freq="MS"))["total_amount"]
        .sum()
        .reset_index()
        .rename(columns={"date": "month", "total_amount": "total_sales"})
    )
    monthly = monthly.sort_values("month").reset_index(drop=True)
    return monthly


def build_trend_chart(monthly_df: pd.DataFrame):
    """Return a Plotly line chart of monthly sales with tooltips (FR-003)."""
    monthly_df = monthly_df.copy()
    monthly_df["month_label"] = monthly_df["month"].dt.strftime("%b %Y")
    fig = px.line(
        monthly_df,
        x="month_label",
        y="total_sales",
        markers=True,
        labels={"month_label": "Month", "total_sales": "Sales ($)"},
        title="Sales Trend Over Time",
    )
    fig.update_traces(
        hovertemplate="<b>%{x}</b><br>Sales: $%{y:,.2f}<extra></extra>",
    )
    fig.update_yaxes(tickprefix="$", tickformat=",.0f")
    fig.update_layout(
        xaxis_title=None,
        yaxis_title="Sales ($)",
        hovermode="x unified",
        margin=dict(t=40, b=0),
    )
    return fig


def compute_category_breakdown(df: pd.DataFrame) -> pd.DataFrame:
    """Group by category, sum total_amount, sort descending (FR-004)."""
    if df.empty:
        return pd.DataFrame(columns=["category", "total_sales"])
    return (
        df.groupby("category")["total_amount"]
        .sum()
        .reset_index()
        .rename(columns={"total_amount": "total_sales"})
        .sort_values("total_sales", ascending=False)
        .reset_index(drop=True)
    )


def compute_regional_breakdown(df: pd.DataFrame) -> pd.DataFrame:
    """Group by region, sum total_amount, sort descending (FR-005)."""
    if df.empty:
        return pd.DataFrame(columns=["region", "total_sales"])
    return (
        df.groupby("region")["total_amount"]
        .sum()
        .reset_index()
        .rename(columns={"total_amount": "total_sales"})
        .sort_values("total_sales", ascending=False)
        .reset_index(drop=True)
    )


def build_category_chart(category_df: pd.DataFrame):
    """Return a Plotly horizontal bar chart of sales by category (FR-004)."""
    fig = px.bar(
        category_df,
        x="total_sales",
        y="category",
        orientation="h",
        title="Sales by Category",
        labels={"total_sales": "Sales ($)", "category": "Category"},
    )
    fig.update_traces(
        hovertemplate="<b>%{y}</b><br>Sales: $%{x:,.2f}<extra></extra>",
    )
    fig.update_xaxes(tickprefix="$", tickformat=",.0f")
    fig.update_yaxes(categoryorder="total ascending")
    fig.update_layout(margin=dict(t=40, b=0))
    return fig


def build_regional_chart(regional_df: pd.DataFrame):
    """Return a Plotly horizontal bar chart of sales by region (FR-005)."""
    fig = px.bar(
        regional_df,
        x="total_sales",
        y="region",
        orientation="h",
        title="Sales by Region",
        labels={"total_sales": "Sales ($)", "region": "Region"},
    )
    fig.update_traces(
        hovertemplate="<b>%{y}</b><br>Sales: $%{x:,.2f}<extra></extra>",
    )
    fig.update_xaxes(tickprefix="$", tickformat=",.0f")
    fig.update_yaxes(categoryorder="total ascending")
    fig.update_layout(margin=dict(t=40, b=0))
    return fig


def apply_filters(
    df: pd.DataFrame,
    date_start,
    date_end,
    categories: list,
    regions: list,
) -> pd.DataFrame:
    """Filter the cleaned DataFrame by active filter state (FR-006).

    Applies date range, then category, then region filters in order.
    Empty categories/regions lists mean no filter applied for that dimension.
    """
    mask = (df["date"].dt.date >= date_start) & (df["date"].dt.date <= date_end)
    if categories:
        mask &= df["category"].isin(categories)
    if regions:
        mask &= df["region"].isin(regions)
    return df[mask].reset_index(drop=True)


# ── Main app ──────────────────────────────────────────────────────────────────

st.title("ShopSmart Sales Dashboard")

df_raw = load_data()
df_clean, rows_skipped = clean_data(df_raw)

data_date_min = df_clean["date"].dt.date.min()
data_date_max = df_clean["date"].dt.date.max()
st.caption(
    f"Dataset covers {data_date_min.strftime('%b %d, %Y')} – {data_date_max.strftime('%b %d, %Y')}"
)

# ── Data quality banner ───────────────────────────────────────────────────────

if rows_skipped > 0:
    st.warning(f"{rows_skipped} row(s) excluded due to unrecoverable missing data.")

# ── Filter bar ────────────────────────────────────────────────────────────────

date_min = df_clean["date"].dt.date.min()
date_max = df_clean["date"].dt.date.max()
all_categories = sorted(df_clean["category"].unique().tolist())
all_regions = sorted(df_clean["region"].unique().tolist())

f_col1, f_col2, f_col3 = st.columns(3)

with f_col1:
    date_range = st.date_input(
        "Date Range",
        value=(date_min, date_max),
        min_value=date_min,
        max_value=date_max,
    )

with f_col2:
    selected_categories = st.multiselect(
        "Category", options=all_categories, default=[]
    )

with f_col3:
    selected_regions = st.multiselect(
        "Region", options=all_regions, default=[]
    )

# Handle date_input returning a single date while user is picking the range
if isinstance(date_range, (list, tuple)) and len(date_range) == 2:
    date_start, date_end = date_range
else:
    date_start = date_end = date_range[0] if date_range else date_min

df = apply_filters(df_clean, date_start, date_end, selected_categories, selected_regions)

# ── KPI cards ─────────────────────────────────────────────────────────────────

kpis = compute_kpis(df)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Sales", f"${kpis['total_sales']:,.2f}")

with col2:
    st.metric("Total Orders", f"{kpis['total_orders']:,}")

with col3:
    st.metric("Avg Order Value", f"${kpis['avg_order_value']:,.2f}")

with col4:
    st.metric(
        f"Top Category: {kpis['top_category_name']}",
        f"${kpis['top_category_value']:,.2f}",
    )

# ── Charts (empty-state guard) ────────────────────────────────────────────────

if df.empty:
    st.info("No data matches the selected filters.")
else:
    # ── Sales trend chart ─────────────────────────────────────────────────────

    monthly_df = compute_monthly_trend(df)
    st.plotly_chart(build_trend_chart(monthly_df), use_container_width=True)

    # ── Category & regional breakdowns ────────────────────────────────────────

    chart_col1, chart_col2 = st.columns(2)

    with chart_col1:
        st.plotly_chart(
            build_category_chart(compute_category_breakdown(df)),
            use_container_width=True,
        )

    with chart_col2:
        st.plotly_chart(
            build_regional_chart(compute_regional_breakdown(df)),
            use_container_width=True,
        )
