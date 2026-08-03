"""
loader.py
Loads and lightly cleans the Dashboard_Data.xlsx, HEIS Data.xlsx, and
master_dataset.xlsx workbooks. All I/O and caching lives here so the
rest of the app never touches pandas.read_excel directly.
"""

from pathlib import Path
from datetime import datetime
import pandas as pd
import streamlit as st

DATA_PATH = Path(__file__).resolve().parent.parent / "data" / "Dashboard_Data.xlsx"
HEIS_PATH = Path(__file__).resolve().parent.parent / "data" / "HEIS_Data.xlsx"
MASTER_PATH = Path(__file__).resolve().parent.parent / "data" / "enrollment_data(claude).xlsx"

MASTER_SHEETS = {
    "enrolment_summary": "enrolment_summary",
    "enrolment_by_level_gender": "enrolment_by_level_gender",
    "enrolment_by_sector": "enrolment_by_sector",
    "enrolment_by_discipline": "enrolment_by_discipline",
    "enrolment_by_province_gender": "enrolment_by_province_gender",
    "phds_produced": "phds_produced",
    "data_quality_notes": "data_quality_notes",
}


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
def _load_master_data_cached(mtime: float) -> dict:
    data = {}
    for key, sheet in MASTER_SHEETS.items():
        try:
            data[key] = pd.read_excel(MASTER_PATH, sheet_name=sheet)
        except (ValueError, FileNotFoundError):
            data[key] = pd.DataFrame()
    return data


def load_master_data() -> dict:
    """
    Loads every sheet from enrollment_data(claude).xlsx (the consolidated
    HEC annual report extraction — enrolment, sector, province+gender,
    PhDs, etc.) into a dict of DataFrames keyed by sheet name. Cache key
    includes the file's modified time, so editing the Excel file always
    produces fresh data on the next rerun instead of serving a stale
    cached copy until the app process is restarted.
    """
    mtime = MASTER_PATH.stat().st_mtime if MASTER_PATH.exists() else 0
    return _load_master_data_cached(mtime)


@st.cache_data(show_spinner=False)
def get_master_years(master_data: dict) -> list:
    """Sorted list of all years present across the master dataset's sheets."""
    years = set()
    for key in ("enrolment_summary", "enrolment_by_level_gender",
                "enrolment_by_sector", "enrolment_by_province_gender"):
        df = master_data.get(key)
        if df is not None and "year" in df.columns:
            years.update(df["year"].dropna().unique().tolist())
    return sorted(years)


@st.cache_data(show_spinner=False)
def get_master_provinces(master_data: dict) -> list:
    """Sorted list of all provinces present in enrolment_by_province_gender."""
    df = master_data.get("enrolment_by_province_gender")
    if df is None or "province" not in df.columns:
        return []
    return sorted(df["province"].dropna().unique().tolist())


# Backward-compatible aliases (in case any file still imports the older names)
get_available_years = get_master_years
get_available_provinces = get_master_provinces


def filter_master_df(df: pd.DataFrame, filters: dict) -> pd.DataFrame:
    """
    Applies the active cross-filter selection (from components/filters.py)
    to any master_dataset sheet. Columns not present in df are ignored,
    so this is safe to call on any sheet regardless of which columns it has.
    """
    out = df.copy()
    if filters.get("years") and "year" in out.columns:
        out = out[out["year"].isin(filters["years"])]
    if filters.get("provinces") and "province" in out.columns:
        out = out[out["province"].isin(filters["provinces"])]
    if filters.get("genders") and "gender" in out.columns:
        out = out[out["gender"].isin(filters["genders"])]
    if filters.get("sectors") and "sector" in out.columns:
        out = out[out["sector"].isin(filters["sectors"])]
    return out


REGION_GENDER_CSV_PATH = Path(__file__).resolve().parent.parent / "data" / "Region&gender wise enrollment.csv"


@st.cache_data(show_spinner=False)
def _load_region_gender_enrollment_cached(mtime: float) -> pd.DataFrame:
    df = pd.read_csv(REGION_GENDER_CSV_PATH)
    df.columns = [c.strip() for c in df.columns]
    df["Year"] = df["Year"].astype(str).str.strip()
    df["Province"] = df["Province"].astype(str).str.strip()
    df["Sector"] = df["Sector"].astype(str).str.strip()
    for col in ("Male", "Female", "Total"):
        df[col] = df[col].astype(str).str.replace(",", "", regex=False).str.strip()
        df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)
    return df


def load_region_gender_enrollment() -> pd.DataFrame:
    """
    Loads 'Region&gender wise enrollment.csv' — columns: Year, Province,
    Sector, Male, Female, Total. Cache key includes the file's modified
    time, so editing the CSV always produces fresh data on the next rerun
    (a plain @st.cache_data on the read would otherwise keep serving the
    first-ever version of the file until the app process is restarted).
    """
    if not REGION_GENDER_CSV_PATH.exists():
        return pd.DataFrame()
    mtime = REGION_GENDER_CSV_PATH.stat().st_mtime
    return _load_region_gender_enrollment_cached(mtime)


@st.cache_data(show_spinner=False)
def get_last_updated() -> str:
    """Returns a human readable last-modified timestamp for the data file."""
    try:
        ts = DATA_PATH.stat().st_mtime
        return datetime.fromtimestamp(ts).strftime("%d %b %Y, %H:%M")
    except FileNotFoundError:
        return "Unknown"