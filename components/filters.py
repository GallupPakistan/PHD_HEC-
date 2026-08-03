"""
components/filters.py

Renders an inline filter bar (Year / Province / Gender / Sector) meant to
sit at the TOP of a page's content area, directly above its charts —
NOT in the left navigation sidebar. Used by the three enrolment pages
(Enrollment Summary, Enrollment Ratios, Enrollment Details) so that
changing a filter re-filters every chart on that page.

Usage inside a page, e.g. app_pages/overview.py or your enrollment pages:

    from components.filters import render_filters
    from utils.loader import load_master_data, filter_master_df

    master_data = load_master_data()
    filters = render_filters(master_data, key_prefix="summary")

    df = filter_master_df(master_data["enrolment_summary"], filters)
    # ... pass df into your charts/tables/kpis as usual
"""

import streamlit as st
from utils.loader import get_master_years, get_master_provinces

GENDERS = ["Male", "Female"]
SECTORS = ["Public", "Private"]


def render_filters(master_data: dict, key_prefix: str) -> dict:
    """
    Renders a horizontal filter bar above the page's charts.

    Args:
        master_data: dict of DataFrames from utils.loader.load_master_data()
        key_prefix: unique prefix per page (e.g. "summary", "ratios",
                    "details") so each page's filter widgets keep their
                    own independent state instead of colliding.

    Returns:
        dict: {"years": [...], "provinces": [...], "genders": [...], "sectors": [...]}
        Pass this straight into utils.loader.filter_master_df(df, filters).
    """
    all_years = get_master_years(master_data)
    all_provinces = get_master_provinces(master_data)

    st.caption("Leave a filter empty to include all values for that filter.")
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        years = st.multiselect(
            "Year", options=all_years,
            default=st.session_state.get(f"{key_prefix}_years", []),
            key=f"{key_prefix}_years",
        )
    with col2:
        provinces = st.multiselect(
            "Province", options=all_provinces,
            default=st.session_state.get(f"{key_prefix}_provinces", []),
            key=f"{key_prefix}_provinces",
        )
    with col3:
        genders = st.multiselect(
            "Gender", options=GENDERS,
            default=st.session_state.get(f"{key_prefix}_genders", []),
            key=f"{key_prefix}_genders",
        )
    with col4:
        sectors = st.multiselect(
            "Sector", options=SECTORS,
            default=st.session_state.get(f"{key_prefix}_sectors", []),
            key=f"{key_prefix}_sectors",
        )

    return {
        "years": years,
        "provinces": provinces,
        "genders": genders,
        "sectors": sectors,
    }