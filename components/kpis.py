"""
kpis.py
Renders KPI card rows: an icon, a label, a large number, and a short
description, styled to match an enterprise BI dashboard.
"""

from typing import List, Dict
import streamlit as st
from utils.helpers import format_number


def render_kpi_row(kpis: List[Dict]) -> None:
    """Renders a horizontal row of KPI cards.

    Each kpi dict must contain: icon, label, value, description.
    """
    cols = st.columns(len(kpis))
    for col, kpi in zip(cols, kpis):
        with col:
            value = kpi["value"]
            display_value = format_number(value) if isinstance(value, (int, float)) else value
            st.markdown(
                f"""
                <div class="bi-card">
                    <span class="kpi-icon material-symbols-outlined">{kpi['icon']}</span>
                    <div class="kpi-label">{kpi['label']}</div>
                    <div class="kpi-value">{display_value}</div>
                    <div class="kpi-desc">{kpi['description']}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
