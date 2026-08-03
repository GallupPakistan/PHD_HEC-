"""
sidebar.py
Renders the permanent left navigation sidebar: logo area, dashboard title,
grouped navigation buttons with icons and section labels, a divider, a
theme toggle, and a footer.

Matches the reference image:
- "Overview" alone at top, no section label above it
- "DIRECTORY" section: Universities, PhD Directory
- "ANALYTICS" section: Enrollment Summary, Enrollment Ratios, Enrollment Details
- "OTHERS" section: About

Icons are rendered using Streamlit's native `icon=":material/<name>:"`
button parameter (Streamlit >= 1.31) - your app already loads the
Material Symbols Outlined font in styles.py, so these render as real
icons next to each label with zero extra HTML/CSS needed.
"""

import streamlit as st

from utils.loader import get_last_updated

# Each section is (section_label_or_None, [(label, material_icon_name), ...])
NAV_SECTIONS = [
    (None, [
        ("Overview", "dashboard"),
    ]),
    ("DIRECTORY", [
        ("Universities", "school"),
        ("PhD Directory", "workspace_premium"),
    ]),
    ("ANALYTICS", [
        ("Enrollment Summary", "monitoring"),
        ("Enrollment Ratios", "percent"),
        ("Enrollment Details", "groups"),
    ]),
    ("OTHERS", [
        ("About", "info"),
    ]),
]


def render_sidebar() -> str:
    """Renders the sidebar and returns the currently selected page name."""

    if "active_page" not in st.session_state:
        st.session_state.active_page = "Overview"

    with st.sidebar:
        st.markdown(
            """
            <div style="display:flex;align-items:center;gap:10px;padding:0.4rem 0.2rem 1rem 0;">
                <div style="width:36px;height:36px;border-radius:8px;background-color:rgba(255,255,255,0.14);
                            display:flex;align-items:center;justify-content:center;">
                    <span class="material-symbols-outlined" style="font-size:20px;">account_balance</span>
                </div>
                <div>
                    <div style="font-weight:700;font-size:0.95rem;line-height:1.1;">HEI's Analytics Dashboard</div>
                    <div style="font-size:0.72rem;opacity:0.7;"></div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.markdown('<hr style="border-color:rgba(255,255,255,0.15);margin:0.2rem 0 0.7rem 0;">', unsafe_allow_html=True)

        for section_label, items in NAV_SECTIONS:
            if section_label:
                st.markdown(
                    f'<div class="nav-section-label">{section_label}</div>',
                    unsafe_allow_html=True,
                )
            for label, icon in items:
                is_active = st.session_state.active_page == label
                wrapper_class = "nav-active" if is_active else ""
                st.markdown(f'<div class="{wrapper_class}">', unsafe_allow_html=True)
                if st.button(label, key=f"nav_{label}", use_container_width=True,
                             icon=f":material/{icon}:"):
                    st.session_state.active_page = label
                st.markdown("</div>", unsafe_allow_html=True)

        st.markdown('<hr style="border-color:rgba(255,255,255,0.15);margin:0.9rem 0;">', unsafe_allow_html=True)

        st.toggle("Dark surface", value=False, key="theme_toggle", disabled=True,
                   help="Reserved for future theming — light enterprise theme is currently active.")

        st.markdown(
            """
            <div style="position:relative;margin-top:1.2rem;font-size:0.72rem;opacity:0.65;">
                Higher Education Commission<br>
                Analytics Platform · v1.0
            </div>
            """,
            unsafe_allow_html=True,
        )

    return st.session_state.active_page