"""
Tests for data processing utilities.
"""

import pytest
import pandas as pd
import numpy as np
from pathlib import Path
import sys

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from data_processing import (
    load_brent_prices,
    load_events,
    calculate_log_returns,
    calculate_simple_returns,
    calculate_rolling_volatility,
    filter_date_range,
    get_data_summary
)


@pytest.fixture
def sample_price_data():
    """Create sample price data for testing."""
    dates = pd.date_range('2020-01-01', periods=100, freq='D')
    prices = np.random.uniform(50, 100, size=100)
    df = pd.DataFrame({'Price': prices}, index=dates)
    df.index.name = 'Date'
    return df


@pytest.fixture
def sample_price_csv(tmp_path):
    """Create a temporary CSV file with sample price data."""
    csv_file = tmp_path / "test_prices.csv"
    data = {
        'Date': ['01-Jan-20', '02-Jan-20', '03-Jan-20', '04-Jan-20', '05-Jan-20'],
        'Price': [60.5, 61.2, 59.8, 62.1, 63.5]
    }
    df = pd.DataFrame(data)
    df.to_csv(csv_file, index=False)
    return str(csv_file)


@pytest.fixture
def sample_events_csv(tmp_path):
    """Create a temporary CSV file with sample events."""
    csv_file = tmp_path / "test_events.csv"
    data = {
        'Date': ['2020-01-15', '2020-03-09'],
        'Event_Name': ['Test Event 1', 'Test Event 2'],
        'Category': ['OPEC Policy', 'Geopolitical'],
        'Description': ['Test description 1', 'Test description 2'],
        'Expected_Impact': ['Upward', 'Downward']
    }
    df = pd.DataFrame(data)
    df.to_csv(csv_file, index=False)
    return str(csv_file)


class TestLoadBrentPrices:
    """Tests for load_brent_prices function."""
    
    def test_load_valid_csv(self, sample_price_csv):
        """Test loading valid CSV file."""
        df = load_brent_prices(sample_price_csv)
        
        assert isinstance(df, pd.DataFrame)
        assert isinstance(df.index, pd.DatetimeIndex)
        assert 'Price' in df.columns
        assert len(df) == 5
    
    def test_file_not_found(self):
        """Test error when file doesn't exist."""
        with pytest.raises(FileNotFoundError):
            load_brent_prices('nonexistent_file.csv')
    
    def test_invalid_columns(self, tmp_path):
        """Test error when CSV has invalid columns."""
        csv_file = tmp_path / "invalid.csv"
        df = pd.DataFrame({'Wrong': [1, 2], 'Columns': [3, 4]})
        df.to_csv(csv_file, index=False)
        
        with pytest.raises(ValueError):
            load_brent_prices(str(csv_file))
    
    def test_date_sorting(self, tmp_path):
        """Test that dates are sorted correctly."""
        csv_file = tmp_path / "unsorted.csv"
        data = {
            'Date': ['05-Jan-20', '02-Jan-20', '01-Jan-20', '03-Jan-20'],
            'Price': [60, 61, 62, 63]
        }
        df = pd.DataFrame(data)
        df.to_csv(csv_file, index=False)
        
        result = load_brent_prices(str(csv_file))
        assert result.index[0] < result.index[-1]  # Ascending order


class TestLoadEvents:
    """Tests for load_events function."""
    
    def test_load_valid_events(self, sample_events_csv):
        """Test loading valid events CSV."""
        df = load_events(sample_events_csv)
        
        assert isinstance(df, pd.DataFrame)
        assert 'Date' in df.columns
        assert 'Event_Name' in df.columns
        assert len(df) == 2
    
    def test_events_file_not_found(self):
        """Test error when events file doesn't exist."""
        with pytest.raises(FileNotFoundError):
            load_events('nonexistent_events.csv')


class TestCalculateReturns:
    """Tests for return calculation functions."""
    
    def test_log_returns(self, sample_price_data):
        """Test log returns calculation."""
        returns = calculate_log_returns(sample_price_data['Price'])
        
        assert isinstance(returns, pd.Series)
        assert len(returns) == len(sample_price_data)
        assert pd.isna(returns.iloc[0])  # First value should be NaN
        assert not pd.isna(returns.iloc[1])  # Second value should exist
    
    def test_simple_returns(self, sample_price_data):
        """Test simple returns calculation."""
        returns = calculate_simple_returns(sample_price_data['Price'])
        
        assert isinstance(returns, pd.Series)
        assert len(returns) == len(sample_price_data)
        assert pd.isna(returns.iloc[0])
    
    def test_log_returns_values(self):
        """Test log returns with known values."""
        prices = pd.Series([100, 110, 105])
        returns = calculate_log_returns(prices)
        
        expected_1 = np.log(110) - np.log(100)
        expected_2 = np.log(105) - np.log(110)
        
        assert np.isclose(returns.iloc[1], expected_1)
        assert np.isclose(returns.iloc[2], expected_2)


class TestCalculateVolatility:
    """Tests for volatility calculation."""
    
    def test_rolling_volatility(self, sample_price_data):
        """Test rolling volatility calculation."""
        returns = calculate_log_returns(sample_price_data['Price'])
        volatility = calculate_rolling_volatility(returns, window=10)
        
        assert isinstance(volatility, pd.Series)
        assert len(volatility) == len(returns)
        # First (window-1) values should be NaN
        assert pd.isna(volatility.iloc[8])
        assert not pd.isna(volatility.iloc[10])
    
    def test_volatility_window_size(self, sample_price_data):
        """Test different window sizes."""
        returns = calculate_log_returns(sample_price_data['Price'])
        
        vol_10 = calculate_rolling_volatility(returns, window=10)
        vol_30 = calculate_rolling_volatility(returns, window=30)
        
        # 30-day volatility should be smoother (fewer non-NaN values)
        assert vol_10.notna().sum() > vol_30.notna().sum()


class TestFilterDateRange:
    """Tests for date filtering."""
    
    def test_filter_start_date(self, sample_price_data):
        """Test filtering with start date."""
        filtered = filter_date_range(
            sample_price_data,
            start_date='2020-02-01'
        )
        
        assert len(filtered) < len(sample_price_data)
        assert filtered.index.min() >= pd.Timestamp('2020-02-01')
    
    def test_filter_end_date(self, sample_price_data):
        """Test filtering with end date."""
        filtered = filter_date_range(
            sample_price_data,
            end_date='2020-02-01'
        )
        
        assert len(filtered) < len(sample_price_data)
        assert filtered.index.max() <= pd.Timestamp('2020-02-01')
    
    def test_filter_both_dates(self, sample_price_data):
        """Test filtering with both start and end dates."""
        filtered = filter_date_range(
            sample_price_data,
            start_date='2020-02-01',
            end_date='2020-03-01'
        )
        
        assert filtered.index.min() >= pd.Timestamp('2020-02-01')
        assert filtered.index.max() <= pd.Timestamp('2020-03-01')


class TestGetDataSummary:
    """Tests for data summary function."""
    
    def test_basic_summary(self, sample_price_data):
        """Test basic summary statistics."""
        summary = get_data_summary(sample_price_data)
        
        assert 'n_observations' in summary
        assert 'date_range' in summary
        assert 'price_stats' in summary
        assert summary['n_observations'] == len(sample_price_data)
        assert 'mean' in summary['price_stats']
        assert 'std' in summary['price_stats']
    
    def test_summary_with_returns(self, sample_price_data):
        """Test summary with returns included."""
        sample_price_data['Log_Returns'] = calculate_log_returns(
            sample_price_data['Price']
        )
        
        summary = get_data_summary(sample_price_data)
        
        assert 'returns_stats' in summary
        assert 'mean' in summary['returns_stats']
        assert 'skewness' in summary['returns_stats']
        assert 'kurtosis' in summary['returns_stats']


class TestIntegration:
    """Integration tests for combined functionality."""
    
    def test_full_data_preparation(self, sample_price_csv):
        """Test complete data preparation pipeline."""
        # This would normally use the real data file
        df = load_brent_prices(sample_price_csv)
        
        # Add returns
        df['Log_Returns'] = calculate_log_returns(df['Price'])
        df['Volatility'] = calculate_rolling_volatility(df['Log_Returns'], window=3)
        
        # Filter date range
        filtered = filter_date_range(df, start_date='2020-01-02')
        
        # Get summary
        summary = get_data_summary(filtered)
        
        assert summary['n_observations'] == 4  # 5 days - 1 filtered
        assert 'returns_stats' in summary
