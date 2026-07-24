"""
geo.py
City-level coordinates for Pakistani cities appearing in HEIS_Data.xlsx,
and a loader that attaches latitude/longitude to each university record
so it can be plotted on a map.

Coordinates are approximate city-center points (not exact campus
addresses) — sufficient for a "main campus location" overview map.
"""

from pathlib import Path
import pandas as pd
import streamlit as st

HEIS_PATH = Path(__file__).resolve().parent.parent / "data" / "HEIS_Data.xlsx"

# Approximate city-center coordinates (lat, lon) for every city present
# in the HEIS dataset.
CITY_COORDS = {
    "Abbottabad": (34.1688, 73.2215),
    "Bagh": (33.9836, 73.7738),
    "Bahawalpur": (29.3956, 71.6722),
    "Bannu": (32.9880, 70.6028),
    "Bhera": (32.4833, 72.9000),
    "Bhimber": (32.9750, 74.0806),
    "Bhitshah, Sindh": (25.7981, 68.5253),
    "Chakdara": (34.6825, 71.9139),
    "Chakwal": (32.9328, 72.8630),
    "Charsadda": (34.1483, 71.7419),
    "Chitral": (35.8511, 71.7861),
    "Daggar": (34.5167, 72.4333),
    "Dera Ghazi Khan": (30.0561, 70.6350),
    "Dera Ismail Khan": (31.8300, 70.9019),
    "Faisalabad": (31.4180, 73.0791),
    "Gambat": (27.3667, 68.5167),
    "Gilgit": (35.9208, 74.3144),
    "Gujranwala": (32.1877, 74.1945),
    "Gujrat": (32.5740, 74.0789),
    "Gwadar": (25.1264, 62.3225),
    "Haripur": (33.9958, 72.9375),
    "Hyderabad": (25.3960, 68.3578),
    "Islamabad": (33.6844, 73.0479),
    "Jamshoro": (25.4300, 68.2775),
    "Jhang": (31.2781, 72.3317),
    "Karachi": (24.8607, 67.0011),
    "Karak": (33.1167, 71.0961),
    "Khairpur": (27.5295, 68.7590),
    "Khairpur Mirs": (27.5295, 68.7590),
    "Khuzdar": (27.8000, 66.6167),
    "Kohat": (33.5836, 71.4411),
    "Kotli": (33.5169, 73.9036),
    "Lahore": (31.5497, 74.3436),
    "Lakki Marwat": (32.6060, 70.9114),
    "Larkana": (27.5590, 68.2120),
    "Lasbela": (25.8828, 66.7178),
    "Loralai": (30.3705, 68.5994),
    "Mansehra": (34.3336, 73.1969),
    "Mardan": (34.1986, 72.0404),
    "Mianwali": (32.5850, 71.5420),
    "Mianwali District": (32.5850, 71.5420),
    "Mirpur (AJK)": (33.1483, 73.7517),
    "Multan": (30.1575, 71.5249),
    "Murree": (33.9070, 73.3943),
    "Muzaffarabad": (34.3700, 73.4711),
    "Narowal": (32.1014, 74.8758),
    "Nawabshah": (26.2442, 68.4100),
    "Nerian Sharif (AJK)": (34.0000, 73.8000),
    "Nowshera": (34.0150, 71.9747),
    "Okara": (30.8100, 73.4467),
    "Peshawar": (34.0151, 71.5249),
    "Quetta": (30.1798, 66.9750),
    "Rahim Yar Khan": (28.4202, 70.2952),
    "Rasul-Mandi Bahauddin": (32.5850, 73.5000),
    "Rawalakot": (33.8580, 73.7658),
    "Rawalpindi": (33.5651, 73.0169),
    "Sahiwal": (30.6650, 73.1100),
    "Sakrand": (26.1389, 68.2761),
    "Sargodha": (32.0836, 72.6711),
    "Shaheed Benazirabad": (26.2442, 68.4100),
    "Shikarpur": (27.9560, 68.6382),
    "Sialkot": (32.4927, 74.5310),
    "Sibi Balochistan": (29.5430, 67.8773),
    "Skardu": (35.2971, 75.6333),
    "Sukkur": (27.7052, 68.8574),
    "Swabi": (34.1200, 72.4700),
    "Swat": (35.2227, 72.4258),
    "Tando Muhammad Khan": (25.1234, 68.5372),
    "Tandojam": (25.4262, 68.5342),
    "Taxila": (33.7460, 72.7972),
    "Topi": (34.0700, 72.6300),
    "Turbat": (26.0031, 63.0526),
    "Wah": (33.7717, 72.7458),
}


@st.cache_data(show_spinner=False)
def load_heis_locations() -> pd.DataFrame:
    """Loads the HEIS institution list and attaches lat/lon per city.

    Multiple universities in the same city are given a small deterministic
    jitter so their markers don't sit exactly on top of one another.
    Returns an empty DataFrame (not an error) if the source file is
    missing, so the calling page can show a friendly message instead of
    crashing.
    """
    if not HEIS_PATH.exists():
        return pd.DataFrame(columns=["University", "Province", "City", "Sector", "Latitude", "Longitude"])

    df = pd.read_excel(HEIS_PATH, sheet_name="Sheet1")
    df = df.rename(columns={"Name of University": "University"})
    df = df[["University", "Province", "City", "Sector"]].dropna(subset=["City"])
    df["City"] = df["City"].astype(str).str.strip()

    df["Latitude"] = df["City"].map(lambda c: CITY_COORDS.get(c, (None, None))[0])
    df["Longitude"] = df["City"].map(lambda c: CITY_COORDS.get(c, (None, None))[1])
    df = df.dropna(subset=["Latitude", "Longitude"]).reset_index(drop=True)

    # Deterministic small jitter (based on row position within each city)
    # so co-located universities fan out slightly instead of overlapping.
    df["_rank_in_city"] = df.groupby("City").cumcount()
    jitter = 0.045
    df["Latitude"] = df["Latitude"] + (df["_rank_in_city"] % 5) * jitter * ((df["_rank_in_city"] % 2) * 2 - 1)
    df["Longitude"] = df["Longitude"] + (df["_rank_in_city"] // 5 % 5) * jitter * ((df["_rank_in_city"] % 3 == 0) * 2 - 1)
    df.drop(columns=["_rank_in_city"], inplace=True)

    return df


@st.cache_data(show_spinner=False)
def load_heis_city_summary() -> pd.DataFrame:
    """Aggregates universities by City + Sector, with a count column used
    to size map bubbles — matching the reference dashboard's style where
    bubble size reflects how many institutions sit in that city, instead
    of one dot per university."""

    df = load_heis_locations()
    if df.empty:
        return pd.DataFrame(columns=["City", "Sector", "Province", "Latitude", "Longitude", "Count"])

    # Use the un-jittered city center for aggregation (jitter is only
    # useful for the per-university view).
    summary = (
        df.assign(
            Latitude=df["City"].map(lambda c: CITY_COORDS.get(c, (None, None))[0]),
            Longitude=df["City"].map(lambda c: CITY_COORDS.get(c, (None, None))[1]),
        )
        .groupby(["City", "Sector"], as_index=False)
        .agg(Province=("Province", "first"), Latitude=("Latitude", "first"),
             Longitude=("Longitude", "first"), Count=("University", "count"))
    )

    # When both Public and Private exist in the same city, they share the
    # exact same city-center coordinate, so the larger bubble fully hides
    # the smaller one. Nudge each sector a small, fixed distance apart
    # (Public up-left, Private down-right) so both stay visible while
    # remaining visually anchored to the same city.
    sector_offset = {"Public": (0.09, -0.09), "Private": (-0.09, 0.09)}
    summary["Latitude"] = summary.apply(
        lambda r: r["Latitude"] + sector_offset.get(r["Sector"], (0, 0))[0], axis=1
    )
    summary["Longitude"] = summary.apply(
        lambda r: r["Longitude"] + sector_offset.get(r["Sector"], (0, 0))[1], axis=1
    )

    return summary