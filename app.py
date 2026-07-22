"""
app.py
Entry point for the HEC Analytics Dashboard. Wires together the sidebar
navigation, global styling, and the eight pages of the application.
"""

import streamlit as st

from utils.styles import inject_global_css
from utils.loader import load_workbook
from components.sidebar import render_sidebar
from app_pages import overview, universities, disciplines, subjects, years, analytics, explorer, about

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
    "Disciplines": disciplines.render,
    "Subjects": subjects.render,
    "Years": years.render,
    "Analytics": analytics.render,
    "Data Explorer": explorer.render,
    "About": about.render,
}

PAGE_MAP[active_page](data)
