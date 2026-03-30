import pandas as pd
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
