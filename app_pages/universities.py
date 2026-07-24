"""
app_pages/universities.py
Universities directory page — built from HEIS Data.xlsx (institution-level
data: Province, City, Sector). Includes a live search box: KPIs, the
directory table, and the sector/province/city charts all update instantly
based on what's typed — no button or Enter needed (Streamlit reruns on
every keystroke). The establishment-year growth chart at the bottom stays
independent of the search, since it's a year-wise trend rather than a
per-university record.
"""

import streamlit as st
import pandas as pd

from components.cards import section_card_start, section_card_end
from components.kpis import render_kpi_row
from components import charts


def render(data: dict) -> None:
    heis = data["heis"]
    ps = data["province_sector"]

    # -----------------------------------------------------------------
    # Live search — filters heis by university name, province, or city.
    # Every keystroke triggers a Streamlit rerun automatically.
    # -----------------------------------------------------------------
    search_term = st.text_input(
        "Search",
        key="uni_search",
        placeholder="🔍 Search by university name, province, or city...",
        label_visibility="collapsed",
    )

    if search_term:
        mask = (
            heis["Name of University"].str.contains(search_term, case=False, na=False)
            | heis["Province"].str.contains(search_term, case=False, na=False)
            | heis["City"].str.contains(search_term, case=False, na=False)
        )
        filtered_heis = heis[mask]
    else:
        filtered_heis = heis

    # -----------------------------------------------------------------
    # KPIs — authoritative 278-total (from Sheet4) when no search is
    # active; switch to live counts from the filtered directory once
    # the user starts typing, since Sheet4 has no name-level detail to
    # filter against.
    # -----------------------------------------------------------------
    if search_term:
        total = len(filtered_heis)
        public_count = int((filtered_heis["Sector"].str.lower() == "public").sum())
        private_count = int((filtered_heis["Sector"].str.lower() == "private").sum())
        provinces_covered = filtered_heis["Province"].nunique()
        total_desc = f"Matching '{search_term}'"
    else:
        total = int(ps["Total"].sum())
        public_count = int(ps["Public"].sum())
        private_count = int(ps["Private"].sum())
        provinces_covered = len(ps)
        total_desc = "All institutions on record"

    kpis = [
        {"icon": "school", "label": "Total Universities", "value": total, "description": total_desc},
        {"icon": "account_balance", "label": "Public Sector", "value": public_count,
         "description": f"{(public_count/total*100):.1f}% of total" if total else ""},
        {"icon": "business_center", "label": "Private Sector", "value": private_count,
         "description": f"{(private_count/total*100):.1f}% of total" if total else ""},
        {"icon": "map", "label": "Provinces Covered", "value": provinces_covered,
         "description": "Distinct provinces/regions"},
    ]
    render_kpi_row(kpis)
    st.write("")

    if search_term and filtered_heis.empty:
        st.info(f"No universities found matching '{search_term}'.")
        return

    # -----------------------------------------------------------------
    # Province & Sector-wise table + Sector donut
    # No search: show the authoritative Sheet4 table (278 total).
    # Search active: show a live breakdown computed from filtered_heis
    # instead, since Sheet4 can't be filtered by name/city.
    # -----------------------------------------------------------------
    col1, col2 = st.columns(2)
    with col1:
        if search_term:
            section_card_start(f"Province & Sector-wise HEIs — matching '{search_term}'")
            live_table = (
                filtered_heis.groupby(["Province", "Sector"]).size()
                .unstack(fill_value=0).reset_index()
            )
            live_table["Total"] = live_table.select_dtypes("number").sum(axis=1)
            live_table = live_table.sort_values("Total", ascending=False)
            st.dataframe(live_table, use_container_width=True, hide_index=True)
        else:
            section_card_start("Province & Sector-wise HEIs")
            st.dataframe(ps, use_container_width=True, hide_index=True)
        section_card_end()
    with col2:
        section_card_start("Sector-wise Number of HEIs")
        if search_term:
            sector_counts = filtered_heis["Sector"].value_counts().reset_index()
            sector_counts.columns = ["Sector", "Count"]
        else:
            sector_counts = pd.DataFrame({
                "Sector": ["Public", "Private"],
                "Count": [public_count, private_count],
            })
        charts.render(charts.donut_chart(sector_counts, names="Sector", values="Count", top_n=5))
        section_card_end()

    # -----------------------------------------------------------------
    # Province & City charts — always driven by filtered_heis, so they
    # update live with the search (identical to heis when no search).
    # -----------------------------------------------------------------
    st.write("")
    col3, col4 = st.columns(2)
    with col3:
        section_card_start("Universities by Province")
        province_counts = filtered_heis["Province"].value_counts().reset_index()
        province_counts.columns = ["Province", "Count"]
        charts.render(charts.horizontal_bar(province_counts, x="Count", y="Province", top_n=10))
        section_card_end()
    with col4:
        section_card_start("Universities by City (Top 10)")
        city_counts = filtered_heis["City"].value_counts().reset_index()
        city_counts.columns = ["City", "Count"]
        charts.render(charts.horizontal_bar(city_counts, x="Count", y="City", top_n=10))
        section_card_end()

    # -----------------------------------------------------------------
    # Directory table of matching results (only shown while searching,
    # so the user can see exactly which universities matched)
    # -----------------------------------------------------------------
    if search_term:
        st.write("")
        section_card_start(f"Matching Universities ({len(filtered_heis)})")
        st.dataframe(
            filtered_heis[["Name of University", "Province", "City", "Sector"]],
            use_container_width=True, hide_index=True,
        )
        section_card_end()

    # -----------------------------------------------------------------
    # Growth chart — independent of the search (year-wise trend, not a
    # per-university record), always shows the full historical series.
    # -----------------------------------------------------------------
    st.write("")
    section_card_start("Increase in HEIs over the Years by Establishment Date")
    growth = data["heis_growth"]
    charts.render(
        charts.dual_line_chart(
            growth, x="Year", y1="Total", y2="New",
            name1="Total HEIs Established Over the Years",
            name2="Total HEIs Established Within a Year",
            milestone_year=2002,
            milestone_label="HEC Established in: 2002",
        )
    )
    section_card_end()