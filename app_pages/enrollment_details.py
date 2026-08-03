"""
app_pages/enrollment_details.py
Enrollment Details — deep-dive breakdowns by level, discipline, province,
region/gender, and sector. Each section is a full-width chart; the single
detailed data table sits at the bottom for row-level verification.
"""

import streamlit as st

from components.cards import section_card_start, section_card_end
from components.tables import render_table
from components.filters import render_filters
from components import charts
from utils.loader import load_master_data, filter_master_df, load_region_gender_enrollment


def render(data: dict) -> None:
    master_data = load_master_data()

    filters = render_filters(master_data, key_prefix="details")

    # --- Region and Gender-wise Enrollment (dedicated section, own filters) ----
    section_card_start("Region and Gender-wise Enrollment")
    region_df = load_region_gender_enrollment()

    if not region_df.empty:
        filt_col1, filt_col2, spacer = st.columns([1, 1, 2])
        with filt_col1:
            rg_year = st.selectbox(
                "Year", options=["All Years"] + sorted(region_df["Year"].unique()),
                index=0,
                key="region_gender_year",
            )
        with filt_col2:
            rg_sector = st.selectbox(
                "Sector", options=["Combined (Public + Private)"] + sorted(region_df["Sector"].unique()),
                key="region_gender_sector",
            )

        rg_filtered = region_df if rg_year == "All Years" else region_df[region_df["Year"] == rg_year]
        if rg_sector != "Combined (Public + Private)":
            rg_filtered = rg_filtered[rg_filtered["Sector"] == rg_sector]

        rg_agg = rg_filtered.groupby("Province", as_index=False)[["Male", "Female", "Total"]].sum()

        st.write("")
        charts.render(charts.diverging_bar_chart(
            rg_agg, category="Province", left_col="Male", right_col="Female",
            left_name="Male", right_name="Female",
        ))
    else:
        st.info("Region & Gender-wise enrollment data not available.")
    section_card_end()
    # --- Level-wise (Treemap) + Province-wise (Lollipop), side by side --------
    col_level, col_province = st.columns(2)
 
    with col_level:
        section_card_start("Level-wise Enrollment")
        level_df = filter_master_df(master_data["enrolment_by_level_gender"], filters)
        if not level_df.empty:
               level_agg = level_df.groupby("level", as_index=False)["count"].sum()
               charts.render(charts.horizontal_bar(level_agg, x="count", y="level", top_n=10))
        else:
               st.info("No level-wise data available for the selected filters.")
        section_card_end()
        
    st.write("")
 
    with col_province:
        section_card_start("Province-wise Enrollment")
        pg_df = filter_master_df(master_data["enrolment_by_province_gender"], filters)
        if not pg_df.empty:
            prov_agg = pg_df.groupby("province", as_index=False)["count"].sum()
            charts.render(charts.lollipop_chart(prov_agg, x="count", y="province", top_n=10))
        else:
            st.info("No province-wise data available for the selected filters.")
        section_card_end()

    st.write("")

    # --- Discipline-wise ---------------------------------------------------------
    section_card_start("Discipline-wise Enrollment")
    disc_df = filter_master_df(master_data["enrolment_by_discipline"], filters)
    if not disc_df.empty:
        disc_agg = disc_df.groupby("discipline", as_index=False)["total"].sum()
        charts.render(charts.horizontal_bar(disc_agg, x="total", y="discipline", top_n=15))
    else:
        st.info("No discipline-wise data available for the selected filters.")
    section_card_end()

    st.write("")


    # --- Filtered Detailed Data Table ------------------------------------------------
    section_card_start("Filtered Detailed Data")
    if not pg_df.empty:
        render_table(pg_df, key="details_full_table")
    else:
        st.info("No detailed row-level data available for the selected filters.")
    section_card_end()