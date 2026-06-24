"""
Unit Tests - Public Health Dashboard Pipeline
Author: Sai Deva Puttur
Description: Tests for data ingestion, cleaning, and validation logic
"""

import pytest
import pandas as pd
from unittest.mock import patch, MagicMock
from datetime import datetime
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'data_ingestion'))


# ============================================================
# FIXTURES
# ============================================================

@pytest.fixture
def sample_raw_data():
    """Sample raw CDC API response data."""
    return [
        {
            "reporting_area": "New York",
            "mmwr_year": "2024",
            "mmwr_week": "10",
            "disease": "Influenza",
            "current_week": "150",
            "current_week_flag": None,
            "previous_52_weeks_max": "500",
            "cum_2024": "1200",
            "cum_2023": "1100",
        },
        {
            "reporting_area": "california",  # Lowercase - should be normalized
            "mmwr_year": "2024",
            "mmwr_week": "10",
            "disease": "COVID-19",
            "current_week": None,           # Missing value
            "current_week_flag": "U",
            "previous_52_weeks_max": "2000",
            "cum_2024": None,               # Missing YTD
            "cum_2023": "3500",
        }
    ]


@pytest.fixture
def sample_dataframe(sample_raw_data):
    """Convert sample data to DataFrame."""
    return pd.DataFrame(sample_raw_data)


# ============================================================
# TESTS: fetch_cdc_data
# ============================================================

class TestFetchCDCData:

    @patch('requests.get')
    def test_fetch_returns_dataframe(self, mock_get):
        """Test that fetch returns a non-empty DataFrame."""
        from ingest_cdc_data import fetch_cdc_data
        mock_response = MagicMock()
        mock_response.json.return_value = [{"disease": "Influenza", "mmwr_year": "2024"}]
        mock_response.raise_for_status = MagicMock()
        mock_get.return_value = mock_response

        result = fetch_cdc_data("https://fake-cdc-url.gov/resource/test.json", limit=10)
        assert isinstance(result, pd.DataFrame)
        assert len(result) == 1

    @patch('requests.get')
    def test_fetch_raises_on_api_error(self, mock_get):
        """Test that HTTP errors are propagated correctly."""
        from ingest_cdc_data import fetch_cdc_data
        import requests
        mock_get.side_effect = requests.exceptions.HTTPError("404 Not Found")

        with pytest.raises(requests.exceptions.HTTPError):
            fetch_cdc_data("https://fake-url.gov", limit=10)


# ============================================================
# TESTS: clean_data
# ============================================================

class TestCleanData:

    def test_column_names_normalized(self, sample_dataframe):
        """Test that column names are lowercased and stripped."""
        from ingest_cdc_data import clean_data
        result = clean_data(sample_dataframe.copy())
        for col in result.columns:
            assert col == col.lower().strip()

    def test_reporting_area_title_cased(self, sample_dataframe):
        """Test that reporting_area is normalized to Title Case."""
        from ingest_cdc_data import clean_data
        result = clean_data(sample_dataframe.copy())
        if 'reporting_area' in result.columns:
            assert result['reporting_area'].iloc[1] == 'California'

    def test_numeric_conversion(self, sample_dataframe):
        """Test that numeric columns are properly cast."""
        from ingest_cdc_data import clean_data
        result = clean_data(sample_dataframe.copy())
        if 'current_week' in result.columns:
            assert pd.api.types.is_numeric_dtype(result['current_week'])

    def test_ingested_at_column_added(self, sample_dataframe):
        """Test that ingested_at timestamp is added."""
        from ingest_cdc_data import clean_data
        result = clean_data(sample_dataframe.copy())
        assert 'ingested_at' in result.columns

    def test_no_duplicate_rows(self, sample_dataframe):
        """Test that duplicates are removed."""
        from ingest_cdc_data import clean_data
        doubled = pd.concat([sample_dataframe, sample_dataframe], ignore_index=True)
        result = clean_data(doubled)
        assert len(result) <= len(sample_dataframe)


# ============================================================
# TESTS: Data Validation
# ============================================================

class TestDataValidation:

    def test_required_fields_present(self, sample_dataframe):
        """Test that key CDC fields exist in the dataset."""
        expected_fields = ['reporting_area', 'mmwr_year', 'mmwr_week', 'disease']
        for field in expected_fields:
            assert field in sample_dataframe.columns

    def test_no_all_null_columns(self, sample_dataframe):
        """Test that no column is entirely null."""
        from ingest_cdc_data import clean_data
        result = clean_data(sample_dataframe.copy())
        for col in result.columns:
            assert not result[col].isna().all(), f"Column {col} is entirely null"


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
