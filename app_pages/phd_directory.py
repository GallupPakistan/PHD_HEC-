"""
app_pages/phd_directory.py
Combined PhD Directory page — brings all PhD dimensions together:
the existing university/discipline/subject/year records, plus the
HEC annual-report "PhDs Produced" figures (cumulative, by discipline
and gender).
"""

import pandas as pd
import streamlit as st

from components.cards import section_card_start, section_card_end, render_page_header, render_insights_panel
from components.kpis import render_kpi_row
from components import charts
from components.tables import render_table
from utils.helpers import compute_overview_insights
from utils.loader import get_last_updated, load_master_data


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

    # -------------------------------------------------------------------------
    # PhDs Produced — HEC Annual Report figures (cumulative since 1947,
    # by discipline and gender). Sourced separately from the PhD directory
    # records above, so it is presented as its own section with a clear
    # label distinguishing it as a national cumulative figure.
    # -------------------------------------------------------------------------
    master_data = load_master_data()
    phds_produced = master_data.get("phds_produced")

    if phds_produced is not None and not phds_produced.empty:
        st.write("")
        st.markdown('<hr class="bi-divider">', unsafe_allow_html=True)

        as_of_options = sorted(phds_produced["as_of"].dropna().unique().tolist())
        latest_as_of = as_of_options[-1] if as_of_options else None

        st.markdown(
            f'<div class="section-title">PhDs Produced Nationally (HEC Annual Report — {latest_as_of})</div>',
            unsafe_allow_html=True,
        )
        st.caption(
            "Cumulative figures since 1947, as reported by HEC. These are national "
            "totals by discipline and gender — distinct from the individual PhD "
            "directory records shown above."
        )

        phd_view = phds_produced[phds_produced["as_of"] == latest_as_of].copy() if latest_as_of else phds_produced
        phd_view["total"] = phd_view["male"].fillna(0) + phd_view["female"].fillna(0)

        national_total = int(phd_view["total"].sum())
        national_male = int(phd_view["male"].fillna(0).sum())
        national_female = int(phd_view["female"].fillna(0).sum())
        female_share = (national_female / national_total * 100) if national_total else 0

        national_kpis = [
            {"icon": "public", "label": "PhDs Produced Nationally", "value": national_total,
             "description": f"Cumulative, {latest_as_of}"},
            {"icon": "man", "label": "Male", "value": national_male, "description": "Cumulative"},
            {"icon": "woman", "label": "Female", "value": national_female, "description": "Cumulative"},
            {"icon": "percent", "label": "Female Share", "value": f"{female_share:.1f}%",
             "description": "Of national total"},
        ]
        render_kpi_row(national_kpis)

        st.write("")
        col5, col6 = st.columns(2)
        with col5:
            section_card_start("PhDs Produced by Discipline (National)")
            disc_totals = phd_view.groupby("discipline", as_index=False)["total"].sum()
            charts.render(charts.horizontal_bar(disc_totals, x="total", y="discipline", top_n=12))
            section_card_end()
        with col6:
            section_card_start("Gender Split (National)")
            gender_totals = pd.DataFrame({
                "gender": ["Male", "Female"],
                "count": [national_male, national_female],
            })
            charts.render(charts.donut_chart(gender_totals, names="gender", values="count"))
            section_card_end()

        st.write("")
        section_card_start("PhDs Produced — Detailed National Table")
        render_table(phd_view[["discipline", "male", "female", "total"]], key="phd_national_table")
        section_card_end()