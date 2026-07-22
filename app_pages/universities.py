"""
pages/universities.py
Detail page for university-level PhD record data.
"""

import streamlit as st

from components.cards import section_card_start, section_card_end, render_page_header
from components.kpis import render_kpi_row
from components import charts
from components.tables import render_table
from utils.helpers import compute_pareto
from utils.loader import get_last_updated


def render(data: dict) -> None:
    university = data["university"]

    render_page_header(
        title="Universities",
        subtitle="Distribution of PhD records across all recorded universities.",
        breadcrumb="Home / Universities",
        last_updated=get_last_updated(),
    )

    kpis = [
        {"icon": "school", "label": "Total Universities", "value": len(university),
         "description": "Institutions with recorded data"},
        {"icon": "military_tech", "label": "Highest University", "value": int(university["Records"].max()),
         "description": university.iloc[0]["University"][:32]},
        {"icon": "functions", "label": "Average Records", "value": university["Records"].mean(),
         "description": "Mean records per university"},
        {"icon": "align_vertical_center", "label": "Median", "value": university["Records"].median(),
         "description": "Median records per university"},
    ]
    render_kpi_row(kpis)

    # One chart per row from here on — each gets full width and enough
    # height to stay readable instead of being squeezed into a column.
    st.write("")
    section_card_start("Top 10 Universities")
    charts.render(charts.horizontal_bar(university, x="Records", y="University", top_n=10))
    section_card_end()

    st.write("")
    section_card_start("Treemap — Share of Records (Top 20 + Others)")
    charts.render(charts.treemap_chart(university, path="University", values="Records", top_n=20))
    section_card_end()

    st.write("")
    section_card_start("Pareto Analysis — Top 10 Universities")
    pareto_df = compute_pareto(university, "Records")
    charts.render(charts.pareto_chart(pareto_df, category="University", value="Records", cum_pct_col="CumulativePct", top_n=20))
    section_card_end()

    st.write("")
    section_card_start("University Records — Searchable Table")
    render_table(university, key="universities_table")
    section_card_end()