"""
tables.py
Professional data tables. Uses streamlit-aggrid (AgGrid) when available for
search, sort, filter, resize, hide-columns, and pagination. Falls back to a
styled st.dataframe if streamlit-aggrid is not installed, so the app never
crashes in an environment where the optional dependency is missing.
"""

import pandas as pd
import streamlit as st

from utils.styles import COLORS

try:
    from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode, JsCode
    AGGRID_AVAILABLE = True
except ImportError:
    AGGRID_AVAILABLE = False


def render_table(df: pd.DataFrame, key: str, page_size: int = 15, height: int = 420) -> None:
    """Renders a searchable, sortable, filterable, paginated table."""

    if AGGRID_AVAILABLE:
        gb = GridOptionsBuilder.from_dataframe(df)
        gb.configure_default_column(
            resizable=True, sortable=True, filter=True, floatingFilter=True,
        )
        gb.configure_pagination(paginationAutoPageSize=False, paginationPageSize=page_size)
        gb.configure_grid_options(domLayout="normal", enableCellTextSelection=True)
        gb.configure_side_bar(columns_panel=True, filters_panel=False)
        grid_options = gb.build()

        AgGrid(
            df,
            gridOptions=grid_options,
            height=height,
            theme="alpine",
            update_mode=GridUpdateMode.NO_UPDATE,
            fit_columns_on_grid_load=True,
            allow_unsafe_jscode=True,
            key=key,
        )
    else:
        st.info(
            "Install `streamlit-aggrid` for the full interactive table experience "
            "(resize, hide columns, sidebar filters). Showing a standard table instead.",
            icon="ℹ️",
        )
        search = st.text_input("Search", key=f"{key}_search", placeholder="Type to filter rows...")
        filtered = df
        if search:
            mask = df.apply(lambda row: row.astype(str).str.contains(search, case=False).any(), axis=1)
            filtered = df[mask]
        st.dataframe(filtered, use_container_width=True, height=height, hide_index=True)

    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button(
        "Export CSV",
        data=csv,
        file_name=f"{key}.csv",
        mime="text/csv",
        key=f"{key}_export",
    )
