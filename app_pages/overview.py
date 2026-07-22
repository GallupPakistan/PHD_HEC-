"""
pages/overview.py
Landing page: five KPI cards, top universities, discipline distribution,
year trend, top subjects, and a quick insights panel.
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

    render_page_header(
        title="Overview",
        subtitle="A consolidated summary of PhD records across universities, disciplines, subjects, and years.",
        breadcrumb="Home / Overview",
        last_updated=get_last_updated(),
    )

    total_records = int(university["Records"].sum())

    kpis = [
        {"icon": "school", "label": "Total Universities", "value": len(university),
         "description": "Institutions with recorded data"},
        {"icon": "category", "label": "Total Disciplines", "value": len(discipline),
         "description": "Distinct discipline categories"},
        {"icon": "menu_book", "label": "Total Subjects", "value": len(subject),
         "description": "Distinct subject categories"},
        {"icon": "calendar_month", "label": "Years Covered", "value": len(year),
         "description": f"{int(year['Year'].min())} – {int(year['Year'].max())}"},
        {"icon": "workspace_premium", "label": "Total PhD Records", "value": total_records,
         "description": "Across all universities"},
    ]
    render_kpi_row(kpis)

    st.write("")
    col1, col2 = st.columns(2)
    with col1:
        section_card_start("Top Universities")
        charts.render(charts.horizontal_bar(university, x="Records", y="University", top_n=10))
        section_card_end()
    with col2:
        section_card_start("Discipline Distribution")
        charts.render(charts.donut_chart(discipline, names="Discipline", values="Records", top_n=8))
        section_card_end()

    st.write("")
    col3, col4 = st.columns(2)
    with col3:
        section_card_start("Year Trend")
        charts.render(charts.line_chart(year, x="Year", y="Records"))
        section_card_end()
    with col4:
        section_card_start("Top Subjects")
        charts.render(charts.horizontal_bar(subject, x="Records", y="Subject", top_n=10))
        section_card_end()

    st.write("")
    render_insights_panel("Quick Insights", compute_overview_insights(data))
