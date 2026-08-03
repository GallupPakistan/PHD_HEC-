"""
topbar.py
Renders the full page header as a navy card: a small logo badge (top
left), breadcrumb with home icon, big page title, subtitle, a
calendar-icon "Last updated" line, decorative dotted pattern, and a
quick stat badge (value + label + icon) on the right.
"""

import streamlit as st

def render_topbar(
    active_page: str,
    subtitle: str,
    last_updated: str,
    stat_label: str = "",
    stat_value: str = "",
    stat_icon: str = "account_balance",
) -> None:
    stat_html = ""
    if stat_label and stat_value:
        stat_html = (
            f'<div class="hec-topbar-stat">'
            f'<div class="hec-topbar-stat-icon-circle"><span class="material-symbols-outlined">{stat_icon}</span></div>'
            f'<div class="hec-topbar-stat-vsep"></div>'
            f'<div class="hec-topbar-stat-text">'
            f'<div class="hec-topbar-stat-value">{stat_value}</div>'
            f'<div class="hec-topbar-stat-label">{stat_label}</div>'
            f'</div>'
            f'</div>'
        )

    # Note: Keep this string flushed to the left margin to prevent markdown code-block formatting!
    topbar_html = f"""<div class="hec-topbar">
<div class="hec-topbar-dots"></div>
<div class="hec-topbar-watermark"><span class="material-symbols-outlined">account_balance</span></div>

<div class="hec-topbar-toprow">
<div class="hec-topbar-brand">
<div class="hec-topbar-logo-circle">
<span class="material-symbols-outlined">account_balance</span>
</div>
<div class="hec-topbar-brand-text">
<div class="hec-topbar-brand-name">HEC Analytics</div>
<div class="hec-topbar-brand-sub">Dashboard</div>
</div>
</div>
<div class="hec-topbar-vsep"></div>
<div class="hec-topbar-crumbs">
<div class="hec-topbar-crumb-icon-badge">
<span class="material-symbols-outlined">home</span>
</div>
<span class="hec-topbar-sep">/</span>
<span class="hec-topbar-crumb">Dashboard</span>
<span class="hec-topbar-sep">/</span>
<span class="hec-topbar-crumb hec-topbar-current">{active_page}</span>
</div>
</div>

<div class="hec-topbar-bottomrow">
<div class="hec-topbar-left">
<div class="hec-topbar-title-wrapper">
<div class="hec-topbar-accent-bar"></div>
<div class="hec-topbar-title">{active_page}</div>
</div>
<div class="hec-topbar-subtitle">{subtitle}</div>
<div class="hec-topbar-lastupdated-pill">
<span class="material-symbols-outlined">calendar_month</span>
<span>Last updated: <b>{last_updated}</b></span>
</div>
</div>
<div class="hec-topbar-right">{stat_html}</div>
</div>
</div>"""

    st.markdown(topbar_html, unsafe_allow_html=True)