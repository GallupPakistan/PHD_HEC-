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
from app_pages import overview, universities, phd_directory, analytics, explorer, about
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
    "Analytics": analytics.render,
    "Data Explorer": explorer.render,
    "About": about.render,
}
PAGE_SUBTITLES = {
    "Overview": "A complete summary across the university directory and all PhD dimensions — universities, disciplines, subjects, and years.",
    "Universities": "Directory of Higher Education Institutions by province, city, and sector.",
    "PhD Directory": "All PhD records combined — by university, discipline, subject, and year.",
    "Analytics": "Deeper analytical breakdowns across the dataset.",
    "Data Explorer": "Browse and filter the raw underlying data.",
    "About": "About this dashboard and data sources.",
}


render_topbar(
    active_page,
    PAGE_SUBTITLES.get(active_page, ""),
    get_last_updated(),
    stat_label="Total Universities",
    stat_value=f"{int(data['province_sector']['Total'].sum()):,}",
)

PAGE_MAP[active_page](data)
