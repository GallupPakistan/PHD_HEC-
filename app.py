"""
app.py
Entry point for the HEC Analytics Dashboard. Wires together the sidebar
navigation, global styling, and the eight pages of the application.
"""

import streamlit as st

from utils.styles import inject_global_css
from utils.loader import load_workbook
from components.topbar import render_topbar
from components.sidebar import render_sidebar, get_last_updated
from app_pages import (
    overview,
    universities,
    phd_directory,
    enrollment_summary,
    enrollment_ratios,
    enrollment_details,
    about,
)
st.set_page_config(
    page_title="HEC Analytics Dashboard",
    page_icon=":material/account_balance:",
    layout="wide",
    initial_sidebar_state="expanded",
)

inject_global_css()

data = load_workbook()

active_page = render_sidebar()


PAGE_MAP = {
    "Overview": overview.render,
    "Universities": universities.render,
    "PhD Directory": phd_directory.render,

    "Enrollment Summary": enrollment_summary.render,
    "Enrollment Ratios": enrollment_ratios.render,
    "Enrollment Details": enrollment_details.render,
    "About": about.render,
}
PAGE_SUBTITLES = {
    "Overview":
        "A complete summary across the university directory and all PhD dimensions — universities, disciplines, subjects, and years.",

    "Universities":
        "Directory of Higher Education Institutions by province, city, and sector.",

    "PhD Directory":
        "All PhD records combined — by university, discipline, subject, and year.",

    "Enrollment Summary":
        "High-level overview of higher education enrolment across Pakistan.",

    "Enrollment Ratios":
        "Gender, province and sector based enrolment ratios and comparisons.",

    "Enrollment Details":
        "Detailed enrolment statistics by level, discipline, province and sector.",

    "About":
        "About this dashboard and data sources.",
}


render_topbar(
    active_page,
    PAGE_SUBTITLES.get(active_page, ""),
    get_last_updated(),
    stat_label="Total Universities",
    stat_value=f"{int(data['province_sector']['Total'].sum()):,}",
)

PAGE_MAP[active_page](data)
