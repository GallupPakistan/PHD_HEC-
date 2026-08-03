"""
charts.py
Plotly chart factories, all sharing one consistent visual language:
transparent backgrounds, consistent margins/height, no toolbar, and the
enterprise color palette defined in utils.styles.
"""

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from utils.styles import COLORS, CHART_SEQUENCE, FONT_FAMILY

CHART_HEIGHT = 350
CONFIG = {"displayModeBar": False, "responsive": True}


def _base_layout(fig: go.Figure, show_legend: bool = False) -> go.Figure:
    fig.update_layout(
        height=CHART_HEIGHT,
        margin=dict(l=10, r=15, t=25, b=15),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family=FONT_FAMILY, color=COLORS["text"], size=12),
        showlegend=show_legend,
    )
    fig.update_xaxes(showgrid=True, gridcolor=COLORS["border"], zeroline=False)
    fig.update_yaxes(showgrid=False, zeroline=False)
    return fig


def render(fig: go.Figure) -> None:
    st.plotly_chart(fig, use_container_width=True, config=CONFIG)


def horizontal_bar(df: pd.DataFrame, x: str, y: str, top_n: int = 5, color: str = None) -> go.Figure:
    """
    Perfectly Fitted Horizontal Bar Chart:
    - Auto-expands x-axis range (+30%) so labels NEVER cut off.
    - Clean custom hover template.
    - Limits to top_n dynamically without layout overflow.
    """
    if df.empty:
        return _base_layout(go.Figure())

    plot_df = df.dropna(subset=[x, y]).sort_values(by=x, ascending=False).head(top_n).copy()

    total_val = plot_df[x].sum() if plot_df[x].sum() > 0 else 1
    plot_df["pct"] = (plot_df[x] / total_val) * 100
    plot_df["display_text"] = plot_df.apply(lambda r: f" {r[x]:,.0f} ({r['pct']:.1f}%)", axis=1)

    plot_df = plot_df.sort_values(by=x, ascending=True)

    fig = px.bar(
        plot_df,
        x=x,
        y=y,
        orientation="h",
        color_discrete_sequence=[color or COLORS["primary"]],
        text="display_text",
    )

    fig.update_traces(
        textposition="outside",
        textfont=dict(size=11, color=COLORS["text"]),
        marker_line_width=0,
        hovertemplate="<b>%{y}</b><br>Count: %{x:,.0f}<extra></extra>",
    )

    fig = _base_layout(fig)

    max_val = plot_df[x].max() if not plot_df.empty else 100
    fig.update_xaxes(range=[0, max_val * 1.30], title=None)
    fig.update_yaxes(title=None)

    return fig


def column_chart(df: pd.DataFrame, x: str, y: str, top_n: int = 5) -> go.Figure:
    """
    Clean Fitted Column Chart:
    - Auto-expands Y-axis so numbers above bars fit in given container space.
    """
    if df.empty:
        return _base_layout(go.Figure())

    plot_df = df.dropna(subset=[x, y]).sort_values(by=y, ascending=False).head(top_n).copy()

    total_val = plot_df[y].sum() if plot_df[y].sum() > 0 else 1
    plot_df["pct"] = (plot_df[y] / total_val) * 100
    plot_df["display_text"] = plot_df.apply(lambda r: f"{r[y]:,.0f}<br>({r['pct']:.1f}%)", axis=1)

    fig = px.bar(
        plot_df,
        x=x,
        y=y,
        color_discrete_sequence=[COLORS["secondary"]],
        text="display_text",
    )

    fig.update_traces(
        textposition="outside",
        textfont=dict(size=10),
        marker_line_width=0,
        hovertemplate="<b>%{x}</b><br>Count: %{y:,.0f}<extra></extra>",
    )

    fig = _base_layout(fig)

    max_val = plot_df[y].max() if not plot_df.empty else 100
    fig.update_yaxes(range=[0, max_val * 1.25], title=None)
    fig.update_xaxes(title=None)

    return fig


def donut_chart(df: pd.DataFrame, names: str, values: str, top_n: int = 5) -> go.Figure:
    """
    Proportional Donut Chart:
    - Fits smoothly inside dashboard cards without label overlapping.
    """
    if df.empty:
        return _base_layout(go.Figure())

    plot_df = df.dropna(subset=[names, values]).sort_values(by=values, ascending=False).head(top_n)

    fig = px.pie(
        plot_df,
        names=names,
        values=values,
        hole=0.60,
        color_discrete_sequence=CHART_SEQUENCE,
    )

    fig.update_traces(
        textposition="inside",
        textinfo="percent",
        texttemplate="<b>%{percent:.1%}</b>",
        insidetextfont=dict(size=11, color="#FFFFFF"),
        marker=dict(line=dict(color=COLORS.get("card", "#000000"), width=1.5)),
        hovertemplate="<b>%{label}</b><br>Value: %{value:,.0f}<br>Share: %{percent}<extra></extra>",
    )

    fig = _base_layout(fig, show_legend=True)

    fig.update_layout(
        margin=dict(l=10, r=10, t=10, b=10),
        legend=dict(
            orientation="h",
            yanchor="top",
            y=-0.05,
            xanchor="center",
            x=0.5,
            font=dict(size=11),
        ),
    )
    return fig

def bar_group_with_trend_area(df, x: str, y_cols: list, names: list = None,
                               trend_col: str = None, trend_name: str = "Trend",
                               bar_colors: list = None) -> go.Figure:
    """
    Grouped bar chart (e.g. Male / Female / Total per year) with a
    translucent area + line trend overlaid on top of one series.
 
    df         : dataframe, one row per x category (already in year order)
    x          : column name for x-axis categories (e.g. "year")
    y_cols     : list of column names to plot as grouped bars, e.g.
                 ["male", "female", "total"]
    names      : display names for the bars (defaults to y_cols)
    trend_col  : which column to draw the area/line trend for
                 (defaults to the last entry in y_cols, e.g. "total")
    trend_name : legend label for the trend line
    bar_colors : optional list of 3 colors for the bars (light blue,
                 blue, green look from the reference image); defaults to
                 a light/dark/accent triple pulled from CHART_SEQUENCE
    """
    if df.empty:
        return _base_layout(go.Figure())
 
    names = names or y_cols
    trend_col = trend_col or y_cols[-1]
    x_vals = df[x].astype(str).tolist()
 
    colors = bar_colors or [
        "#AFC9E8",              # light blue
        COLORS.get("primary", "#1F3864"),   # blue
        COLORS.get("success", "#2E8B57"),   # green
    ]
 
    fig = go.Figure()
 
    # --- grouped bars ---
    for i, col in enumerate(y_cols):
        fig.add_trace(go.Bar(
            x=x_vals,
            y=df[col],
            name=names[i],
            marker_color=colors[i % len(colors)],
            marker_line_color="rgba(0,0,0,0.15)",
            marker_line_width=1,
            hovertemplate=f"{names[i]}: %{{y:,.0f}}<extra></extra>",
        ))
 
    # --- translucent area + line trend on top ---
    fig.add_trace(go.Scatter(
        x=x_vals,
        y=df[trend_col],
        name=trend_name,
        mode="lines",
        line=dict(color="rgba(220,60,60,0.9)", width=2, shape="spline"),
        fill="tozeroy",
        fillcolor="rgba(220,60,60,0.15)",
        hovertemplate=f"{trend_name}: %{{y:,.0f}}<extra></extra>",
    ))
 
    fig = _base_layout(fig, show_legend=True)
    fig.update_layout(
        barmode="group",
        bargap=0.25,
        bargroupgap=0.08,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5),
        margin=dict(l=10, r=15, t=25, b=15),
    )
    fig.update_xaxes(
        title=None,
        type="category",
        categoryorder="array",
        categoryarray=x_vals,
    )
    fig.update_yaxes(title=None)
    return fig

def line_chart(df: pd.DataFrame, x: str, y: str) -> go.Figure:
    fig = px.line(df, x=x, y=y, markers=True, color_discrete_sequence=[COLORS["primary"]])
    fig.update_traces(
        line_width=2.5,
        marker_size=6,
        hovertemplate="%{x}<br><b>%{y:,.0f}</b><extra></extra>",
    )
    fig = _base_layout(fig)
    fig.update_xaxes(title=None)
    fig.update_yaxes(title=None)
    return fig


def area_chart(df: pd.DataFrame, x: str, y: str) -> go.Figure:
    fig = px.area(df, x=x, y=y, color_discrete_sequence=[COLORS["accent"]])
    fig.update_traces(
        line_width=2,
        hovertemplate="%{x}<br><b>%{y:,.0f}</b><extra></extra>",
    )
    fig = _base_layout(fig)
    fig.update_xaxes(title=None)
    fig.update_yaxes(title=None)
    return fig

def dual_line_chart(df: pd.DataFrame, x: str, y1: str, y2: str, name1: str, name2: str,
                     milestone_year: int = None, milestone_label: str = None) -> go.Figure:
    """Two-line trend chart matching the HEC reference style."""

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df[x], y=df[y1], mode="lines+markers+text", name=name1,
        line=dict(color=COLORS["success"], width=2.5), marker=dict(size=5),
        text=df[y1].astype(int).astype(str), textposition="top center",
        textfont=dict(size=9, color=COLORS["success"]),
        hovertemplate=f"{name1}: %{{y}}<extra></extra>",
    ))
    fig.add_trace(go.Scatter(
        x=df[x], y=df[y2], mode="lines+markers+text", name=name2,
        line=dict(color=COLORS["primary"], width=2.5), marker=dict(size=5),
        text=df[y2].astype(int).astype(str), textposition="bottom center",
        textfont=dict(size=9, color=COLORS["primary"]),
        hovertemplate=f"{name2}: %{{y}}<extra></extra>",
    ))

    if milestone_year is not None:
        fig.add_vline(x=milestone_year, line_width=2, line_dash="dash", line_color="orange")
        fig.add_annotation(
            x=milestone_year, y=0, yref="paper", yanchor="bottom",
            text=milestone_label or f"Established in: {milestone_year}",
            showarrow=False, font=dict(size=11, color="orange"), xshift=6, align="left",
        )

    fig = _base_layout(fig, show_legend=True)
    fig.update_layout(
        hovermode="x unified",
        hoverlabel=dict(namelength=-1, font_size=11),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5),
        margin=dict(l=10, r=15, t=25, b=40),
    )
    fig.update_xaxes(title=None)
    fig.update_yaxes(title=None)
    return fig
def dual_line_chart_categorical(df: pd.DataFrame, x: str, y1: str, y2: str, name1: str, name2: str) -> go.Figure:
    """
    Two-line trend chart for STRING/period-style x values (e.g. "2009-10",
    "2011-12", "2022-23") where a numeric/date axis would misparse the
    labels. Forces a category axis in the exact row order of df, with a
    visible marker + value label at every point.
    """
    if df.empty:
        return _base_layout(go.Figure())
 
    x_vals = df[x].astype(str).tolist()
 
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=x_vals, y=df[y1], mode="lines+markers+text", name=name1,
        line=dict(color=COLORS["success"], width=2.5), marker=dict(size=6),
        text=df[y1].astype(int).astype(str), textposition="top center",
        textfont=dict(size=9, color=COLORS["success"]),
        hovertemplate=f"{name1}: %{{y:,.0f}}<extra></extra>",
    ))
    fig.add_trace(go.Scatter(
        x=x_vals, y=df[y2], mode="lines+markers+text", name=name2,
        line=dict(color=COLORS["primary"], width=2.5), marker=dict(size=6),
        text=df[y2].astype(int).astype(str), textposition="bottom center",
        textfont=dict(size=9, color=COLORS["primary"]),
        hovertemplate=f"{name2}: %{{y:,.0f}}<extra></extra>",
    ))
 
    fig = _base_layout(fig, show_legend=True)
    fig.update_layout(
        hovermode="x unified",
        hoverlabel=dict(namelength=-1, font_size=11),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5),
        margin=dict(l=10, r=15, t=25, b=40),
    )
    fig.update_xaxes(
        title=None,
        type="category",
        categoryorder="array",
        categoryarray=x_vals,
    )
    fig.update_yaxes(title=None)
    return fig

def treemap_chart(df, path: str, values: str, top_n: int = 12) -> go.Figure:
    """
    Clean, professional treemap:
    - path      : column with the category label (e.g. "level")
    - values    : column with the numeric size (e.g. "count")
    - top_n     : max number of segments shown
    """
    plot_df = df.dropna(subset=[path, values]).copy()
    plot_df = plot_df[plot_df[values] > 0].sort_values(values, ascending=False).head(top_n)
 
    if plot_df.empty:
        return _base_layout(go.Figure())
 
    total = plot_df[values].sum()
    plot_df["_pct"] = plot_df[values] / total * 100
    plot_df["_label"] = plot_df[path].astype(str).str.replace(", ", "<br>").str.replace(" - ", "<br>")
 
    fig = px.treemap(
        plot_df,
        path=[px.Constant("All"), "_label"],
        values=values,
        color="_label",
        color_discrete_sequence=CHART_SEQUENCE,
    )
 
    fig.update_traces(
        texttemplate="<b>%{label}</b><br>%{value:,.0f}<br>(%{percentEntry:.1%})",
        textfont=dict(family=FONT_FAMILY, size=13, color="#FFFFFF"),
        textposition="middle center",
        hovertemplate="<b>%{label}</b><br>Count: %{value:,.0f}<br>Share of total: %{percentEntry:.1%}<extra></extra>",
        marker=dict(line=dict(width=2, color=COLORS.get("card", "#FFFFFF"))),
        tiling=dict(pad=3),
        root_color="rgba(0,0,0,0)",
    )
 
    # Root/parent cell ("All") should stay invisible-ish and not steal a
    # big label of its own
    fig.data[0].textfont.size = 13
 
    fig = _base_layout(fig)
    fig.update_layout(
        margin=dict(l=5, r=5, t=5, b=5),
        uniformtext=dict(minsize=10, mode="hide"),  # <-- hides text instead of overlapping when box too small
    )
    return fig


def pareto_chart(df: pd.DataFrame, category: str, value: str, cum_pct_col: str, top_n: int = 10) -> go.Figure:
    """
    Balanced Pareto Chart:
    - Reduced top_n to 10 so x-axis labels are comfortably legible.
    """
    plot_df = df.head(top_n)
    fig = go.Figure()

    fig.add_trace(
        go.Bar(
            x=plot_df[category],
            y=plot_df[value],
            name="Records",
            marker_color=COLORS["primary"],
        )
    )

    fig.add_trace(
        go.Scatter(
            x=plot_df[category],
            y=plot_df[cum_pct_col],
            name="Cumulative %",
            yaxis="y2",
            mode="lines+markers",
            line=dict(color=COLORS["accent"], width=2.5),
        )
    )

    fig = _base_layout(fig, show_legend=True)
    fig.update_layout(
        height=400,
        margin=dict(l=15, r=15, t=25, b=100),
        yaxis2=dict(overlaying="y", side="right", range=[0, 110], showgrid=False, title=None),
        xaxis=dict(tickangle=-35, tickfont=dict(size=10), title=None),
        yaxis=dict(title=None),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    )
    return fig
    
def funnel_chart(df, stage_col: str, value_col: str, colors: list = None) -> go.Figure:
    """
    Funnel / progression chart - e.g. Level-wise Enrollment:
    Bachelor -> Master -> MS/MPhil -> PhD (or Lead -> Opportunity ->
    Qualified -> Sold -> Retained, as in the reference image).
 
    df         : dataframe, one row per stage, already in the order you
                 want top-to-bottom (largest stage first)
    stage_col  : column with the stage label (e.g. "level")
    value_col  : column with the numeric value (e.g. "count")
    colors     : optional list of colors, dark-to-light, one per stage
    """
    if df.empty:
        return _base_layout(go.Figure())
 
    plot_df = df.dropna(subset=[stage_col, value_col]).copy()
    first_val = plot_df[value_col].iloc[0] if plot_df[value_col].iloc[0] else 1
    plot_df["_pct_of_first"] = plot_df[value_col] / first_val * 100
 
    default_palette = [
        "#1F3864", "#2E5A87", "#3D82A8", "#5FA9B8", "#8FC7C0", "#C4E4D8",
    ]
    palette = colors or default_palette
    n = len(plot_df)
    bar_colors = [palette[i % len(palette)] for i in range(n)]
 
    fig = go.Figure(go.Funnel(
        y=plot_df[stage_col],
        x=plot_df[value_col],
        textposition="inside",
        texttemplate="<b>%{label}</b><br>%{value:,.0f}",
        textfont=dict(family=FONT_FAMILY, size=13, color="#FFFFFF"),
        marker=dict(color=bar_colors, line=dict(width=1, color="rgba(255,255,255,0.5)")),
        connector=dict(line=dict(color=COLORS.get("border", "#D9D9D9"), width=1, dash="dot")),
        hovertemplate="<b>%{label}</b><br>Count: %{value:,.0f}<br>Share of first stage: %{percentInitial}<extra></extra>",
    ))
    # positioned using paper-relative y matching each funnel row
    n_rows = len(plot_df)
    for i, (_, row) in enumerate(plot_df.iterrows()):
        y_pos = 1 - (i + 0.5) / n_rows
        fig.add_annotation(
            x=0.0, y=y_pos, xref="paper", yref="paper",
            text=f"<b>{row['_pct_of_first']:.1f}%</b>",
            showarrow=False,
            font=dict(size=12, color=bar_colors[i], family=FONT_FAMILY),
            xanchor="right", align="right",
            xshift=-8,
        )
 
    fig = _base_layout(fig, show_legend=False)
    fig.update_layout(
        margin=dict(l=70, r=15, t=15, b=15),
        funnelmode="stack",
    )
    return fig

def lollipop_chart(df, x: str, y: str, top_n: int = 10) -> go.Figure:
    """
    Professional lollipop chart:
    - x : numeric value column (e.g. "count")
    - y : category column (e.g. "province")
    """
    if df.empty:
        return _base_layout(go.Figure())
 
    plot_df = df.dropna(subset=[x, y]).sort_values(by=x, ascending=True).head(top_n).copy()
    total = plot_df[x].sum() if plot_df[x].sum() > 0 else 1
    plot_df["_pct"] = plot_df[x] / total * 100
 
    max_val = plot_df[x].max() if not plot_df.empty else 100
    min_size, max_size = 10, 22
    if plot_df[x].max() != plot_df[x].min():
        plot_df["_marker_size"] = min_size + (plot_df[x] - plot_df[x].min()) / \
            (plot_df[x].max() - plot_df[x].min()) * (max_size - min_size)
    else:
        plot_df["_marker_size"] = (min_size + max_size) / 2
 
    fig = go.Figure()
 
    # soft alternating row bands for readability
    for i in range(len(plot_df)):
        if i % 2 == 0:
            fig.add_shape(
                type="rect", xref="paper", yref="y",
                x0=0, x1=1, y0=i - 0.5, y1=i + 0.5,
                fillcolor="rgba(0,0,0,0.025)", line_width=0, layer="below",
            )
 
    # stems
    for _, row in plot_df.iterrows():
        fig.add_shape(
            type="line",
            x0=0, x1=row[x], y0=row[y], y1=row[y],
            line=dict(color=COLORS["border"], width=3),
            layer="below",
        )
 
    # heads + value labels
    fig.add_trace(go.Scatter(
        x=plot_df[x], y=plot_df[y], mode="markers+text",
        marker=dict(
            size=plot_df["_marker_size"],
            color=COLORS["primary"],
            line=dict(width=1.5, color="white"),
        ),
        text=[f"  {v:,.0f}" for v in plot_df[x]],
        textposition="middle right",
        textfont=dict(size=11, color=COLORS["text"], family=FONT_FAMILY),
        customdata=plot_df["_pct"],
        hovertemplate="<b>%{y}</b><br>Count: %{x:,.0f}<br>Share: %{customdata:.1f}%<extra></extra>",
    ))
 
    fig = _base_layout(fig)
    fig.update_layout(showlegend=False)
    fig.update_xaxes(title=None, range=[0, max_val * 1.25], showgrid=True)
    fig.update_yaxes(title=None)
    return fig
 

# ---------------------------------------------------------------------------
# Enrollment-module additions (Multi-line trend, 100%-stacked, diverging bar)
# ---------------------------------------------------------------------------

def multi_line_chart(df, x: str, y_cols: list, names: list = None) -> go.Figure:
    """
    Multi-series line chart (e.g. Male / Female / Total enrolment trend).
    Fixed: same category-axis treatment as dual_line_chart, plus markers
    and per-point value labels so it's no longer a bare flat line.
    """
    if df.empty:
        return _base_layout(go.Figure())
 
    names = names or y_cols
    x_vals = df[x].astype(str).tolist()
 
    fig = go.Figure()
    for i, col in enumerate(y_cols):
        color = CHART_SEQUENCE[i % len(CHART_SEQUENCE)]
        fig.add_trace(go.Scatter(
            x=x_vals, y=df[col], mode="lines+markers+text", name=names[i],
            line=dict(color=color, width=2.5), marker=dict(size=6),
            text=df[col].astype(int).astype(str),
            textposition="top center" if i % 2 == 0 else "bottom center",
            textfont=dict(size=9, color=color),
            hovertemplate=f"{names[i]}: %{{y:,.0f}}<extra></extra>",
        ))
 
    fig = _base_layout(fig, show_legend=True)
    fig.update_layout(
        hovermode="x unified",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5),
        margin=dict(l=10, r=15, t=25, b=15),
    )
    fig.update_xaxes(
        title=None,
        type="category",
        categoryorder="array",
        categoryarray=x_vals,
    )
    fig.update_yaxes(title=None)
    return fig

def stacked_bar_100(df: pd.DataFrame, category: str, value: str, group: str) -> go.Figure:
    """
    100%-stacked horizontal bar — e.g. Male vs Female % per province, or
    Public vs Private % per year. Expects a long-format df with one row
    per (category, group) pair and a numeric value column.
    """
    if df.empty:
        return _base_layout(go.Figure())

    pivot = df.pivot_table(index=category, columns=group, values=value, aggfunc="sum").fillna(0)
    pivot_pct = pivot.div(pivot.sum(axis=1), axis=0) * 100

    fig = go.Figure()
    for i, col in enumerate(pivot_pct.columns):
        color = CHART_SEQUENCE[i % len(CHART_SEQUENCE)]
        fig.add_trace(go.Bar(
            y=pivot_pct.index,
            x=pivot_pct[col],
            name=str(col),
            orientation="h",
            marker_color=color,
            text=pivot_pct[col].apply(lambda v: f"{v:.1f}%"),
            textposition="inside",
            hovertemplate=f"{col}: %{{x:.1f}}%<extra></extra>",
        ))

    fig = _base_layout(fig, show_legend=True)
    fig.update_layout(
        barmode="stack",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5),
    )
    fig.update_xaxes(title=None, range=[0, 100])
    fig.update_yaxes(title=None)
    return fig


def _short_number(v: float) -> str:
    """Compact number formatting for chart labels, e.g. 1051904 -> '1.05M'."""
    v = float(v)
    if abs(v) >= 1_000_000:
        return f"{v / 1_000_000:.2f}M"
    if abs(v) >= 1_000:
        return f"{v / 1_000:.1f}K"
    return f"{v:,.0f}"


def grouped_bar_trend_chart(df: pd.DataFrame, x: str, bar_cols: list, bar_names: list = None,
                             trend_col: str = None, trend_name: str = None,
                             trend_color: str = "rgba(214, 69, 65, 1)",
                             trend_fill_color: str = "rgba(214, 69, 65, 0.15)") -> go.Figure:
    """
    Grouped bar chart with an optional shaded trend line overlaid on top —
    e.g. Male/Female bars per year, with a Total trend area drawn over them
    (matches the reference combo-chart style: bars + soft-shaded area line).
    """
    if df.empty:
        return _base_layout(go.Figure())

    bar_names = bar_names or bar_cols
    fig = go.Figure()

    for i, col in enumerate(bar_cols):
        color = CHART_SEQUENCE[i % len(CHART_SEQUENCE)]
        fig.add_trace(go.Bar(
            x=df[x], y=df[col], name=bar_names[i],
            marker_color=color,
            text=df[col].apply(_short_number),
            textposition="outside",
            textfont=dict(size=10),
            cliponaxis=False,
            hovertemplate=f"{bar_names[i]}: %{{y:,.0f}}<extra></extra>",
        ))

    if trend_col is not None:
        fig.add_trace(go.Scatter(
            x=df[x], y=df[trend_col], name=trend_name or trend_col,
            mode="lines+markers", line=dict(color=trend_color, width=2), marker=dict(size=5),
            fill="tozeroy", fillcolor=trend_fill_color,
            hovertemplate=f"{trend_name or trend_col}: %{{y:,.0f}}<extra></extra>",
        ))

    fig = _base_layout(fig, show_legend=True)
    fig.update_layout(
        barmode="group",
        bargap=0.28,
        bargroupgap=0.10,
        margin=dict(l=10, r=15, t=40, b=15),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5),
    )
    fig.update_xaxes(title=None)
    fig.update_yaxes(title=None, rangemode="tozero")
    return fig


def diverging_bar_chart(df: pd.DataFrame, category: str, left_col: str, right_col: str,
                         left_name: str = "Male", right_name: str = "Female",
                         preserve_order: bool = False) -> go.Figure:
    """
    Diverging (butterfly) bar chart — e.g. Male (left, negative) vs Female
    (right, positive) enrollment per province/region, or per year. Expects
    one row per category with separate left/right numeric columns.

    preserve_order: if True, keeps the df's existing row order (e.g. a
    chronological year trend) instead of sorting by right_col's value —
    use this for time-series categories like Year.
    """
    if df.empty:
        return _base_layout(go.Figure())

    if preserve_order:
        plot_df = df.copy()
        # Plotly renders horizontal bars bottom-to-top, so reverse to keep
        # the earliest category (e.g. earliest year) at the top.
        plot_df = plot_df.iloc[::-1].reset_index(drop=True)
    else:
        plot_df = df.sort_values(by=right_col, ascending=True).copy()
    plot_df["_row_total"] = plot_df[left_col] + plot_df[right_col]
    plot_df["_left_pct"] = (plot_df[left_col] / plot_df["_row_total"].replace(0, 1)) * 100
    plot_df["_right_pct"] = (plot_df[right_col] / plot_df["_row_total"].replace(0, 1)) * 100

    fig = go.Figure()
    fig.add_trace(go.Bar(
        y=plot_df[category],
        x=-plot_df[left_col],
        name=left_name,
        orientation="h",
        marker_color=COLORS["primary"],
        text=[f"{v:,.0f} ({p:.1f}%)" for v, p in zip(plot_df[left_col], plot_df["_left_pct"])],
        textposition="outside",
        hovertemplate=f"<b>%{{y}}</b><br>{left_name}: %{{customdata:,.0f}}<extra></extra>",
        customdata=plot_df[left_col],
    ))
    fig.add_trace(go.Bar(
        y=plot_df[category],
        x=plot_df[right_col],
        name=right_name,
        orientation="h",
        marker_color=COLORS["accent"],
        text=[f"{v:,.0f} ({p:.1f}%)" for v, p in zip(plot_df[right_col], plot_df["_right_pct"])],
        textposition="outside",
        hovertemplate=f"<b>%{{y}}</b><br>{right_name}: %{{x:,.0f}}<extra></extra>",
    ))

    max_val = max(plot_df[left_col].max(), plot_df[right_col].max()) if not plot_df.empty else 100
    fig = _base_layout(fig, show_legend=True)
    fig.update_layout(
        barmode="relative",
        bargap=0.25,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5),
        margin=dict(l=10, r=25, t=25, b=15),
    )
    fig.update_xaxes(
        title=None,
        range=[-max_val * 1.35, max_val * 1.35],
        tickvals=[-max_val, -max_val / 2, 0, max_val / 2, max_val],
        ticktext=[f"{max_val:,.0f}", f"{max_val/2:,.0f}", "0", f"{max_val/2:,.0f}", f"{max_val:,.0f}"],
    )
    fig.update_yaxes(title=None)
    return fig