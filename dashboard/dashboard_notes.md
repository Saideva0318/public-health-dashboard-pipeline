# Power BI Dashboard Guide - Public Health Dashboard Pipeline

## Overview

This file documents the Power BI dashboard layout, KPI cards, visuals, and PostgreSQL connection setup for the CDC Public Health Surveillance Dashboard.

---

## PostgreSQL Connection Setup

1. Open Power BI Desktop
2. Click **Get Data** > **PostgreSQL database**
3. Enter:
   - Server: `localhost` (or your server IP)
   - Database: `public_health_db`
4. Select **DirectQuery** mode for live data
5. Load the following views:
   - `vw_curated_health_cases`
   - `vw_weekly_trend`
   - `vw_state_summary`
   - `vw_top_diseases`
   - `vw_data_quality`

---

## Dashboard Layout

### Page 1: Executive Summary

| Visual | Type | Data Source | Notes |
|---|---|---|---|
| Total YTD Cases | KPI Card | `vw_curated_health_cases` | SUM of `ytd_cases_current` |
| YoY Change % | KPI Card | `vw_curated_health_cases` | AVG of `yoy_pct_change` |
| States Reporting | KPI Card | `vw_state_summary` | COUNT DISTINCT of `state` |
| Data Completeness | KPI Card | `vw_data_quality` | AVG of `completeness_pct` |
| Weekly Trend | Line Chart | `vw_weekly_trend` | X: `mmwr_week`, Y: `total_weekly_cases`, Legend: `disease` |
| Top 10 Diseases | Bar Chart | `vw_top_diseases` | Y: `disease`, X: `total_ytd_cases_2024` |

### Page 2: Geographic Breakdown

| Visual | Type | Data Source | Notes |
|---|---|---|---|
| Cases by State | Filled Map | `vw_state_summary` | Color: `total_ytd_cases`, Location: `state` |
| State Table | Table | `vw_state_summary` | Columns: state, total_ytd_cases, disease_count, completeness |
| State Slicer | Slicer | `vw_state_summary` | Filter all visuals by state |

### Page 3: Disease Analysis

| Visual | Type | Data Source | Notes |
|---|---|---|---|
| YoY Comparison | Clustered Bar | `vw_top_diseases` | 2024 vs 2023 YTD side-by-side |
| Disease Trend | Line Chart | `vw_weekly_trend` | Weekly trend by selected disease |
| Disease Slicer | Dropdown | `vw_top_diseases` | Filter by disease name |

### Page 4: Data Quality

| Visual | Type | Data Source | Notes |
|---|---|---|---|
| Completeness Over Time | Line Chart | `vw_data_quality` | X: `mmwr_week`, Y: `completeness_pct` |
| Missing Records | Table | `vw_data_quality` | Columns: year, week, total_records, missing counts |
| Completeness Gauge | Gauge | `vw_data_quality` | Target: 95% completeness |

---

## KPI Definitions

| KPI | Formula | Target |
|---|---|---|
| Total YTD Cases | SUM(ytd_cases_current) | N/A - tracking metric |
| YoY Change | AVG(yoy_pct_change) | Trending indicator |
| Data Completeness | AVG(completeness_pct) | >= 95% |
| States Reporting | COUNT DISTINCT(state) | All 50 states + DC |

---

## Dashboard Screenshot Placeholders

> Add screenshots of your Power BI dashboard here after building it.
> Recommended: Export as PNG and save to `dashboard/screenshots/` folder.

- `dashboard/screenshots/page1_executive_summary.png`
- `dashboard/screenshots/page2_geographic.png`
- `dashboard/screenshots/page3_disease_analysis.png`
- `dashboard/screenshots/page4_data_quality.png`
