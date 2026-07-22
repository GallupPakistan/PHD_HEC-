"""
pages/explorer.py
Raw data explorer — lets the user pick a dataset and inspect it through the
full-featured AgGrid table (search, resize, hide columns, pagination,
sorting, filtering, CSV/Excel export).
"""

import io
import streamlit as st
import pandas as pd

from components.cards import section_card_start, section_card_end, render_page_header
from components.tables import render_table
from utils.loader import get_last_updated


def render(data: dict) -> None:
    render_page_header(
        title="Data Explorer",
        subtitle="Explore the underlying datasets directly with full search, filter, and export capability.",
        breadcrumb="Home / Data Explorer",
        last_updated=get_last_updated(),
    )

    dataset_name = st.selectbox(
        "Select dataset",
        options=["University", "Discipline", "Subject", "Year"],
        key="explorer_dataset",
    )
    df = data[dataset_name.lower()]

    section_card_start(f"{dataset_name} Dataset")
    render_table(df, key=f"explorer_{dataset_name.lower()}")

    buffer = io.BytesIO()
    with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name=dataset_name[:31])
    st.download_button(
        "Export Excel",
        data=buffer.getvalue(),
        file_name=f"{dataset_name.lower()}_export.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        key=f"explorer_{dataset_name.lower()}_xlsx",
    )
    section_card_end()
