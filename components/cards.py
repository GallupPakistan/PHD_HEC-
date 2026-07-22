"""
cards.py
Layout building blocks: section card wrapper, insights panel, and page
header (title, subtitle, breadcrumb, last-updated).
"""

from typing import Dict
import streamlit as st


def section_card_start(title: str) -> None:
    """Opens a bordered card container with a section title. Must be paired
    with section_card_end() after the content is rendered."""
    st.markdown(f'<div class="bi-card"><div class="section-title">{title}</div>', unsafe_allow_html=True)


def section_card_end() -> None:
    st.markdown("</div>", unsafe_allow_html=True)


def render_insights_panel(title: str, insights: Dict[str, str]) -> None:
    """Renders a card with label/value insight rows."""
    section_card_start(title)
    rows = "".join(
        f'<div class="insight-item"><span class="insight-label">{k}</span>'
        f'<span class="insight-value">{v}</span></div>'
        for k, v in insights.items()
    )
    st.markdown(rows, unsafe_allow_html=True)
    section_card_end()


def render_page_header(title: str, subtitle: str, breadcrumb: str, last_updated: str) -> None:
    st.markdown(
        f"""
        <div class="breadcrumb">{breadcrumb}</div>
        <div class="page-title">{title}</div>
        <div class="page-subtitle">{subtitle}</div>
        <div class="last-updated">Last updated: {last_updated}</div>
        <hr class="bi-divider">
        """,
        unsafe_allow_html=True,
    )
