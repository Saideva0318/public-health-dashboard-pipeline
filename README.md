# Public Health Dashboard Pipeline

![Python](https://img.shields.io/badge/Python-3.10-blue?logo=python) ![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-blue?logo=postgresql) ![Power BI](https://img.shields.io/badge/PowerBI-Dashboard-yellow?logo=powerbi) ![License](https://img.shields.io/badge/License-MIT-green)

> Built an end-to-end public health data pipeline using Python, SQL, PostgreSQL, and Power BI to transform CDC open data into analytics-ready tables and interactive surveillance dashboards.

---

## Business Problem

Public health agencies generate massive volumes of disease surveillance data that are difficult to monitor, analyze, and act on in a timely manner. This project simulates a real-world data engineering solution that ingests raw CDC open data, cleans and transforms it into curated tables, and exposes KPIs via an interactive Power BI dashboard for health analysts and decision-makers.

---

## Architecture

```
CDC Open Data (CSV/API)
        |
        v
 [Python Ingestion Layer]
  - Download & validate
  - Clean & normalize
  - Load to PostgreSQL
        |
        v
 [PostgreSQL Database]
  - Raw schema
  - Curated/transformed views
        |
        v
 [Power BI Dashboard]
  - Disease trend analysis
  - Geographic breakdown
  - Demographic split
  - Data completeness KPIs
```

---

## Tech Stack

| Layer | Tool |
|---|---|
| Ingestion | Python 3.10, Requests, Pandas |
| Storage | PostgreSQL 15 |
| Transformation | SQL (views, CTEs) |
| Visualization | Power BI |
| Orchestration | Apache Airflow (optional) |
| Version Control | Git, GitHub |

---

## Project Structure

```
public-health-dashboard-pipeline/
|-- data_ingestion/
|   |-- ingest_cdc_data.py       # Pull and load CDC data
|   |-- clean_data.py            # Data cleaning utilities
|-- sql/
|   |-- schema.sql               # PostgreSQL table definitions
|   |-- transformations.sql      # Curated views and KPI logic
|-- dashboard/
|   |-- dashboard_notes.md       # Power BI layout and KPI guide
|-- docs/
|   |-- architecture.md          # Architecture diagram details
|   |-- data_dictionary.md       # Field definitions
|-- tests/
|   |-- test_pipeline.py         # Unit tests for pipeline
|-- requirements.txt
|-- README.md
|-- LICENSE
```

---

## Dashboard KPIs

- Total reported cases by time period
- Weekly/monthly trend line
- State and regional case breakdown
- Top 5 conditions or disease categories
- Demographic split (age group, sex)
- Data completeness and reporting quality indicator

---

## Data Source

This project uses CDC Open Data:
- **CDC National Notifiable Disease Surveillance System (NNDSS)**
- Public dataset available at: https://data.cdc.gov
- No API key required for public datasets

---

## Setup & Run

```bash
# 1. Clone the repository
git clone https://github.com/Saideva0318/public-health-dashboard-pipeline.git
cd public-health-dashboard-pipeline

# 2. Install dependencies
pip install -r requirements.txt

# 3. Set up PostgreSQL database
psql -U postgres -f sql/schema.sql

# 4. Run the ingestion pipeline
python data_ingestion/ingest_cdc_data.py

# 5. Apply transformations
psql -U postgres -d public_health_db -f sql/transformations.sql

# 6. Open Power BI and connect to PostgreSQL
# See dashboard/dashboard_notes.md for setup guide
```

---

## Business Impact

- Reduced manual data processing time by automating CDC data ingestion
- Enabled real-time visibility into disease trends and regional health patterns
- Standardized reporting quality metrics across state-level data submissions
- Scalable architecture that can be extended to Airflow for full orchestration

---

## Author

**Sai Deva Puttur**  
Data Engineer | Analytics Professional | NYC Metro Area  
[GitHub](https://github.com/Saideva0318) | [LinkedIn](https://linkedin.com/in/saideva)

---

*MIT License - See LICENSE file for details*
