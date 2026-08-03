"""
app_pages/enrollment_ratios.py
Enrollment Ratios — Male vs Female, Province-wise, and Public vs Private
ratio breakdowns for the selected filters.
"""

import pandas as pd
import streamlit as st

from components.cards import section_card_start, section_card_end
from components.tables import render_table
from components.filters import render_filters
from components import charts
from utils.loader import load_master_data, filter_master_df


def render(data: dict) -> None:
    master_data = load_master_data()

    filters = render_filters(master_data, key_prefix="ratios")

    col1, col2 = st.columns(2)

    # --- Male vs Female Ratio -------------------------------------------------
    with col1:
        section_card_start("Male vs Female Ratio")
        summary_df = filter_master_df(master_data["enrolment_summary"], filters)
        if not summary_df.empty:
            gender_totals = pd.DataFrame({
                "gender": ["Male", "Female"],
                "count": [summary_df["male"].sum(), summary_df["female"].sum()],
            })
            charts.render(charts.donut_chart(gender_totals, names="gender", values="count"))
        else:
            st.info("No data available for the selected filters.")
        section_card_end()

    # --- Public vs Private Ratio -----------------------------------------------
    with col2:
        section_card_start("Public vs Private Ratio")
        sector_df = filter_master_df(master_data["enrolment_by_sector"], filters)
        if not sector_df.empty:
            sector_totals = sector_df.groupby("sector", as_index=False)["total"].sum()
            charts.render(charts.donut_chart(sector_totals, names="sector", values="total"))
        else:
            st.info("No sector-wise data available for the selected filters.")
        section_card_end()

    st.write("")
    section_card_start("Province-wise Gender Ratio")
    pg_df = filter_master_df(master_data["enrolment_by_province_gender"], filters)
    if not pg_df.empty:
        charts.render(charts.stacked_bar_100(pg_df, category="province", value="count", group="gender"))
    else:
        st.info("Province-level data not available for the selected filters.")
    section_card_end()

    st.write("")
    section_card_start("Public vs Private Ratio by Year")
    sector_df_full = filter_master_df(master_data["enrolment_by_sector"], filters)
    if not sector_df_full.empty:
        melted = sector_df_full.melt(
            id_vars=["year", "sector"], value_vars=["total"],
            var_name="metric", value_name="value",
        )
        charts.render(charts.stacked_bar_100(melted, category="year", value="value", group="sector"))
    else:
        st.info("No year-wise sector data available for the selected filters.")
    section_card_end()

    st.write("")
    col3, col4 = st.columns(2)
    with col3:
        section_card_start("Gender Comparison Table")
        if not summary_df.empty:
            render_table(summary_df[["year", "male", "female", "total"]], key="ratios_gender_table")
        section_card_end()
    with col4:
        section_card_start("Sector Comparison Table")
        if not sector_df.empty:
            render_table(sector_df, key="ratios_sector_table")
        section_card_end()