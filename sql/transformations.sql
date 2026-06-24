-- ============================================================
-- Public Health Dashboard Pipeline - SQL Transformations
-- Author: Sai Deva Puttur
-- Description: Views and KPI queries for Power BI dashboard
-- ============================================================

-- ============================================================
-- VIEW 1: Curated case data with YoY change calculation
-- ============================================================

CREATE OR REPLACE VIEW vw_curated_health_cases AS
SELECT
    reporting_area                          AS state,
    mmwr_year                               AS reporting_year,
    mmwr_week                               AS reporting_week,
    disease                                 AS disease_name,
    COALESCE(current_week, 0)               AS weekly_cases,
    COALESCE(previous_52_weeks_max, 0)      AS max_52_week_cases,
    COALESCE(cum_2024, 0)                   AS ytd_cases_current,
    COALESCE(cum_2023, 0)                   AS ytd_cases_prior_year,
    CASE
        WHEN COALESCE(cum_2023, 0) = 0 THEN NULL
        ELSE ROUND(((COALESCE(cum_2024, 0) - COALESCE(cum_2023, 0)) / NULLIF(cum_2023, 0)) * 100, 2)
    END                                     AS yoy_pct_change,
    CASE
        WHEN current_week_flag IS NOT NULL THEN 'Incomplete'
        ELSE 'Complete'
    END                                     AS data_completeness_flag,
    ingested_at
FROM raw_cdc_cases
WHERE reporting_area IS NOT NULL
  AND disease IS NOT NULL;


-- ============================================================
-- VIEW 2: Weekly case trend by disease
-- ============================================================

CREATE OR REPLACE VIEW vw_weekly_trend AS
SELECT
    mmwr_year,
    mmwr_week,
    disease,
    SUM(COALESCE(current_week, 0))   AS total_weekly_cases,
    COUNT(DISTINCT reporting_area)   AS states_reporting
FROM raw_cdc_cases
GROUP BY mmwr_year, mmwr_week, disease
ORDER BY mmwr_year DESC, mmwr_week DESC;


-- ============================================================
-- VIEW 3: State-level summary
-- ============================================================

CREATE OR REPLACE VIEW vw_state_summary AS
SELECT
    reporting_area                      AS state,
    mmwr_year,
    COUNT(DISTINCT disease)             AS disease_count,
    SUM(COALESCE(current_week, 0))      AS total_weekly_cases,
    SUM(COALESCE(cum_2024, 0))          AS total_ytd_cases,
    ROUND(
        100.0 * SUM(CASE WHEN current_week_flag IS NULL THEN 1 ELSE 0 END)
        / NULLIF(COUNT(*), 0), 2
    )                                   AS reporting_completeness_pct
FROM raw_cdc_cases
GROUP BY reporting_area, mmwr_year
ORDER BY total_ytd_cases DESC;


-- ============================================================
-- VIEW 4: Top diseases by case volume
-- ============================================================

CREATE OR REPLACE VIEW vw_top_diseases AS
SELECT
    disease,
    SUM(COALESCE(cum_2024, 0))      AS total_ytd_cases_2024,
    SUM(COALESCE(cum_2023, 0))      AS total_ytd_cases_2023,
    ROUND(
        100.0 * (SUM(COALESCE(cum_2024, 0)) - SUM(COALESCE(cum_2023, 0)))
        / NULLIF(SUM(COALESCE(cum_2023, 0)), 0), 2
    )                               AS yoy_pct_change
FROM raw_cdc_cases
GROUP BY disease
ORDER BY total_ytd_cases_2024 DESC
LIMIT 20;


-- ============================================================
-- VIEW 5: Data quality / completeness check
-- ============================================================

CREATE OR REPLACE VIEW vw_data_quality AS
SELECT
    mmwr_year,
    mmwr_week,
    COUNT(*)                                                AS total_records,
    SUM(CASE WHEN current_week IS NULL THEN 1 ELSE 0 END)   AS missing_weekly_cases,
    SUM(CASE WHEN cum_2024 IS NULL THEN 1 ELSE 0 END)       AS missing_ytd_2024,
    ROUND(
        100.0 * SUM(CASE WHEN current_week IS NOT NULL THEN 1 ELSE 0 END)
        / NULLIF(COUNT(*), 0), 2
    )                                                       AS completeness_pct
FROM raw_cdc_cases
GROUP BY mmwr_year, mmwr_week
ORDER BY mmwr_year DESC, mmwr_week DESC;
