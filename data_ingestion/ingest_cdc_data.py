"""
CDC Public Health Data Ingestion Pipeline
Author: Sai Deva Puttur
Description: Downloads CDC open health data, cleans it, and loads into PostgreSQL
"""

import requests
import pandas as pd
import psycopg2
from psycopg2.extras import execute_values
import logging
from datetime import datetime
import os

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# CDC Open Data API endpoint (NNDSS - Weekly Cases)
CDC_API_URL = "https://data.cdc.gov/resource/x9gk-5huc.json"
LIMIT = 5000

# PostgreSQL connection config (use env vars in production)
DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "port": os.getenv("DB_PORT", 5432),
    "database": os.getenv("DB_NAME", "public_health_db"),
    "user": os.getenv("DB_USER", "postgres"),
    "password": os.getenv("DB_PASSWORD", "")
}


def fetch_cdc_data(url: str, limit: int = 5000) -> pd.DataFrame:
    """Fetch data from CDC Socrata Open Data API."""
    logger.info(f"Fetching CDC data from: {url}")
    params = {"$limit": limit, "$order": "mmwr_year DESC"}
    response = requests.get(url, params=params, timeout=30)
    response.raise_for_status()
    data = response.json()
    df = pd.DataFrame(data)
    logger.info(f"Fetched {len(df)} records from CDC API")
    return df


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """Clean and normalize the raw CDC dataset."""
    logger.info("Cleaning and normalizing data...")

    # Standardize column names
    df.columns = [col.lower().strip().replace(" ", "_") for col in df.columns]

    # Drop fully null columns
    df.dropna(axis=1, how="all", inplace=True)

    # Convert numeric fields
    numeric_cols = ["current_week", "previous_52_weeks_max", "cum_2024", "cum_2023"]
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    # Standardize state names
    if "reporting_area" in df.columns:
        df["reporting_area"] = df["reporting_area"].str.strip().str.title()

    # Add ingestion timestamp
    df["ingested_at"] = datetime.utcnow()

    # Drop duplicates
    df.drop_duplicates(inplace=True)

    logger.info(f"Cleaned data shape: {df.shape}")
    return df


def load_to_postgres(df: pd.DataFrame, table_name: str = "raw_cdc_cases") -> None:
    """Load cleaned DataFrame into PostgreSQL."""
    logger.info(f"Loading {len(df)} rows into PostgreSQL table: {table_name}")
    conn = psycopg2.connect(**DB_CONFIG)
    cursor = conn.cursor()

    columns = list(df.columns)
    values = [tuple(row) for row in df.itertuples(index=False, name=None)]

    insert_sql = f"""
        INSERT INTO {table_name} ({', '.join(columns)})
        VALUES %s
        ON CONFLICT DO NOTHING
    """
    execute_values(cursor, insert_sql, values)
    conn.commit()
    cursor.close()
    conn.close()
    logger.info("Data loaded successfully.")


def run_pipeline():
    """Main pipeline runner."""
    logger.info("Starting CDC Public Health Ingestion Pipeline...")
    try:
        raw_df = fetch_cdc_data(CDC_API_URL, limit=LIMIT)
        clean_df = clean_data(raw_df)
        load_to_postgres(clean_df)
        logger.info("Pipeline completed successfully.")
    except Exception as e:
        logger.error(f"Pipeline failed: {e}")
        raise


if __name__ == "__main__":
    run_pipeline()
