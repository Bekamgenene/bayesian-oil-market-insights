# Dashboard Setup Guide

This guide provides step-by-step instructions for setting up and running the Bayesian Oil Market Insights dashboard with Flask backend and React frontend.

## Architecture Overview

The dashboard follows a modern client-server architecture:

- **Backend**: Flask REST API (Python)
- **Frontend**: React single-page application (JavaScript)
- **Data Flow**: CSV files → Flask → JSON API → React → Recharts visualization

## Prerequisites

- Python 3.8+ (with pip)
- Node.js 14+ and npm
- Git (optional, for version control)

## Backend Setup

### 1. Navigate to Backend Directory

```bash
cd dashboard/backend
```

### 2. Create Python Virtual Environment (Recommended)

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

Required packages:

- Flask==3.0.0
- flask-cors==4.0.0
- pandas==2.0.0
- numpy==1.24.0

### 4. Verify Data Files

Ensure the following files exist in `data/` directory:

- `brent_with_changepoint.csv` (price data with changepoint indicator)
- `structured_events.csv` (major oil market events)
- `changepoint_results.json` (Bayesian analysis results)

If missing, run the Jupyter notebooks in `notebooks/` to generate them.

### 5. Start Flask Server

```bash
python app.py
```

The backend will start on **http://localhost:5000**

You should see:

```
 * Running on http://127.0.0.1:5000
 * Press CTRL+C to quit
```

### 6. Test API Endpoints

Open a browser or use curl to test:

```bash
# Health check
curl http://localhost:5000/api/health

# Get changepoint data
curl http://localhost:5000/api/changepoint

# Get price data
curl http://localhost:5000/api/prices
```

## Frontend Setup

### 1. Navigate to Frontend Directory

Open a **new terminal** (keep Flask running in the first terminal):

```bash
cd dashboard/frontend
```

### 2. Install Node Dependencies

```bash
npm install
```

This installs:

- react, react-dom (UI framework)
- recharts (charting library)
- axios (HTTP client)
- react-datepicker (date filtering)
- date-fns (date utilities)

### 3. Start React Development Server

```bash
npm start
```

The frontend will start on **http://localhost:3000** and automatically open in your browser.

The React app is configured to proxy API calls to `http://localhost:5000`.

## Running the Full Application

### Option 1: Two Terminal Windows

**Terminal 1 (Backend):**

```bash
cd dashboard/backend
python app.py
```

**Terminal 2 (Frontend):**

```bash
cd dashboard/frontend
npm start
```

### Option 2: Using PowerShell Script (Windows)

Create `start-dashboard.ps1`:

```powershell
# Start Flask backend
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd dashboard/backend; python app.py"

# Wait for backend to start
Start-Sleep -Seconds 3

# Start React frontend
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd dashboard/frontend; npm start"
```

Run:

```bash
.\start-dashboard.ps1
```

## Accessing the Dashboard

Once both servers are running:

1. **Frontend UI**: http://localhost:3000
2. **Backend API**: http://localhost:5000/api

The dashboard has 4 tabs:

- **Overview**: Key metrics and price chart with changepoint
- **Price Analysis**: Detailed price trends with regime comparison
- **Events**: Event timeline and table with filtering
- **Statistics**: Summary statistics and model parameters

## Features

### Date Filtering

Use the sidebar to filter data by:

- Start date
- End date
- Event types (OPEC, Geopolitical, Economic)

### Interactive Charts

- Hover over data points for details
- Changepoint marked with red line
- Event markers on timeline
- Responsive design for mobile/tablet

### API Integration

All data is fetched dynamically from the Flask API:

- Real-time filtering via query parameters
- Error handling with user-friendly messages
- Loading states during data fetch

## Troubleshooting

### Backend Issues

**Port 5000 already in use:**

```bash
# Windows: Find and kill process on port 5000
netstat -ano | findstr :5000
taskkill /PID <PID> /F

# macOS/Linux
lsof -ti:5000 | xargs kill -9
```

**Import errors:**

```bash
# Ensure virtual environment is activated
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

**Data files not found:**

```bash
# Check data directory exists
ls ../data/

# Run notebooks to generate data
cd ../../notebooks
jupyter notebook
# Run task1 and task2 notebooks
```

### Frontend Issues

**npm install fails:**

```bash
# Clear npm cache
npm cache clean --force

# Delete node_modules and package-lock.json
rm -rf node_modules package-lock.json

# Reinstall
npm install
```

**Port 3000 already in use:**

```bash
# Windows
netstat -ano | findstr :3000
taskkill /PID <PID> /F

# macOS/Linux
lsof -ti:3000 | xargs kill -9

# Or set different port
set PORT=3001 && npm start
```

**CORS errors:**
Ensure Flask server is running and `flask-cors` is installed:

```bash
pip install flask-cors
```

**Blank page or errors:**
Check browser console (F12) for errors. Common issues:

- Backend not running (check http://localhost:5000/api/health)
- Incorrect API URLs (check `src/services/api.js`)
- Missing dependencies (run `npm install`)

### Network Issues

**Backend and frontend on different machines:**

Update `dashboard/frontend/src/services/api.js`:

```javascript
const API_BASE_URL =
  process.env.REACT_APP_API_URL || "http://<backend-ip>:5000/api";
```

Or set environment variable:

```bash
# Windows
set REACT_APP_API_URL=http://192.168.1.100:5000/api
npm start

# macOS/Linux
REACT_APP_API_URL=http://192.168.1.100:5000/api npm start
```

## Production Deployment

### Build React App

```bash
cd dashboard/frontend
npm run build
```

This creates an optimized production build in `build/` directory.

### Serve with Flask

Update Flask to serve React build:

```python
# dashboard/backend/app.py
from flask import send_from_directory

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve_react(path):
    if path and os.path.exists(os.path.join('../frontend/build', path)):
        return send_from_directory('../frontend/build', path)
    return send_from_directory('../frontend/build', 'index.html')
```

Run Flask only:

```bash
python app.py
```

Access at http://localhost:5000

### Deploy to Cloud

**Options:**

1. **Heroku**: Deploy Flask + React build
2. **AWS**: EC2 for Flask, S3 + CloudFront for React
3. **Azure**: App Service for Flask, Static Web Apps for React
4. **Google Cloud**: App Engine for Flask, Cloud Storage for React

See `DEPLOYMENT.md` for detailed cloud deployment instructions.

## API Documentation

Full API documentation available in `dashboard/backend/README.md`

**Available Endpoints:**

- `GET /api/health` - Server health check
- `GET /api/prices` - Price data with filtering
- `GET /api/events` - Events with filtering
- `GET /api/changepoint` - Bayesian changepoint results
- `GET /api/statistics` - Summary statistics
- `GET /api/event-types` - Available event categories
- `GET /api/date-range` - Dataset date boundaries

## Development Workflow

1. **Make changes to Flask API**: Edit `dashboard/backend/app.py`, Flask auto-reloads
2. **Make changes to React**: Edit files in `dashboard/frontend/src/`, React auto-reloads
3. **Add new endpoints**: Update `app.py` and `api.js`
4. **Add new components**: Create in `src/components/`, import in `App.js`
5. **Test changes**: Both servers support hot-reloading during development

## Next Steps

- Run Jupyter notebooks to ensure data files are generated
- Start both backend and frontend servers
- Test all features and filtering
- Take screenshots for documentation
- Deploy to production environment

For questions or issues, refer to the main `README.md` or create an issue in the repository.
