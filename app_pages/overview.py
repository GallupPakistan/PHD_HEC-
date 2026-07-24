"""
app_pages/overview.py
Comprehensive overview: brings together HEIS (university directory) and
ALL PhD dimensions (University, Discipline, Subject, Year) into one page,
with every section clearly labeled so it's obvious what each chart shows.
"""

import streamlit as st

from components.cards import section_card_start, section_card_end, render_page_header, render_insights_panel
from components.kpis import render_kpi_row
from components import charts
from utils.helpers import compute_overview_insights
from utils.loader import get_last_updated


def render(data: dict) -> None:
    heis = data["heis"]
    university = data["university"]
    discipline = data["discipline"]
    subject = data["subject"]
    year = data["year"]
    growth = data["heis_growth"]


    # -----------------------------------------------------------------
    # Top-level KPIs (combined across both datasets)
    # -----------------------------------------------------------------
    ps = data["province_sector"]
    total_universities = int(ps["Total"].sum())
    public_count = int(ps["Public"].sum())
    private_count = int(ps["Private"].sum())
    total_phd_records = int(university["Records"].sum())

    kpis = [
        {"icon": "school", "label": "Total Universities", "value": total_universities,
         "description": ""},
        {"icon": "account_balance", "label": "Public", "value": public_count, "description": ""},
        {"icon": "business_center", "label": "Private", "value": private_count, "description": ""},
        {"icon": "workspace_premium", "label": "Total PhD Records", "value": total_phd_records,
         "description": ""},
    ]
    render_kpi_row(kpis)

    # -----------------------------------------------------------------
    # SECTION 1 — University Directory (HEIS)
    # -----------------------------------------------------------------
    st.write("")
    st.markdown("### 🏛️ University Directory Overview")
    col1, col2 = st.columns(2)
    with col1:
        section_card_start("Sector-wise Number of HEIs (Public vs Private)")
        sector_counts = heis["Sector"].value_counts().reset_index()
        sector_counts.columns = ["Sector", "Count"]
        charts.render(charts.donut_chart(sector_counts, names="Sector", values="Count", top_n=5))
        section_card_end()
    with col2:
        section_card_start("Universities by Province")
        province_counts = heis["Province"].value_counts().reset_index()
        province_counts.columns = ["Province", "Count"]
        charts.render(charts.horizontal_bar(province_counts, x="Count", y="Province", top_n=10))
        section_card_end()



    # -----------------------------------------------------------------
    # SECTION 2 — PhD Records by University
    # -----------------------------------------------------------------
    st.write("")
    st.markdown("### 🎓 PhD Records — by University")
    section_card_start("Top Universities by PhD Count")
    charts.render(charts.horizontal_bar(university, x="Records", y="University", top_n=10))
    section_card_end()

    # -----------------------------------------------------------------
    # SECTION 3 — PhD Records by Discipline
    # -----------------------------------------------------------------
    st.write("")
    st.markdown("### 📚 PhD Records — by Discipline")
    col3, col4 = st.columns(2)
    with col3:
        section_card_start("Discipline Distribution")
        charts.render(charts.donut_chart(discipline, names="Discipline", values="Records", top_n=8))
        section_card_end()
    with col4:
        section_card_start("Top Disciplines by PhD Count")
        charts.render(charts.horizontal_bar(discipline, x="Records", y="Discipline", top_n=10))
        section_card_end()

    # -----------------------------------------------------------------
    # SECTION 4 — PhD Records by Subject
    # -----------------------------------------------------------------
    st.write("")
    st.markdown("### 📖 PhD Records — by Subject")
    col5, col6 = st.columns(2)
    with col5:
        section_card_start("Top Subjects by PhD Count")
        charts.render(charts.horizontal_bar(subject, x="Records", y="Subject", top_n=10))
        section_card_end()
    with col6:
        section_card_start("Subject Breakdown (Treemap)")
        charts.render(charts.treemap_chart(subject, path="Subject", values="Records", top_n=15))
        section_card_end()

    # -----------------------------------------------------------------
    # SECTION 5 — PhD Records by Year
    # -----------------------------------------------------------------
    st.write("")
    st.markdown("### 📅 PhD Records — by Year")
    section_card_start("PhD Trend by Year")
    charts.render(charts.line_chart(year, x="Year", y="Records"))
    section_card_end()

    # -----------------------------------------------------------------
    # Quick Insights
    # -----------------------------------------------------------------
    st.write("")
    render_insights_panel("Quick Insights", compute_overview_insights(data))