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


# ── Main app ──────────────────────────────────────────────────────────────────

st.title("ShopSmart Sales Dashboard")

df_raw = load_data()
df, rows_skipped = clean_data(df_raw)

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

# ── Sales trend chart ─────────────────────────────────────────────────────────

monthly_df = compute_monthly_trend(df)
st.plotly_chart(build_trend_chart(monthly_df), use_container_width=True)
