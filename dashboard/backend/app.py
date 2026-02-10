"""
Flask Backend API for Bayesian Oil Market Insights Dashboard
Provides REST endpoints for price data, events, and changepoint analysis results
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
import pandas as pd
import json
from pathlib import Path
from datetime import datetime

app = Flask(__name__)
CORS(app)  # Enable CORS for React frontend

# Data paths
DATA_DIR = Path(__file__).parent.parent.parent / "data"

# Load data on startup
def load_all_data():
    """Load all required datasets"""
    try:
        # Price data with changepoint indicator
        df = pd.read_csv(DATA_DIR / "brent_with_changepoint.csv")
        df['Date'] = pd.to_datetime(df['Date'])
        
        # Events data
        events_df = pd.read_csv(DATA_DIR / "structured_events.csv")
        events_df['Date'] = pd.to_datetime(events_df['Date'])
        
        # Changepoint results
        with open(DATA_DIR / "changepoint_results.json", 'r') as f:
            results = json.load(f)
        
        return df, events_df, results
    except Exception as e:
        print(f"Error loading data: {e}")
        return None, None, None

# Global data variables
price_data, events_data, changepoint_results = load_all_data()

# ============================================================================
# API ENDPOINTS
# ============================================================================

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'message': 'Bayesian Oil Market API is running',
        'version': '1.0.0'
    })

@app.route('/api/prices', methods=['GET'])
def get_prices():
    """
    Get Brent oil price data with optional date filtering
    
    Query Parameters:
        start_date (str): Start date in YYYY-MM-DD format
        end_date (str): End date in YYYY-MM-DD format
    
    Returns:
        JSON array of price records
    """
    try:
        df = price_data.copy()
        
        # Apply date filters if provided
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        if start_date:
            df = df[df['Date'] >= pd.to_datetime(start_date)]
        if end_date:
            df = df[df['Date'] <= pd.to_datetime(end_date)]
        
        # Convert to JSON-friendly format
        df['Date'] = df['Date'].dt.strftime('%Y-%m-%d')
        
        return jsonify({
            'success': True,
            'count': len(df),
            'data': df.to_dict(orient='records')
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/events', methods=['GET'])
def get_events():
    """
    Get major oil market events with optional filtering
    
    Query Parameters:
        start_date (str): Start date in YYYY-MM-DD format
        end_date (str): End date in YYYY-MM-DD format
        event_type (str): Filter by event type (OPEC_Decision, Geopolitical, Economic_Shock)
    
    Returns:
        JSON array of event records
    """
    try:
        df = events_data.copy()
        
        # Apply date filters
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        event_type = request.args.get('event_type')
        
        if start_date:
            df = df[df['Date'] >= pd.to_datetime(start_date)]
        if end_date:
            df = df[df['Date'] <= pd.to_datetime(end_date)]
        if event_type:
            df = df[df['Event_Type'] == event_type]
        
        # Convert to JSON-friendly format
        df['Date'] = df['Date'].dt.strftime('%Y-%m-%d')
        
        return jsonify({
            'success': True,
            'count': len(df),
            'data': df.to_dict(orient='records')
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/changepoint', methods=['GET'])
def get_changepoint():
    """
    Get Bayesian changepoint analysis results
    
    Returns:
        JSON object with changepoint statistics and parameters
    """
    try:
        return jsonify({
            'success': True,
            'data': changepoint_results
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/statistics', methods=['GET'])
def get_statistics():
    """
    Get summary statistics for price data
    
    Query Parameters:
        start_date (str): Start date for statistics calculation
        end_date (str): End date for statistics calculation
    
    Returns:
        JSON object with statistical metrics
    """
    try:
        df = price_data.copy()
        
        # Apply date filters
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        if start_date:
            df = df[df['Date'] >= pd.to_datetime(start_date)]
        if end_date:
            df = df[df['Date'] <= pd.to_datetime(end_date)]
        
        # Calculate statistics
        stats = {
            'count': len(df),
            'mean_price': float(df['Price'].mean()),
            'median_price': float(df['Price'].median()),
            'std_price': float(df['Price'].std()),
            'min_price': float(df['Price'].min()),
            'max_price': float(df['Price'].max()),
            'mean_return': float(df['log_return'].mean()) if 'log_return' in df.columns else None,
            'volatility': float(df['log_return'].std()) if 'log_return' in df.columns else None
        }
        
        return jsonify({
            'success': True,
            'data': stats
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/event-types', methods=['GET'])
def get_event_types():
    """
    Get list of unique event types
    
    Returns:
        JSON array of event type strings
    """
    try:
        event_types = events_data['Event_Type'].unique().tolist()
        
        return jsonify({
            'success': True,
            'data': event_types
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/date-range', methods=['GET'])
def get_date_range():
    """
    Get available date range in the dataset
    
    Returns:
        JSON object with min and max dates
    """
    try:
        return jsonify({
            'success': True,
            'data': {
                'min_date': price_data['Date'].min().strftime('%Y-%m-%d'),
                'max_date': price_data['Date'].max().strftime('%Y-%m-%d')
            }
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'success': False,
        'error': 'Endpoint not found',
        'message': 'The requested API endpoint does not exist'
    }), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        'success': False,
        'error': 'Internal server error',
        'message': 'An unexpected error occurred'
    }), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
