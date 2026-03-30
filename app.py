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
