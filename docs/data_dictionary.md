# Data Dictionary - Public Health Dashboard Pipeline

## Table: `raw_cdc_cases`

| Column | Type | Description |
|---|---|---|
| `id` | SERIAL | Auto-increment primary key |
| `reporting_area` | VARCHAR(100) | U.S. state or territory name |
| `mmwr_year` | INTEGER | Morbidity and Mortality Weekly Report year |
| `mmwr_week` | INTEGER | MMWR epidemiological week number (1-52) |
| `disease` | VARCHAR(200) | Notifiable disease or condition name |
| `current_week` | NUMERIC | Case count for the current MMWR week |
| `current_week_flag` | VARCHAR(10) | Flag indicating data quality issues (U = unavailable) |
| `previous_52_weeks_max` | NUMERIC | Maximum weekly cases in the prior 52 weeks |
| `cum_2024` | NUMERIC | Year-to-date cumulative cases (current year) |
| `cum_2023` | NUMERIC | Year-to-date cumulative cases (prior year) |
| `cum_2024_flag` | VARCHAR(10) | Data quality flag for YTD current year |
| `cum_2023_flag` | VARCHAR(10) | Data quality flag for YTD prior year |
| `ingested_at` | TIMESTAMP | UTC timestamp of when record was loaded |

---

## View: `vw_curated_health_cases`

| Column | Type | Description |
|---|---|---|
| `state` | VARCHAR | Standardized U.S. state name |
| `reporting_year` | INTEGER | MMWR reporting year |
| `reporting_week` | INTEGER | MMWR week number |
| `disease_name` | VARCHAR | Notifiable disease name |
| `weekly_cases` | NUMERIC | Cases reported in current week (null-safe) |
| `max_52_week_cases` | NUMERIC | Historical max for prior 52 weeks |
| `ytd_cases_current` | NUMERIC | YTD cases current year (null-safe) |
| `ytd_cases_prior_year` | NUMERIC | YTD cases prior year (null-safe) |
| `yoy_pct_change` | NUMERIC | Year-over-year % change in YTD cases |
| `data_completeness_flag` | VARCHAR | 'Complete' or 'Incomplete' based on flag field |
| `ingested_at` | TIMESTAMP | Source ingestion timestamp |

---

## View: `vw_weekly_trend`

| Column | Type | Description |
|---|---|---|
| `mmwr_year` | INTEGER | Reporting year |
| `mmwr_week` | INTEGER | Reporting week |
| `disease` | VARCHAR | Disease name |
| `total_weekly_cases` | NUMERIC | Aggregated weekly case count |
| `states_reporting` | INTEGER | Count of distinct states that reported |

---

## View: `vw_state_summary`

| Column | Type | Description |
|---|---|---|
| `state` | VARCHAR | U.S. state name |
| `mmwr_year` | INTEGER | Reporting year |
| `disease_count` | INTEGER | Number of distinct diseases reported |
| `total_weekly_cases` | NUMERIC | Total cases in current week |
| `total_ytd_cases` | NUMERIC | Total YTD cases for the year |
| `reporting_completeness_pct` | NUMERIC | % of records with complete data |

---

## CDC Data Flags

| Flag Value | Meaning |
|---|---|
| `U` | Unavailable — data not yet reported |
| `N` | Not reportable — disease not notifiable in that jurisdiction |
| `-` | No reported cases |
| `C` | Cumulative YTD case counts are confidential |
| (blank) | Data is complete and available |
