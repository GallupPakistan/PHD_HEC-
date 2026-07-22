"""
pages/years.py
Detail page for year-level PhD record trends.
"""

import streamlit as st

from components.cards import section_card_start, section_card_end, render_page_header
from components.kpis import render_kpi_row
from components import charts
from components.tables import render_table
from utils.loader import get_last_updated


def render(data: dict) -> None:
    year = data["year"]
    peak_row = year.loc[year["Records"].idxmax()]

    render_page_header(
        title="Years",
        subtitle="Trend of PhD records over time.",
        breadcrumb="Home / Years",
        last_updated=get_last_updated(),
    )

    kpis = [
        {"icon": "calendar_month", "label": "Years Covered", "value": len(year),
         "description": "Distinct years with data"},
        {"icon": "first_page", "label": "Earliest Year", "value": int(year["Year"].min()),
         "description": "First recorded year"},
        {"icon": "last_page", "label": "Latest Year", "value": int(year["Year"].max()),
         "description": "Most recent recorded year"},
        {"icon": "trending_up", "label": "Peak Year", "value": int(peak_row["Year"]),
         "description": f"{int(peak_row['Records']):,} records"},
    ]
    render_kpi_row(kpis)

    st.write("")
    col1, col2 = st.columns(2)
    with col1:
        section_card_start("Line Chart — Records Over Time")
        charts.render(charts.line_chart(year, x="Year", y="Records"))
        section_card_end()
    with col2:
        section_card_start("Area Chart — Cumulative Trend")
        charts.render(charts.area_chart(year, x="Year", y="Records"))
        section_card_end()

    st.write("")
    section_card_start("Column Chart — Records per Year")
    charts.render(charts.column_chart(year, x="Year", y="Records"))
    section_card_end()

    st.write("")
    section_card_start("Year Records — Table")
    render_table(year, key="years_table")
    section_card_end()
