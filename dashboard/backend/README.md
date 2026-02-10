# Flask Backend API

REST API server for Bayesian Oil Market Insights dashboard.

## API Endpoints

### Health Check

```
GET /api/health
```

Returns server status and version.

**Response:**

```json
{
  "status": "healthy",
  "message": "Bayesian Oil Market API is running",
  "version": "1.0.0"
}
```

### Get Prices

```
GET /api/prices?start_date=2018-01-01&end_date=2022-12-31
```

Retrieve Brent oil price data with optional date filtering.

**Query Parameters:**

- `start_date` (optional): Start date (YYYY-MM-DD)
- `end_date` (optional): End date (YYYY-MM-DD)

**Response:**

```json
{
  "success": true,
  "count": 2258,
  "data": [
    {
      "Date": "2014-01-02",
      "Price": 110.38,
      "log_price": 4.703459,
      "log_return": 0.001234,
      "is_after_changepoint": 0
    }
  ]
}
```

### Get Events

```
GET /api/events?event_type=OPEC_Decision
```

Retrieve major oil market events with filtering.

**Query Parameters:**

- `start_date` (optional): Start date (YYYY-MM-DD)
- `end_date` (optional): End date (YYYY-MM-DD)
- `event_type` (optional): OPEC_Decision | Geopolitical | Economic_Shock

**Response:**

```json
{
  "success": true,
  "count": 15,
  "data": [
    {
      "Date": "2014-11-27",
      "Event_Type": "OPEC_Decision",
      "Description": "OPEC maintains production at 30M bpd...",
      "Expected_Impact": "Negative"
    }
  ]
}
```

### Get Changepoint Results

```
GET /api/changepoint
```

Retrieve Bayesian changepoint analysis results.

**Response:**

```json
{
  "success": true,
  "data": {
    "change_point_date": "2018-06-26",
    "change_point_index": 1140,
    "change_point_uncertainty_days": 1.02,
    "mu_before": -0.000403,
    "mu_after": 0.000909,
    "sigma_before": 0.02125,
    "sigma_after": 0.040032,
    "mean_change": 0.001312,
    "volatility_change": 0.018782,
    "price_before": 63.06,
    "price_after": 69.33,
    "price_change_pct": 9.95,
    "prob_mean_increase": 0.8,
    "prob_volatility_increase": 1.0
  }
}
```

### Get Statistics

```
GET /api/statistics?start_date=2018-06-26
```

Get summary statistics for filtered price data.

**Response:**

```json
{
  "success": true,
  "data": {
    "count": 1118,
    "mean_price": 69.33,
    "median_price": 67.25,
    "std_price": 15.42,
    "min_price": 19.33,
    "max_price": 117.68,
    "mean_return": 0.000909,
    "volatility": 0.040032
  }
}
```

### Get Event Types

```
GET /api/event-types
```

Returns list of available event types.

**Response:**

```json
{
  "success": true,
  "data": ["OPEC_Decision", "Geopolitical", "Economic_Shock"]
}
```

### Get Date Range

```
GET /api/date-range
```

Returns available date range in dataset.

**Response:**

```json
{
  "success": true,
  "data": {
    "min_date": "2014-01-02",
    "max_date": "2022-12-30"
  }
}
```

## Setup

### Installation

```bash
cd dashboard/backend
pip install -r requirements.txt
```

### Running the Server

```bash
python app.py
```

Server runs at `http://localhost:5000`

### Testing Endpoints

```bash
# Health check
curl http://localhost:5000/api/health

# Get prices
curl "http://localhost:5000/api/prices?start_date=2018-01-01&end_date=2022-12-31"

# Get events
curl "http://localhost:5000/api/events?event_type=OPEC_Decision"

# Get changepoint
curl http://localhost:5000/api/changepoint
```

## Error Handling

All endpoints return errors in consistent format:

```json
{
  "success": false,
  "error": "Error type",
  "message": "Detailed error message"
}
```

**Status Codes:**

- `200` - Success
- `400` - Bad request (invalid parameters)
- `404` - Endpoint not found
- `500` - Internal server error
