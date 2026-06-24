-- ============================================================
-- Public Health Dashboard Pipeline - PostgreSQL Schema
-- Author: Sai Deva Puttur
-- Description: Table definitions for raw and curated CDC data
-- ============================================================

-- Create database (run separately)
-- CREATE DATABASE public_health_db;

-- ============================================================
-- RAW LAYER: Stores ingested CDC data as-is
-- ============================================================

CREATE TABLE IF NOT EXISTS raw_cdc_cases (
    id                      SERIAL PRIMARY KEY,
    reporting_area          VARCHAR(100),
    mmwr_year               INTEGER,
    mmwr_week               INTEGER,
    disease                 VARCHAR(200),
    current_week            NUMERIC,
    current_week_flag       VARCHAR(10),
    previous_52_weeks_max   NUMERIC,
    cum_2024                NUMERIC,
    cum_2023                NUMERIC,
    cum_2024_flag           VARCHAR(10),
    cum_2023_flag           VARCHAR(10),
    ingested_at             TIMESTAMP DEFAULT NOW()
);

COMMENT ON TABLE raw_cdc_cases IS 'Raw CDC NNDSS disease surveillance records ingested from the CDC open data API';

-- ============================================================
-- CURATED LAYER: Cleaned, analytics-ready table
-- ============================================================

CREATE TABLE IF NOT EXISTS curated_health_cases (
    id                      SERIAL PRIMARY KEY,
    reporting_state         VARCHAR(100),
    mmwr_year               INTEGER,
    mmwr_week               INTEGER,
    disease_name            VARCHAR(200),
    weekly_cases            NUMERIC,
    max_52_week_cases       NUMERIC,
    ytd_cases_current       NUMERIC,
    ytd_cases_prior_year    NUMERIC,
    yoy_change              NUMERIC,
    data_completeness_flag  VARCHAR(20),
    loaded_at               TIMESTAMP DEFAULT NOW()
);

COMMENT ON TABLE curated_health_cases IS 'Curated and transformed CDC health case data ready for Power BI reporting';

-- ============================================================
-- REPORTING LAYER: Summary table for dashboard KPIs
-- ============================================================

CREATE TABLE IF NOT EXISTS kpi_weekly_summary (
    id                  SERIAL PRIMARY KEY,
    snapshot_date       DATE,
    total_cases_week    NUMERIC,
    top_disease         VARCHAR(200),
    top_state           VARCHAR(100),
    states_reporting    INTEGER,
    data_completeness   NUMERIC,
    generated_at        TIMESTAMP DEFAULT NOW()
);

COMMENT ON TABLE kpi_weekly_summary IS 'Weekly KPI snapshot table used by Power BI for executive dashboard';

-- Index for performance on common filters
CREATE INDEX IF NOT EXISTS idx_raw_mmwr_year ON raw_cdc_cases(mmwr_year);
CREATE INDEX IF NOT EXISTS idx_raw_reporting_area ON raw_cdc_cases(reporting_area);
CREATE INDEX IF NOT EXISTS idx_curated_disease ON curated_health_cases(disease_name);
CREATE INDEX IF NOT EXISTS idx_curated_state ON curated_health_cases(reporting_state);
