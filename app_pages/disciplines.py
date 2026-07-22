"""
pages/disciplines.py
Detail page for discipline-level PhD record data.
"""

import streamlit as st

from components.cards import section_card_start, section_card_end, render_page_header
from components.kpis import render_kpi_row
from components import charts
from components.tables import render_table
from utils.loader import get_last_updated


def render(data: dict) -> None:
    discipline = data["discipline"]

    render_page_header(
        title="Disciplines",
        subtitle="Breakdown of PhD records by academic discipline.",
        breadcrumb="Home / Disciplines",
        last_updated=get_last_updated(),
    )

    kpis = [
        {"icon": "category", "label": "Total Disciplines", "value": len(discipline),
         "description": "Distinct discipline categories"},
        {"icon": "trending_up", "label": "Largest Discipline", "value": int(discipline["Records"].max()),
         "description": discipline.iloc[0]["Discipline"][:32]},
        {"icon": "trending_down", "label": "Smallest Discipline", "value": int(discipline["Records"].min()),
         "description": discipline.iloc[-1]["Discipline"][:32]},
        {"icon": "functions", "label": "Average", "value": discipline["Records"].mean(),
         "description": "Mean records per discipline"},
    ]
    render_kpi_row(kpis)

    st.write("")
    col1, col2 = st.columns(2)
    with col1:
        section_card_start("Discipline Distribution")
        charts.render(charts.donut_chart(discipline, names="Discipline", values="Records", top_n=len(discipline)))
        section_card_end()
    with col2:
        section_card_start("All Disciplines — Ranked")
        charts.render(charts.horizontal_bar(discipline, x="Records", y="Discipline", top_n=len(discipline)))
        section_card_end()

    st.write("")
    section_card_start("Treemap — Share of Records")
    charts.render(charts.treemap_chart(discipline, path="Discipline", values="Records"))
    section_card_end()

    st.write("")
    section_card_start("Discipline Records — Table")
    render_table(discipline, key="disciplines_table")
    section_card_end()
