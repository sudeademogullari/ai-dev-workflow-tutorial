import datetime
import sys
from unittest.mock import MagicMock

import plotly.graph_objects as go

# ---------------------------------------------------------------------------
# Mock streamlit before importing app so that page-config, widget calls, and
# metric/chart renders are all no-ops.  Must happen before `import app`.
# ---------------------------------------------------------------------------
_st = MagicMock()
_ctx = MagicMock()
_ctx.__enter__ = MagicMock(return_value=_ctx)
_ctx.__exit__ = MagicMock(return_value=False)
_st.columns.side_effect = lambda n, *a, **kw: [_ctx] * n
_st.multiselect.return_value = []
_st.date_input.return_value = (datetime.date(2024, 1, 1), datetime.date(2024, 12, 31))
sys.modules["streamlit"] = _st

from app import (  # noqa: E402
    REQUIRED_COLUMNS,
    build_category_chart,
    build_regional_chart,
    build_trend_chart,
    clean_data,
    compute_category_breakdown,
    compute_kpis,
    compute_monthly_trend,
    compute_regional_breakdown,
    load_data,
)


def test_data_loads():
    df = load_data()
    assert len(df) == 482
    assert REQUIRED_COLUMNS.issubset(set(df.columns))


def test_kpis_compute():
    df_clean, _ = clean_data(load_data())
    kpis = compute_kpis(df_clean)
    assert kpis["total_orders"] == 482
    assert 650_000 <= kpis["total_sales"] <= 700_000
    assert kpis["avg_order_value"] > 0
    assert isinstance(kpis["top_category_name"], str) and kpis["top_category_name"]


def test_charts_render():
    df_clean, _ = clean_data(load_data())

    trend_fig = build_trend_chart(compute_monthly_trend(df_clean))
    assert isinstance(trend_fig, go.Figure)
    assert len(trend_fig.data) >= 1

    category_fig = build_category_chart(compute_category_breakdown(df_clean))
    assert isinstance(category_fig, go.Figure)
    assert len(category_fig.data) >= 1

    regional_fig = build_regional_chart(compute_regional_breakdown(df_clean))
    assert isinstance(regional_fig, go.Figure)
    assert len(regional_fig.data) >= 1
