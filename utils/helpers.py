"""
helpers.py
Small, reusable, pure functions used across pages: number formatting,
insight generation, and common statistics.
"""

import pandas as pd


def format_number(value: float) -> str:
    """Formats a number with thousands separators, no decimals."""
    try:
        return f"{int(round(value)):,}"
    except (ValueError, TypeError):
        return str(value)


def compute_overview_insights(data: dict) -> dict:
    """Builds the set of quick insights shown on the Overview page."""
    university = data["university"]
    discipline = data["discipline"]
    subject = data["subject"]
    year = data["year"]

    top_university = university.iloc[0]
    top_discipline = discipline.iloc[0]
    top_subject = subject.iloc[0]
    peak_year_row = year.loc[year["Records"].idxmax()]

    avg_records = university["Records"].mean()

    return {
        "Highest University": f"{top_university['University']} ({format_number(top_university['Records'])})",
        "Highest Discipline": f"{top_discipline['Discipline']} ({format_number(top_discipline['Records'])})",
        "Most Common Subject": f"{top_subject['Subject']} ({format_number(top_subject['Records'])})",
        "Peak Year": f"{int(peak_year_row['Year'])} ({format_number(peak_year_row['Records'])})",
        "Average Records / University": format_number(avg_records),
    }


def compute_pareto(df: pd.DataFrame, value_col: str) -> pd.DataFrame:
    """Adds cumulative percentage columns for a Pareto chart."""
    out = df.sort_values(value_col, ascending=False).reset_index(drop=True).copy()
    total = out[value_col].sum()
    out["Cumulative"] = out[value_col].cumsum()
    out["CumulativePct"] = (out["Cumulative"] / total * 100).round(1)
    return out


def paginate_dataframe(df: pd.DataFrame, page: int, page_size: int) -> pd.DataFrame:
    """Returns a single page slice of a DataFrame."""
    start = page * page_size
    end = start + page_size
    return df.iloc[start:end]
