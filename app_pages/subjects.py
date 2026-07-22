"""
pages/subjects.py
Detail page for subject-level PhD record data. Never uses a pie/donut
chart here since there are hundreds of subject categories.
"""

import streamlit as st

from components.cards import section_card_start, section_card_end, render_page_header
from components.kpis import render_kpi_row
from components import charts
from components.tables import render_table
from utils.loader import get_last_updated


def render(data: dict) -> None:
    subject = data["subject"]

    render_page_header(
        title="Subjects",
        subtitle="Breakdown of PhD records by subject. Hundreds of categories — ranked views only, no pie chart.",
        breadcrumb="Home / Subjects",
        last_updated=get_last_updated(),
    )

    kpis = [
        {"icon": "menu_book", "label": "Total Subjects", "value": len(subject),
         "description": "Distinct subject categories"},
        {"icon": "military_tech", "label": "Largest Subject", "value": int(subject["Records"].max()),
         "description": subject.iloc[0]["Subject"][:32]},
        {"icon": "functions", "label": "Average", "value": subject["Records"].mean(),
         "description": "Mean records per subject"},
    ]
    render_kpi_row(kpis)

    st.write("")
    col1, col2 = st.columns(2)
    with col1:
        section_card_start("Top 20 Subjects")
        charts.render(charts.horizontal_bar(subject, x="Records", y="Subject", top_n=20))
        section_card_end()
    with col2:
        section_card_start("Treemap — Share of Records")
        charts.render(charts.treemap_chart(subject.head(40), path="Subject", values="Records"))
        section_card_end()

    st.write("")
    section_card_start("Lollipop Chart — Top 20 Subjects")
    charts.render(charts.lollipop_chart(subject, x="Records", y="Subject", top_n=20))
    section_card_end()

    st.write("")
    section_card_start("Subject Records — Searchable Table")
    render_table(subject, key="subjects_table")
    section_card_end()
