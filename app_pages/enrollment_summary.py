"""
app_pages/enrollment_summary.py
Enrollment Summary — headline KPIs and year-wise Male/Female/Total trend,
plus gender and sector distribution for the selected filters.
"""

import pandas as pd
import streamlit as st

from components.cards import section_card_start, section_card_end
from components.kpis import render_kpi_row
from components.tables import render_table
from components.filters import render_filters
from components import charts
from utils.loader import load_master_data, filter_master_df


def _format_large_number(value: float) -> str:
    """Formats large numbers with M/K suffixes, e.g. 23,700,000 -> '23.7M'."""
    value = float(value)
    if abs(value) >= 1_000_000:
        return f"{value / 1_000_000:.1f}M"
    if abs(value) >= 1_000:
        return f"{value / 1_000:.1f}K"
    return f"{value:,.0f}"


def render(data: dict) -> None:
    master_data = load_master_data()

    filters = render_filters(master_data, key_prefix="summary")

    # --- Core year-wise trend (Male/Female/Total) ---------------------------
    summary_df = filter_master_df(master_data["enrolment_summary"], filters)

    if summary_df.empty:
        st.warning("No enrollment summary data for the selected filters.")
        return

    # Province/Gender/Sector filters don't apply here — the national
    # year-wise summary sheet has no such breakdown (see data_quality_notes).
    if filters.get("provinces") or filters.get("genders") or filters.get("sectors"):
        st.caption(
            "Note: Province/Gender/Sector filters don't affect the KPI cards or "
            "trend chart below — this national summary is only broken down by year. "
            "See Enrollment Details for province/sector/gender-level breakdowns."
        )

    if len(summary_df) == 1:
        row = summary_df.iloc[0]
        total_val, male_val, female_val = row["total"], row["male"], row["female"]
        period_label = f"{row['year']}"
    else:
        total_val = summary_df["total"].sum()
        male_val = summary_df["male"].sum()
        female_val = summary_df["female"].sum()
        years_span = f"{summary_df['year'].min()}–{summary_df['year'].max()}"
        period_label = f"Cumulative, {len(summary_df)} years ({years_span})"

    # Decade growth — always computed from the full (unfiltered) history,
    # since this is a fixed historical comparison, not a filtered-selection metric.
    full_summary = master_data["enrolment_summary"]
    first_row, last_row = full_summary.iloc[0], full_summary.iloc[-1]
    decade_growth = ((last_row["total"] - first_row["total"]) / first_row["total"] * 100) if first_row["total"] else 0
    decade_growth_desc = f"{first_row['year']} → {last_row['year']}"

    kpis = [
        {"icon": "groups", "label": "Total Enrollment", "value": _format_large_number(total_val),
         "description": period_label},
        {"icon": "man", "label": "Male Students", "value": _format_large_number(male_val),
         "description": period_label},
        {"icon": "woman", "label": "Female Students", "value": _format_large_number(female_val),
         "description": period_label},
        {"icon": "trending_up", "label": "Decade Growth", "value": f"{decade_growth:+.1f}%",
         "description": decade_growth_desc},
    ]
    render_kpi_row(kpis)

    with st.expander("Verify these numbers"):
        st.caption(
            "Cross-check: these KPI values come directly from the row below in "
            "enrolment_summary (from enrollment_data(claude).xlsx). Male + Female "
            "should equal Total; open the same row in the Excel file to confirm."
        )
        st.dataframe(summary_df, use_container_width=True, hide_index=True)

    st.write("")
    trend_col1, trend_col2 = st.columns(2)

    with trend_col1:
        section_card_start("Enrollment Over the Last Decade")
        charts.render(charts.dual_line_chart_categorical(
            full_summary, x="year", y1="male", y2="female",
            name1="Male", name2="Female",
        ))
        section_card_end()

    with trend_col2:
        section_card_start("Male / Female Enrollment Trend")
        charts.render(charts.bar_group_with_trend_area(
            summary_df, x="year", y_cols=["male", "female"], names=["Male", "Female"],
            trend_col="total", trend_name="Total",
        ))
        section_card_end()

    st.write("")
    col1, col2 = st.columns(2)

    # --- Gender distribution (from province+gender breakdown, where available) ---
    with col1:
        section_card_start("Gender Distribution")
        pg_df = filter_master_df(master_data["enrolment_by_province_gender"], filters)
        if not pg_df.empty:
            gender_totals = pg_df.groupby("gender", as_index=False)["count"].sum()
            charts.render(charts.donut_chart(gender_totals, names="gender", values="count"))
        else:
            gender_totals = pd.DataFrame({
                "gender": ["Male", "Female"],
                "count": [male_val, female_val],
            })
            charts.render(charts.donut_chart(gender_totals, names="gender", values="count"))
            st.caption("Province/Sector-level gender breakdown not available for this year — showing overall totals.")
        section_card_end()

    # --- Sector distribution (Public vs Private) ----------------------------
    with col2:
        section_card_start("Sector Distribution")
        sector_df = filter_master_df(master_data["enrolment_by_sector"], filters)
        if not sector_df.empty:
            sector_totals = sector_df.groupby("sector", as_index=False)["total"].sum()
            charts.render(charts.donut_chart(sector_totals, names="sector", values="total"))
        else:
            st.info("No sector-wise data available for the selected year(s).")
        section_card_end()

    st.write("")
    section_card_start("Summary Table")
    render_table(summary_df, key="enrollment_summary_table")
    section_card_end()