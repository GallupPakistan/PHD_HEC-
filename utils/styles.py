"""
styles.py
Central style configuration for the HEI'sS Analytics Dashboard.
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
    BI look and feel. Call once, at the very top of app.py."""

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

        #MainMenu {{visibility: hidden;}}
        div[data-testid="stToolbar"] {{
            display: none !important;
        }}
        header {{
            height: 0 !important;
            min-height: 0 !important;
        }}
        footer {{visibility: hidden;}}

        /* ---------- Sidebar ---------- */
        section[data-testid="stSidebar"] {{
            background-color: {COLORS['primary']};
            border-right: none;
            border-radius: 14px;
            margin: 0.7rem 0 0.7rem 0.7rem;
            box-shadow: 0 6px 16px rgba(11, 58, 117, 0.22);
            width: 15.5rem !important;
            min-width: 15.5rem;
        }}
        section[data-testid="stSidebar"] > div {{
            border-radius: 14px;
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
            padding: 0.55rem 0.3rem;
            border-radius: 6px;
            font-weight: 500;
            font-size: 0.92rem;
            margin-bottom: 1px;
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

        section[data-testid="stSidebar"] *::-webkit-scrollbar {{
            width: 8px;
            height: 8px;
        }}
        section[data-testid="stSidebar"] *::-webkit-scrollbar-track {{
            background: rgba(255,255,255,0.08);
            border-radius: 8px;
        }}
        section[data-testid="stSidebar"] *::-webkit-scrollbar-thumb {{
            background-color: rgba(255,255,255,0.55);
            border-radius: 8px;
            border: 2px solid transparent;
            background-clip: padding-box;
        }}
        section[data-testid="stSidebar"] *::-webkit-scrollbar-thumb:hover {{
            background-color: rgba(255,255,255,0.75);
        }}
        section[data-testid="stSidebar"] * {{
            scrollbar-width: thin;
            scrollbar-color: rgba(255,255,255,0.55) rgba(255,255,255,0.08);
        }}

        .block-container {{
            padding-top: 0.6rem;
            padding-bottom: 2rem;
            padding-left: 2.2rem;
            padding-right: 2.2rem;
            max-width: 1500px;
        }}

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

        div[data-testid="stDataFrame"] {{
            border: 1px solid {COLORS['border']};
            border-radius: 8px;
        }}

        div[data-testid="stMetric"] {{
            background-color: {COLORS['card']};
            border: 1px solid {COLORS['border']};
            border-radius: 10px;
            padding: 0.8rem;
        }}

        /* ---------- Top bar (full page header) ---------- */
        .hec-topbar {{
            position: relative;
            background-color: {COLORS['primary']} !important;
            border-radius: 14px;
            padding: 1.3rem 1.6rem;
            margin: 0 0 1.4rem 0;
            display: flex;
            align-items: flex-start;
            justify-content: space-between;
            gap: 1.5rem;
            box-shadow: 0 6px 16px rgba(11, 58, 117, 0.22);
        }}
        .hec-topbar-left {{ display: flex; flex-direction: column; gap: 0.25rem; }}
        .hec-topbar-crumbs {{
            display: flex; align-items: center; gap: 0.35rem;
            font-size: 0.76rem; color: rgba(255,255,255,0.6); white-space: nowrap;
        }}
        .hec-topbar-current {{ color: #FFFFFF; font-weight: 700; }}
        .hec-topbar-sep {{ font-size: 14px; color: rgba(255,255,255,0.4); }}
        .hec-topbar-title {{
            font-size: 1.5rem; font-weight: 800; color: #FFFFFF; margin-top: 0.3rem;
        }}
        .hec-topbar-subtitle {{
            font-size: 0.86rem; color: rgba(255,255,255,0.8); max-width: 640px; margin-top: 0.1rem;
        }}
        .hec-topbar-lastupdated-inline {{
            font-size: 0.72rem; color: rgba(255,255,255,0.55); margin-top: 0.35rem;
        }}
        .hec-topbar-right {{ display: flex; align-items: center; padding-top: 0.3rem; }}
        .hec-topbar-stat {{
            text-align: right;
            background-color: rgba(255,255,255,0.1);
            border-radius: 10px;
            padding: 0.6rem 1.1rem;
        }}
        .hec-topbar-stat-value {{
            font-size: 1.5rem; font-weight: 800; color: #FFFFFF; line-height: 1.1;
        }}
        .hec-topbar-stat-label {{
            font-size: 0.7rem; color: rgba(255,255,255,0.7); margin-top: 0.15rem;
            text-transform: uppercase; letter-spacing: 0.03em;
        }}

        @media (max-width: 900px) {{
            .hec-topbar-center {{ display: none; }}
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )