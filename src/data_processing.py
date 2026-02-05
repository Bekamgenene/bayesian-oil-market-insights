"""
Data loading and preprocessing utilities for Brent oil price analysis.
"""

import pandas as pd
import numpy as np
from typing import Optional, Tuple
from pathlib import Path


def load_brent_prices(file_path: str) -> pd.DataFrame:
    """
    Load Brent oil prices from CSV file.
    
    Parameters
    ----------
    file_path : str
        Path to the BrentOilPrices.csv file
        
    Returns
    -------
    pd.DataFrame
        DataFrame with Date index and Price column
        
    Raises
    ------
    FileNotFoundError
        If the file doesn't exist
    ValueError
        If the data format is invalid
    """
    if not Path(file_path).exists():
        raise FileNotFoundError(f"File not found: {file_path}")
    
    df = pd.read_csv(file_path)
    
    # Validate columns
    if 'Date' not in df.columns or 'Price' not in df.columns:
        raise ValueError("CSV must contain 'Date' and 'Price' columns")
    
    # Convert date and set as index
    df['Date'] = pd.to_datetime(df['Date'], format='%d-%b-%y')
    df = df.sort_values('Date').reset_index(drop=True)
    df.set_index('Date', inplace=True)
    
    return df


def load_events(file_path: str) -> pd.DataFrame:
    """
    Load major oil market events from CSV file.
    
    Parameters
    ----------
    file_path : str
        Path to the events CSV file
        
    Returns
    -------
    pd.DataFrame
        DataFrame with event information
        
    Raises
    ------
    FileNotFoundError
        If the file doesn't exist
    """
    if not Path(file_path).exists():
        raise FileNotFoundError(f"File not found: {file_path}")
    
    df = pd.read_csv(file_path)
    df['Date'] = pd.to_datetime(df['Date'])
    df = df.sort_values('Date').reset_index(drop=True)
    
    return df


def calculate_log_returns(prices: pd.Series) -> pd.Series:
    """
    Calculate log returns from price series.
    
    Parameters
    ----------
    prices : pd.Series
        Price series
        
    Returns
    -------
    pd.Series
        Log returns: log(price_t) - log(price_{t-1})
    """
    log_prices = np.log(prices)
    log_returns = log_prices.diff()
    return log_returns


def calculate_simple_returns(prices: pd.Series) -> pd.Series:
    """
    Calculate simple percentage returns from price series.
    
    Parameters
    ----------
    prices : pd.Series
        Price series
        
    Returns
    -------
    pd.Series
        Simple returns: (price_t - price_{t-1}) / price_{t-1}
    """
    return prices.pct_change()


def calculate_rolling_volatility(
    returns: pd.Series, 
    window: int = 30
) -> pd.Series:
    """
    Calculate rolling volatility (standard deviation of returns).
    
    Parameters
    ----------
    returns : pd.Series
        Return series
    window : int, optional
        Rolling window size in days (default: 30)
        
    Returns
    -------
    pd.Series
        Rolling volatility
    """
    return returns.rolling(window=window).std()


def filter_date_range(
    df: pd.DataFrame,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None
) -> pd.DataFrame:
    """
    Filter DataFrame by date range.
    
    Parameters
    ----------
    df : pd.DataFrame
        DataFrame with DatetimeIndex
    start_date : str, optional
        Start date (inclusive) in format 'YYYY-MM-DD'
    end_date : str, optional
        End date (inclusive) in format 'YYYY-MM-DD'
        
    Returns
    -------
    pd.DataFrame
        Filtered DataFrame
    """
    if start_date:
        df = df[df.index >= pd.Timestamp(start_date)]
    if end_date:
        df = df[df.index <= pd.Timestamp(end_date)]
    return df


def prepare_modeling_data(
    price_file: str,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    calculate_returns: bool = True
) -> pd.DataFrame:
    """
    Prepare complete dataset for modeling.
    
    Parameters
    ----------
    price_file : str
        Path to price CSV file
    start_date : str, optional
        Start date for filtering
    end_date : str, optional
        End date for filtering
    calculate_returns : bool, optional
        Whether to calculate log returns (default: True)
        
    Returns
    -------
    pd.DataFrame
        Prepared dataset with prices and optionally returns
    """
    df = load_brent_prices(price_file)
    
    if start_date or end_date:
        df = filter_date_range(df, start_date, end_date)
    
    if calculate_returns:
        df['Log_Returns'] = calculate_log_returns(df['Price'])
        df['Simple_Returns'] = calculate_simple_returns(df['Price'])
        df['Volatility_30d'] = calculate_rolling_volatility(df['Log_Returns'], window=30)
    
    return df


def get_data_summary(df: pd.DataFrame) -> dict:
    """
    Get summary statistics for the dataset.
    
    Parameters
    ----------
    df : pd.DataFrame
        DataFrame with price data
        
    Returns
    -------
    dict
        Dictionary with summary statistics
    """
    summary = {
        'n_observations': len(df),
        'date_range': {
            'start': df.index.min(),
            'end': df.index.max()
        },
        'price_stats': {
            'mean': df['Price'].mean(),
            'median': df['Price'].median(),
            'std': df['Price'].std(),
            'min': df['Price'].min(),
            'max': df['Price'].max()
        },
        'missing_values': df['Price'].isna().sum()
    }
    
    if 'Log_Returns' in df.columns:
        summary['returns_stats'] = {
            'mean': df['Log_Returns'].mean(),
            'std': df['Log_Returns'].std(),
            'skewness': df['Log_Returns'].skew(),
            'kurtosis': df['Log_Returns'].kurtosis()
        }
    
    return summary
