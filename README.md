# HEC Analytics Dashboard

An enterprise-grade Streamlit analytics dashboard for HEC PhD records data,
styled to resemble a Government / HEC / Power BI reporting product rather
than a default Streamlit demo.

## Getting Started

```bash
pip install -r requirements.txt
streamlit run app.py
```

Place your workbook at `data/Dashboard_Data.xlsx` with sheets named
`University`, `Discipline`, `Subject`, and `Year`, each with two columns:
a name/label column and a `Numbers` (record count) column. A sample file
is already included.

## Project Structure

```
app.py                  Entry point — wires sidebar, styling, and pages
components/
    sidebar.py          Left navigation: logo, nav buttons, footer
    cards.py            Page headers, section cards, insights panel
    charts.py           Plotly chart factories (bar, donut, line, treemap...)
    tables.py           AgGrid-powered searchable/sortable/exportable tables
    kpis.py             KPI card row renderer
app_pages/
    overview.py         Landing page — KPIs, top charts, quick insights
    universities.py     University-level detail page
    disciplines.py      Discipline-level detail page
    subjects.py         Subject-level detail page (no pie — 700+ categories)
    years.py            Year-level trend page
    analytics.py        Cross-cutting rankings & trend/distribution view
    explorer.py         Raw dataset explorer with CSV/Excel export
    about.py            Dashboard & dataset metadata
utils/
    loader.py           Cached Excel loading & cleaning
    styles.py           Color palette + global CSS injection
    helpers.py          Formatting, insights, Pareto/pagination helpers
data/
    Dashboard_Data.xlsx Source workbook
```

> **Note:** the pages folder is named `app_pages/` rather than `pages/`.
> Streamlit auto-generates its own sidebar navigation for any folder
> literally named `pages/` next to `app.py`, which would conflict with
> the custom sidebar built here. Renaming it avoids that collision while
> keeping the same modular structure requested.

## Design System

| Token | Value |
|---|---|
| Primary | `#0B3A75` |
| Secondary | `#4F6D8A` |
| Accent | `#58C4B5` |
| Background | `#F5F7FA` |
| Card | `#FFFFFF` |
| Border | `#E4E8ED` |
| Text | `#243447` |
| Muted Text | `#6B7280` |
| Success | `#2E8B57` |

All charts share one Plotly layout function (`components/charts.py`) so
margins, fonts, heights, and colors stay consistent across every page.
Toolbars are disabled and backgrounds are transparent throughout.

## Technology Stack

- **Streamlit** — application framework
- **Plotly** — all charting (bar, donut, line, area, column, treemap,
  Pareto, lollipop)
- **streamlit-aggrid** — professional tables (search, sort, filter,
  column resize/hide, pagination, sticky header, CSV/Excel export)
- **pandas / openpyxl** — data loading and cleaning, cached with
  `st.cache_data`

## Notes

- If `streamlit-aggrid` is not installed, tables gracefully fall back to
  a styled `st.dataframe` with a text-based search box so the app never
  breaks — but installing it is recommended for the full experience
  described in the spec (column resize/hide, sidebar filters, sticky
  header).
- Subjects has ~740 categories, so per the spec no pie/donut chart is
  used there — only ranked bar, treemap, and lollipop views.
