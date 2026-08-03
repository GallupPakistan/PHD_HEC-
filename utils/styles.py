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
        .nav-section-label {{
            font-size: 0.68rem;
            font-weight: 700;
            color: rgba(255,255,255,0.45) !important;
            text-transform: uppercase;
            letter-spacing: 0.06em;
            margin: 0.9rem 0 0.25rem 0.4rem;
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
            overflow: hidden;
            background-color: {COLORS['primary']} !important;
            border-radius: 12px;
            padding: 1.5rem 2rem;
            margin: 0 0 1.4rem 0;
            box-shadow: 0 10px 24px rgba(0, 0, 0, 0.2);
            color: #FFFFFF;
        }}

        /* faint giant building icon watermark */
        .hec-topbar-watermark {{
            position: absolute;
            top: -2rem;
            right: 30%; /* Shifted closer to the center like the image */
            opacity: 0.05;
            pointer-events: none;
        }}
        .hec-topbar-watermark .material-symbols-outlined {{
            font-size: 18rem;
            color: #FFFFFF;
        }}

        /* dotted pattern, top right corner */
        .hec-topbar-dots {{
            position: absolute;
            top: 1.3rem;
            right: 1.6rem;
            width: 120px;
            height: 80px;
            background-image: radial-gradient(rgba(255,255,255,0.2) 1.5px, transparent 1.5px);
            background-size: 12px 12px;
            pointer-events: none;
        }}

        /* ---- top row: brand (logo + name) on the left, breadcrumb ---- */
        .hec-topbar-toprow {{
            position: relative;
            display: flex;
            align-items: center;
            justify-content: flex-start; /* Aligns items to the left */
            margin-bottom: 2rem;
        }}
        .hec-topbar-brand {{
            display: flex;
            align-items: center;
            gap: 0.8rem;
        }}
        .hec-topbar-logo-circle {{
            width: 44px;
            height: 44px;
            border-radius: 50%;
            background-color: rgba(255,255,255,0.1);
            display: flex;
            align-items: center;
            justify-content: center;
            border: 1px solid rgba(255,255,255,0.15);
        }}
        .hec-topbar-logo-circle .material-symbols-outlined {{
            font-size: 24px;
            color: #FFFFFF;
        }}
        .hec-topbar-brand-text {{
            display: flex;
            flex-direction: column;
            line-height: 1.2;
        }}
        .hec-topbar-brand-name {{
            font-size: 1.1rem;
            font-weight: 700;
            color: #FFFFFF;
            letter-spacing: 0.02em;
        }}
        .hec-topbar-brand-sub {{
            font-size: 0.85rem;
            font-weight: 500;
            color: #79AFFF; /* Lighter blue to match image */
        }}

        /* Separator between Brand and Breadcrumbs */
        .hec-topbar-vsep {{
            width: 1px;
            height: 32px;
            background-color: rgba(255,255,255,0.15);
            margin: 0 1.5rem;
        }}

        .hec-topbar-crumbs {{
            display: flex;
            align-items: center;
            gap: 0.6rem;
            font-size: 0.85rem;
            color: rgba(255,255,255,0.7);
            white-space: nowrap;
        }}
        .hec-topbar-crumb-icon-badge {{
            width: 30px;
            height: 30px;
            border-radius: 8px;
            background-color: rgba(0, 0, 0, 0.25); /* Dark recessed badge */
            display: inline-flex;
            align-items: center;
            justify-content: center;
            box-shadow: inset 0 1px 3px rgba(0,0,0,0.3);
        }}
        .hec-topbar-crumb-icon-badge .material-symbols-outlined {{
            font-size: 16px;
            color: #FFFFFF;
        }}
        .hec-topbar-sep {{ color: rgba(255,255,255,0.35); margin: 0 0.2rem; }}
        .hec-topbar-crumb {{ color: rgba(255,255,255,0.8); }}
        .hec-topbar-current {{ color: #FFFFFF; font-weight: 600; }}

        /* ---- bottom row: title/subtitle/last-updated on the left, stat card on the right ---- */
        .hec-topbar-bottomrow {{
            position: relative;
            display: flex;
            align-items: flex-end;
            justify-content: space-between;
            gap: 1.5rem;
        }}
        .hec-topbar-left {{ display: flex; flex-direction: column; gap: 0.6rem; max-width: 650px; }}

        .hec-topbar-title-wrapper {{
            display: flex;
            align-items: center;
            gap: 0.8rem;
        }}
        .hec-topbar-accent-bar {{
            width: 4px;
            height: 2rem;
            border-radius: 4px;
            background-color: #3b82f6; /* Bright blue accent line */
        }}
        .hec-topbar-title {{
            font-size: 2rem;
            font-weight: 700;
            color: #FFFFFF;
            line-height: 1;
            letter-spacing: -0.01em;
        }}
        .hec-topbar-subtitle {{
            font-size: 0.9rem;
            color: rgba(255,255,255,0.75);
            line-height: 1.5;
            margin-bottom: 0.3rem;
        }}
        .hec-topbar-lastupdated-pill {{
            display: inline-flex;
            align-items: center;
            gap: 0.5rem;
            background-color: rgba(0, 0, 0, 0.2);
            border: 1px solid rgba(255,255,255,0.05);
            border-radius: 8px;
            padding: 0.4rem 0.8rem;
            font-size: 0.8rem;
            color: rgba(255,255,255,0.7);
            width: fit-content;
        }}
        .hec-topbar-lastupdated-pill .material-symbols-outlined {{
            font-size: 16px;
            color: #79AFFF;
        }}
        .hec-topbar-lastupdated-pill b {{ color: #FFFFFF; font-weight: 600; }}

        /* Custom Stat Card Configuration */
        .hec-topbar-right {{ display: flex; align-items: center; }}
        .hec-topbar-stat {{
            display: flex;
            align-items: center;
            background: linear-gradient(135deg, rgba(255,255,255,0.12), rgba(255,255,255,0.03));
            border: 1px solid rgba(255,255,255,0.15);
            border-radius: 12px;
            padding: 1rem 1.5rem;
            box-shadow: 0 8px 24px rgba(0,0,0,0.2);
            backdrop-filter: blur(10px);
        }}
        .hec-topbar-stat-icon-circle {{
            width: 52px;
            height: 52px;
            border-radius: 50%;
            background-color: #0F4C9D; /* Bright blue background for the icon */
            border: 2px solid #1A60BC;
            display: flex;
            align-items: center;
            justify-content: center;
            flex-shrink: 0;
        }}
        .hec-topbar-stat-icon-circle .material-symbols-outlined {{
            font-size: 28px;
            color: #FFFFFF;
        }}
        .hec-topbar-stat-vsep {{
            width: 1px;
            height: 44px;
            background-color: rgba(255,255,255,0.15);
            margin: 0 1.5rem;
        }}
        .hec-topbar-stat-text {{
            display: flex;
            flex-direction: column;
            justify-content: center;
        }}
        .hec-topbar-stat-value {{
            font-size: 2rem;
            font-weight: 800;
            color: #FFFFFF;
            line-height: 1;
            letter-spacing: -0.02em;
        }}
        .hec-topbar-stat-label {{
            font-size: 0.65rem;
            font-weight: 600;
            color: rgba(255,255,255,0.7);
            text-transform: uppercase;
            letter-spacing: 0.05em;
            margin-top: 0.3rem;
        }}

        @media (max-width: 900px) {{
            .hec-topbar-watermark {{ display: none; }}
            .hec-topbar-bottomrow {{ flex-direction: column; align-items: flex-start; }}
            .hec-topbar-stat {{ width: 100%; justify-content: flex-start; }}
        }}

        @media (max-width: 900px) {{
            .hec-topbar-center {{ display: none; }}
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )