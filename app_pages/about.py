"""
pages/about.py
Dashboard information: dataset info, refresh date, total records,
technology stack, and version.
"""

import streamlit as st

from components.cards import section_card_start, section_card_end, render_page_header
from utils.loader import get_last_updated


def render(data: dict) -> None:
    university = data["university"]
    total_records = int(university["Records"].sum())

   

    col1, col2 = st.columns(2)
    with col1:
        section_card_start("Dataset Information")
        st.markdown(
            f"""
            <div class="insight-item"><span class="insight-label">Source File</span><span class="insight-value">Dashboard_Data.xlsx</span></div>
            <div class="insight-item"><span class="insight-label">Sheets</span><span class="insight-value">University, Discipline, Subject, Year</span></div>
            <div class="insight-item"><span class="insight-label">Total Records</span><span class="insight-value">{total_records:,}</span></div>
            <div class="insight-item"><span class="insight-label">Refresh Date</span><span class="insight-value">{get_last_updated()}</span></div>
            """,
            unsafe_allow_html=True,
        )
        section_card_end()
    with col2:
        section_card_start("Technology Stack")
        st.markdown(
            """
            <div class="insight-item"><span class="insight-label">Framework</span><span class="insight-value">Streamlit</span></div>
            <div class="insight-item"><span class="insight-label">Charting</span><span class="insight-value">Plotly</span></div>
            <div class="insight-item"><span class="insight-label">Tables</span><span class="insight-value">streamlit-aggrid (AgGrid)</span></div>
            <div class="insight-item"><span class="insight-label">Data Processing</span><span class="insight-value">pandas, openpyxl</span></div>
            <div class="insight-item"><span class="insight-label">Version</span><span class="insight-value">1.0.0</span></div>
            """,
            unsafe_allow_html=True,
        )
        section_card_end()
