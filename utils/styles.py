"""
styles.py
Central style configuration for the HEC Analytics Dashboard.
Holds the color palette and the global CSS injected into every page.

NOTE: This version deliberately avoids touching header/toolbar
visibility or forcing display/visibility on the sidebar container —
newer Streamlit versions (1.60+) tie the sidebar's expand/collapse
behavior to that header's internal JS, and overriding it was hiding
the sidebar entirely. Only cosmetic styling is applied here.
"""

import streamlit as st

# --------------------------------------------------------------------------
# Color palette (single source of truth — never hardcode colors elsewhere)
# --------------------------------------------------------------------------
COLORS = {
    "primary": "#0B3A75",
    "secondary": "#4F6D8A",
    "accent": "#58C4B5",
    "background": "#F5F7FA",
    "card": "#FFFFFF",
    "border": "#E4E8ED",
    "text": "#243447",
    "muted": "#6B7280",
    "hover": "#E8F2FF",
    "selected": "#D6E8FF",
    "success": "#2E8B57",
}

# A qualitative sequence built from the palette, used across all charts so
# every chart on every page shares the same visual language.
CHART_SEQUENCE = [
    COLORS["primary"],
    COLORS["accent"],
    COLORS["secondary"],
    "#7FA6C9",
    "#8FD9CD",
    "#A9BBCB",
    "#2E5C8A",
    "#3FA898",
]

FONT_FAMILY = (
    "'Segoe UI', 'Inter', -apple-system, BlinkMacSystemFont, "
    "'Helvetica Neue', Arial, sans-serif"
)


def inject_global_css() -> None:
    """Injects the global CSS used to re-skin Streamlit into an enterprise
    BI look and feel. Call once, at the very top of app.py.

    Intentionally does NOT hide header/toolbar/decoration and does NOT
    force display/visibility on the sidebar — those overrides broke the
    sidebar's collapse/expand behavior on Streamlit 1.60."""

    st.markdown(
        f"""
        <style>
        @import url('https://fonts.googleapis.com/icon?family=Material+Symbols+Outlined');

        html, body, [class*="css"] {{
            font-family: {FONT_FAMILY};
            color: {COLORS['text']};
        }}

        .stApp {{
            background-color: {COLORS['background']};
        }}

        /* Safe to hide: these never affect sidebar layout */
        #MainMenu {{visibility: hidden;}}
        footer {{visibility: hidden;}}

        /* Sidebar cosmetic styling only — no display/visibility overrides */
        section[data-testid="stSidebar"] {{
            background-color: {COLORS['primary']};
            border-right: 1px solid {COLORS['border']};
        }}
        section[data-testid="stSidebar"] * {{
            color: #FFFFFF !important;
        }}
        section[data-testid="stSidebar"] .stButton button {{
            width: 100%;
            text-align: left;
            background-color: transparent;
            border: none;
            color: #E8EEF5 !important;
            padding: 0.55rem 0.9rem;
            border-radius: 6px;
            font-weight: 500;
            font-size: 0.92rem;
            margin-bottom: 2px;
            transition: background-color 0.15s ease;
        }}
        section[data-testid="stSidebar"] .stButton button:hover {{
            background-color: rgba(255,255,255,0.10);
            color: #FFFFFF !important;
        }}
        section[data-testid="stSidebar"] .stButton button:focus {{
            box-shadow: none !important;
        }}
        .nav-active button {{
            background-color: rgba(255,255,255,0.16) !important;
            border-left: 3px solid {COLORS['accent']} !important;
        }}

        /* Remove default block padding for tighter control */
        .block-container {{
            padding-top: 1.4rem;
            padding-bottom: 2rem;
            padding-left: 2.2rem;
            padding-right: 2.2rem;
            max-width: 1500px;
        }}

        /* Card component */
        .bi-card {{
            background-color: {COLORS['card']};
            border: 1px solid {COLORS['border']};
            border-radius: 10px;
            padding: 1.1rem 1.3rem;
            box-shadow: 0 1px 3px rgba(16, 30, 54, 0.06);
            height: 100%;
        }}
        .bi-card:hover {{
            box-shadow: 0 3px 10px rgba(16, 30, 54, 0.10);
        }}

        .kpi-label {{
            font-size: 0.80rem;
            font-weight: 600;
            color: {COLORS['muted']};
            text-transform: uppercase;
            letter-spacing: 0.03em;
            margin-bottom: 0.35rem;
        }}
        .kpi-value {{
            font-size: 1.9rem;
            font-weight: 700;
            color: {COLORS['primary']};
            line-height: 1.1;
        }}
        .kpi-desc {{
            font-size: 0.78rem;
            color: {COLORS['muted']};
            margin-top: 0.3rem;
        }}
        .kpi-icon {{
            font-size: 1.4rem;
            color: {COLORS['accent']};
            background-color: {COLORS['hover']};
            border-radius: 8px;
            padding: 0.4rem 0.55rem;
            display: inline-block;
            margin-bottom: 0.55rem;
            font-family: 'Material Symbols Outlined';
        }}

        .section-title {{
            font-size: 1.02rem;
            font-weight: 700;
            color: {COLORS['primary']};
            margin: 0 0 0.7rem 0;
            padding-bottom: 0.5rem;
            border-bottom: 1px solid {COLORS['border']};
        }}

        .page-title {{
            font-size: 1.65rem;
            font-weight: 700;
            color: {COLORS['primary']};
            margin-bottom: 0.15rem;
        }}
        .page-subtitle {{
            font-size: 0.92rem;
            color: {COLORS['muted']};
            margin-bottom: 0.15rem;
        }}
        .breadcrumb {{
            font-size: 0.78rem;
            color: {COLORS['secondary']};
            margin-bottom: 0.15rem;
        }}
        .last-updated {{
            font-size: 0.74rem;
            color: {COLORS['muted']};
            margin-bottom: 0.9rem;
        }}

        .insight-item {{
            display: flex;
            justify-content: space-between;
            padding: 0.55rem 0;
            border-bottom: 1px dashed {COLORS['border']};
            font-size: 0.88rem;
        }}
        .insight-item:last-child {{ border-bottom: none; }}
        .insight-label {{ color: {COLORS['muted']}; font-weight: 500; }}
        .insight-value {{ color: {COLORS['primary']}; font-weight: 700; }}

        hr.bi-divider {{
            border: none;
            border-top: 1px solid {COLORS['border']};
            margin: 0.9rem 0;
        }}

        /* Dataframe polish (fallback tables) */
        div[data-testid="stDataFrame"] {{
            border: 1px solid {COLORS['border']};
            border-radius: 8px;
        }}

        /* Metrics tweak (not primary KPI style but used incidentally) */
        div[data-testid="stMetric"] {{
            background-color: {COLORS['card']};
            border: 1px solid {COLORS['border']};
            border-radius: 10px;
            padding: 0.8rem;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )