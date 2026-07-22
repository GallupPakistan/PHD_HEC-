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

    # Sort & pick top N
    plot_df = df.dropna(subset=[x, y]).sort_values(by=x, ascending=False).head(top_n).copy()

    total_val = plot_df[x].sum() if plot_df[x].sum() > 0 else 1
    plot_df["pct"] = (plot_df[x] / total_val) * 100
    plot_df["display_text"] = plot_df.apply(lambda r: f" {r[x]:,.0f} ({r['pct']:.1f}%)", axis=1)

    # Sort ascending for horizontal bar rendering order
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
        # Clean custom tooltip
        hovertemplate="<b>%{y}</b><br>Count: %{x:,.0f}<extra></extra>",
    )

    fig = _base_layout(fig)

    # Auto-expand X-axis range by 30% so outside labels NEVER clip/cut off
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


def treemap_chart(df: pd.DataFrame, path: str, values: str, top_n: int = 12) -> go.Figure:
    """
    Clean Responsive Treemap:
    - Wraps text gracefully and scales according to space.
    """
    plot_df = df.dropna(subset=[path, values]).copy()
    plot_df = plot_df[plot_df[values] > 0].head(top_n)

    if plot_df.empty:
        return _base_layout(go.Figure())

    plot_df["formatted_label"] = plot_df[path].astype(str).str.replace(", ", "<br>").str.replace(" - ", "<br>")

    fig = px.treemap(
        plot_df,
        path=[px.Constant("Total"), "formatted_label"],
        values=values,
        color=values,
        color_continuous_scale=[COLORS.get("card", "#2C3E50"), COLORS["primary"]],
    )

    fig.update_traces(
        textinfo="label+value+percent entry",
        texttemplate="<b>%{label}</b><br>%{value:,.0f} (%{percentEntry:.1%})",
        hovertemplate="<b>%{label}</b><br>Value: %{value:,.0f}<br>Share: %{percentParent:.1%}<extra></extra>",
        marker_line_width=1.5,
        marker_line_color=COLORS.get("border", "#FFFFFF"),
        textfont=dict(family=FONT_FAMILY),
        tiling=dict(pad=2),
    )

    fig = _base_layout(fig)
    fig.update_layout(
        coloraxis_showscale=False,
        margin=dict(l=5, r=5, t=5, b=5),
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


def lollipop_chart(df: pd.DataFrame, x: str, y: str, top_n: int = 10) -> go.Figure:
    plot_df = df.head(top_n).sort_values(x)
    fig = go.Figure()

    for _, row in plot_df.iterrows():
        fig.add_shape(
            type="line",
            x0=0, x1=row[x], y0=row[y], y1=row[y],
            line=dict(color=COLORS["border"], width=2),
        )

    fig.add_trace(
        go.Scatter(
            x=plot_df[x], y=plot_df[y], mode="markers",
            marker=dict(size=10, color=COLORS["primary"]),
            hovertemplate="%{y}: <b>%{x:,.0f}</b><extra></extra>",
        )
    )

    fig = _base_layout(fig)
    fig.update_layout(showlegend=False)
    fig.update_xaxes(title=None)
    fig.update_yaxes(title=None)
    return fig