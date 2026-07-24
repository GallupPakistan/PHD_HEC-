"""
topbar.py
Renders the full page header as a navy card: breadcrumb, title, subtitle,
last-updated, and a quick stat badge on the right. Also shows the
dashboard name "HEI's Analytics Dashboard" prominently in the middle center.
"""

import streamlit as st


def render_topbar(
    active_page: str,
    subtitle: str,
    last_updated: str,
    stat_label: str = "",
    stat_value: str = "",
) -> None:
    stat_html = ""
    if stat_label and stat_value:
        stat_html = (
            f'<div class="hec-topbar-stat">'
            f'<div class="hec-topbar-stat-value">{stat_value}</div>'
            f'<div class="hec-topbar-stat-label">{stat_label}</div>'
            f"</div>"
        )

    topbar_html = f"""<div class="hec-topbar" style="position: relative; padding-top: 10px;">
<div style="text-align: center; margin-top: 30px; margin-bottom: 20px;">
<h1 style="color: #FFFFFF; font-size: 2rem; font-weight: 700; margin: 0; padding: 0; letter-spacing: 0.5px; display: inline-block;">HEI's Analytics Dashboard</h1>
</div>
<div style="display: flex; justify-content: space-between; align-items: flex-end;">
<div class="hec-topbar-left">
<div class="hec-topbar-crumbs">
<span class="hec-topbar-crumb">Home</span>
<span class="hec-topbar-sep material-symbols-outlined">chevron_right</span>
<span class="hec-topbar-crumb hec-topbar-current">{active_page}</span>
</div>
<div class="hec-topbar-title">{active_page}</div>
<div class="hec-topbar-subtitle">{subtitle}</div>
<div class="hec-topbar-lastupdated-inline">Last updated: {last_updated}</div>
</div>
<div class="hec-topbar-right">{stat_html}</div>
</div>
</div>"""

    st.markdown(topbar_html, unsafe_allow_html=True)