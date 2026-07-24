"""
loader.py
Loads and lightly cleans the Dashboard_Data.xlsx and HEIS Data.xlsx workbooks.
All I/O and caching lives here so the rest of the app never touches
pandas.read_excel directly.
"""

from pathlib import Path
from datetime import datetime
import pandas as pd
import streamlit as st

DATA_PATH = Path(__file__).resolve().parent.parent / "data" / "Dashboard_Data.xlsx"
HEIS_PATH = Path(__file__).resolve().parent.parent / "data" / "HEIS_Data.xlsx"


@st.cache_data(show_spinner=False)
def load_heis() -> pd.DataFrame:
    """Loads HEIS Data.xlsx — the university directory (Province/City/Sector)."""
    df = pd.read_excel(HEIS_PATH, sheet_name="Sheet1")
    df.columns = [c.strip() for c in df.columns]
    df["Province"] = df["Province"].astype(str).str.strip()
    df["City"] = df["City"].astype(str).str.strip()
    df["Sector"] = df["Sector"].astype(str).str.strip()
    df["Name of University"] = df["Name of University"].astype(str).str.strip()
    return df

@st.cache_data(show_spinner=False)
def load_heis_growth() -> pd.DataFrame:
    """Loads the HEI growth-over-years data from HEIS_Data.xlsx Sheet2.
    Header row is the 3rd row in the sheet (title + blank row above it)."""
    df = pd.read_excel(HEIS_PATH, sheet_name="Sheet2", skiprows=2)
    df.columns = ["Year", "Total", "New"]
    df = df.dropna(subset=["Year"])
    df["Year"] = pd.to_numeric(df["Year"], errors="coerce")
    df.dropna(subset=["Year"], inplace=True)
    df["Year"] = df["Year"].astype(int)
    df["Total"] = pd.to_numeric(df["Total"], errors="coerce").fillna(0).astype(int)
    df["New"] = pd.to_numeric(df["New"], errors="coerce").fillna(0).astype(int)
    df = df.sort_values("Year").reset_index(drop=True)
    return df

@st.cache_data(show_spinner=False)
def load_province_sector() -> pd.DataFrame:
    """Loads the pre-aggregated Province & Sector-wise HEIs table from
    HEIS_Data.xlsx Sheet4 (the authoritative 278-total table), instead of
    recomputing from Sheet1 which only contains a partial (247-row) list."""
    df = pd.read_excel(HEIS_PATH, sheet_name="Sheet4", skiprows=2)
    df.columns = ["Province", "Private", "Public", "Total"]
    df = df.dropna(subset=["Province"])
    # Drop the summary "TOTAL (PAKISTAN)" row if present — the app computes
    # its own total from the KPI/table logic instead.
    df = df[~df["Province"].astype(str).str.contains("TOTAL", case=False, na=False)]
    df["Private"] = pd.to_numeric(df["Private"], errors="coerce").fillna(0).astype(int)
    df["Public"] = pd.to_numeric(df["Public"], errors="coerce").fillna(0).astype(int)
    df["Total"] = pd.to_numeric(df["Total"], errors="coerce").fillna(0).astype(int)
    df = df.sort_values("Total", ascending=False).reset_index(drop=True)
    return df
@st.cache_data(show_spinner=False)
def load_province_sector() -> pd.DataFrame:
    """Loads the pre-aggregated Province & Sector-wise HEIs table from
    HEIS_Data.xlsx Sheet4 (the authoritative 278-total table)."""
    df = pd.read_excel(HEIS_PATH, sheet_name="Sheet4", skiprows=2)
    df.columns = ["Province", "Private", "Public", "Total"]
    df = df.dropna(subset=["Province"])
    df = df[~df["Province"].astype(str).str.contains("TOTAL", case=False, na=False)]
    df["Private"] = pd.to_numeric(df["Private"], errors="coerce").fillna(0).astype(int)
    df["Public"] = pd.to_numeric(df["Public"], errors="coerce").fillna(0).astype(int)
    df["Total"] = pd.to_numeric(df["Total"], errors="coerce").fillna(0).astype(int)
    df = df.sort_values("Total", ascending=False).reset_index(drop=True)
    return df

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
        "heis": load_heis(),
        "heis_growth": load_heis_growth(),
        "province_sector": load_province_sector(),
    }

@st.cache_data(show_spinner=False)
def get_last_updated() -> str:
    """Returns a human readable last-modified timestamp for the data file."""
    try:
        ts = DATA_PATH.stat().st_mtime
        return datetime.fromtimestamp(ts).strftime("%d %b %Y, %H:%M")
    except FileNotFoundError:
        return "Unknown"