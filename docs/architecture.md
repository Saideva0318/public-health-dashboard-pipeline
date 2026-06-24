# Architecture - Public Health Dashboard Pipeline

## Overview

This pipeline follows a classic **ELT (Extract, Load, Transform)** pattern, common in modern data engineering stacks. Data is extracted from the CDC's public API, loaded into PostgreSQL in raw form, then transformed using SQL views for Power BI consumption.

---

## Architecture Flow

```
+---------------------------+
|   CDC Open Data API       |
|   data.cdc.gov            |
|   (NNDSS Dataset)         |
+---------------------------+
            |
            | HTTP GET / JSON
            v
+---------------------------+
|  Python Ingestion Layer   |
|  ingest_cdc_data.py       |
|  - Fetch CDC API data     |
|  - Validate schema        |
|  - Clean & normalize      |
|  - Log ingestion events   |
+---------------------------+
            |
            | psycopg2 bulk insert
            v
+---------------------------+
|  PostgreSQL Database      |
|  public_health_db         |
|                           |
|  [RAW LAYER]              |
|   raw_cdc_cases           |
|                           |
|  [CURATED VIEWS]          |
|   vw_curated_health_cases |
|   vw_weekly_trend         |
|   vw_state_summary        |
|   vw_top_diseases         |
|   vw_data_quality         |
+---------------------------+
            |
            | DirectQuery / Import
            v
+---------------------------+
|  Power BI Dashboard       |
|  - Disease trend charts   |
|  - State map visual       |
|  - Top diseases table     |
|  - Data quality card      |
|  - YoY comparison bar     |
+---------------------------+
```

---

## Layer Descriptions

### Extract
- **Source:** CDC NNDSS open dataset via Socrata Open Data API
- **Format:** JSON response, up to 5,000 records per call
- **Auth:** No API key required (public dataset)

### Load (Raw)
- **Destination:** `raw_cdc_cases` PostgreSQL table
- **Strategy:** Append-only with `ON CONFLICT DO NOTHING` deduplication
- **Schema:** Preserves all raw CDC fields + `ingested_at` timestamp

### Transform (Curated)
- **Engine:** PostgreSQL SQL Views (no dbt for simplicity; can be upgraded)
- **Logic:** COALESCE for null handling, YoY % change, completeness flags
- **Output Views:** 5 views covering trends, states, diseases, and quality

### Visualize
- **Tool:** Power BI Desktop
- **Connection:** DirectQuery to PostgreSQL via native connector
- **Refresh:** Manual or scheduled (Airflow optional upgrade path)

---

## Upgrade Path

| Feature | Current | Next Step |
|---|---|---|
| Scheduling | Manual run | Apache Airflow DAG |
| Transformation | SQL Views | dbt models |
| Storage | PostgreSQL | Snowflake / BigQuery |
| Raw storage | PostgreSQL | AWS S3 / GCS data lake |
| Dashboard | Power BI | Looker / Metabase |

---

## Environment Variables

| Variable | Description |
|---|---|
| `DB_HOST` | PostgreSQL host (default: localhost) |
| `DB_PORT` | PostgreSQL port (default: 5432) |
| `DB_NAME` | Database name (default: public_health_db) |
| `DB_USER` | PostgreSQL username |
| `DB_PASSWORD` | PostgreSQL password |
