"""
pages/analytics.py
Cross-cutting analytics page: rankings, trend and distribution analysis,
and summary insights across all four datasets in one view.
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
        title="Analytics",
        subtitle="A consolidated analytical view — top rankings, trend, and distribution — for quick understanding of the full dataset.",
        breadcrumb="Home / Analytics",
        last_updated=get_last_updated(),
    )

    total_records = int(university["Records"].sum())
    yoy_growth = 0.0
    if len(year) >= 2:
        prev, last = year.iloc[-2]["Records"], year.iloc[-1]["Records"]
        if prev:
            yoy_growth = round((last - prev) / prev * 100, 1)

    kpis = [
        {"icon": "workspace_premium", "label": "Total Records", "value": total_records,
         "description": "All PhD records combined"},
        {"icon": "school", "label": "Universities", "value": len(university), "description": "Contributing institutions"},
        {"icon": "category", "label": "Disciplines", "value": len(discipline), "description": "Discipline categories"},
        {"icon": "show_chart", "label": "Latest YoY Change", "value": f"{yoy_growth}%",
         "description": "Change vs previous year"},
    ]
    render_kpi_row(kpis)

    st.write("")
    col1, col2, col3 = st.columns(3)
    with col1:
        section_card_start("Top Universities")
        charts.render(charts.horizontal_bar(university, x="Records", y="University", top_n=8))
        section_card_end()
    with col2:
        section_card_start("Top Subjects")
        charts.render(charts.horizontal_bar(subject, x="Records", y="Subject", top_n=8))
        section_card_end()
    with col3:
        section_card_start("Top Disciplines")
        charts.render(charts.horizontal_bar(discipline, x="Records", y="Discipline", top_n=8))
        section_card_end()

    st.write("")
    col4, col5 = st.columns(2)
    with col4:
        section_card_start("Trend Analysis — Records Over Years")
        charts.render(charts.line_chart(year, x="Year", y="Records"))
        section_card_end()
    with col5:
        section_card_start("Distribution Analysis — Disciplines")
        charts.render(charts.donut_chart(discipline, names="Discipline", values="Records", top_n=8))
        section_card_end()

    st.write("")
    render_insights_panel("Summary Insights", compute_overview_insights(data))
