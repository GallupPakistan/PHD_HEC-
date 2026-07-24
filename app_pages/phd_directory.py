"""
app_pages/phd_directory.py
Combined PhD Directory page — brings all four PhD dimensions together.
"""

import streamlit as st

from components.cards import section_card_start, section_card_end, render_page_header, render_insights_panel
from components.kpis import render_kpi_row
from components import charts
from utils.helpers import compute_overview_insights
from utils.loader import get_last_updated


def render(data: dict) -> None:
    university = data["university"]
    discipline = data["discipline"]
    subject = data["subject"]
    year = data["year"]

  

    total_records = int(university["Records"].sum())
    kpis = [
        {"icon": "workspace_premium", "label": "Total PhD Records", "value": total_records,
         "description": "Across all universities"},
        {"icon": "school", "label": "Universities", "value": len(university),
         "description": "With PhD records"},
        {"icon": "category", "label": "Disciplines", "value": len(discipline),
         "description": "Discipline categories"},
        {"icon": "menu_book", "label": "Subjects", "value": len(subject),
         "description": "Distinct subjects"},
        {"icon": "calendar_month", "label": "Years Covered", "value": len(year),
         "description": f"{int(year['Year'].min())} – {int(year['Year'].max())}"},
    ]
    render_kpi_row(kpis)

    st.write("")
    col1, col2 = st.columns(2)
    with col1:
        section_card_start("Top Universities by PhD Count")
        charts.render(charts.horizontal_bar(university, x="Records", y="University", top_n=10))
        section_card_end()
    with col2:
        section_card_start("Discipline Distribution")
        charts.render(charts.donut_chart(discipline, names="Discipline", values="Records", top_n=8))
        section_card_end()

    st.write("")
    col3, col4 = st.columns(2)
    with col3:
        section_card_start("PhD Trend by Year")
        charts.render(charts.line_chart(year, x="Year", y="Records"))
        section_card_end()
    with col4:
        section_card_start("Top Subjects")
        charts.render(charts.horizontal_bar(subject, x="Records", y="Subject", top_n=10))
        section_card_end()

    st.write("")
    section_card_start("Subject Breakdown (Treemap)")
    charts.render(charts.treemap_chart(subject, path="Subject", values="Records", top_n=15))
    section_card_end()

    st.write("")
    render_insights_panel("Quick Insights", compute_overview_insights(data))