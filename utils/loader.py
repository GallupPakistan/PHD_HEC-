"""
loader.py
Loads and lightly cleans the Dashboard_Data.xlsx workbook.
All I/O and caching lives here so the rest of the app never touches
pandas.read_excel directly.
"""

from pathlib import Path
from datetime import datetime
import pandas as pd
import streamlit as st

DATA_PATH = Path(__file__).resolve().parent.parent / "data" / "Dashboard_Data.xlsx"


@st.cache_data(show_spinner=False)
def load_workbook() -> dict:
    """Loads all four sheets from Dashboard_Data.xlsx and returns a dict of
    cleaned DataFrames keyed by sheet name."""

    university = pd.read_excel(DATA_PATH, sheet_name="University")
    discipline = pd.read_excel(DATA_PATH, sheet_name="Discipline")
    subject = pd.read_excel(DATA_PATH, sheet_name="Subject")
    year = pd.read_excel(DATA_PATH, sheet_name="Year")

    university.columns = ["University", "Records"]
    discipline.columns = ["Discipline", "Records"]
    subject.columns = ["Subject", "Records"]
    year.columns = ["Year", "Records"]

    for df in (university, discipline, subject, year):
        df.dropna(subset=[df.columns[0]], inplace=True)
        df["Records"] = pd.to_numeric(df["Records"], errors="coerce").fillna(0).astype(int)

    university["University"] = university["University"].astype(str).str.strip()
    discipline["Discipline"] = discipline["Discipline"].astype(str).str.strip()
    subject["Subject"] = subject["Subject"].astype(str).str.strip()
    year["Year"] = pd.to_numeric(year["Year"], errors="coerce")
    year.dropna(subset=["Year"], inplace=True)
    year["Year"] = year["Year"].astype(int)
    year.sort_values("Year", inplace=True)

    university = university.groupby("University", as_index=False)["Records"].sum()
    university.sort_values("Records", ascending=False, inplace=True, ignore_index=True)

    discipline = discipline.groupby("Discipline", as_index=False)["Records"].sum()
    discipline.sort_values("Records", ascending=False, inplace=True, ignore_index=True)

    subject = subject.groupby("Subject", as_index=False)["Records"].sum()
    subject.sort_values("Records", ascending=False, inplace=True, ignore_index=True)

    return {
        "university": university,
        "discipline": discipline,
        "subject": subject,
        "year": year,
    }


@st.cache_data(show_spinner=False)
def get_last_updated() -> str:
    """Returns a human readable last-modified timestamp for the data file."""
    try:
        ts = DATA_PATH.stat().st_mtime
        return datetime.fromtimestamp(ts).strftime("%d %b %Y, %H:%M")
    except FileNotFoundError:
        return "Unknown"
