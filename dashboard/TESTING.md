# Dashboard Testing Guide

Quick reference for testing the Flask + React dashboard.

## ✅ Pre-requisites Checklist

- [ ] Python 3.8+ installed
- [ ] Node.js 14+ and npm installed
- [ ] Data files generated (run notebooks if missing):
  - `data/brent_with_changepoint.csv`
  - `data/structured_events.csv`
  - `data/changepoint_results.json`

## 🚀 Quick Start (Development Mode)

### Terminal 1: Backend

```bash
cd dashboard/backend
pip install -r requirements.txt
python app.py
```

**Expected output:**

```
 * Running on http://127.0.0.1:5000
 * Data loaded successfully
```

### Terminal 2: Frontend

```bash
cd dashboard/frontend
npm install
npm start
```

**Expected output:**

```
Compiled successfully!
Local:            http://localhost:3000
```

## 🧪 Testing Steps

### 1. Backend API Tests

Test each endpoint with curl or browser:

```bash
# Health check
curl http://localhost:5000/api/health

# Changepoint data
curl http://localhost:5000/api/changepoint

# All prices
curl http://localhost:5000/api/prices

# Filtered prices (2018-2020)
curl "http://localhost:5000/api/prices?start_date=2018-01-01&end_date=2020-12-31"

# All events
curl http://localhost:5000/api/events

# Filtered events (OPEC only)
curl "http://localhost:5000/api/events?event_type=OPEC_Decision"

# Statistics
curl http://localhost:5000/api/statistics

# Date range
curl http://localhost:5000/api/date-range

# Event types
curl http://localhost:5000/api/event-types
```

**All endpoints should return JSON with `success: true`**

### 2. Frontend UI Tests

Visit http://localhost:3000 and test:

#### Overview Tab

- [ ] Metric cards display changepoint date, mean shift, volatility shift, price impact
- [ ] Price chart renders with blue line
- [ ] Red changepoint line appears on chart
- [ ] Insight box shows interpretation text

#### Price Analysis Tab

- [ ] Detailed price chart displays
- [ ] Changepoint marker visible
- [ ] Regime comparison section shows before/after stats
- [ ] Chart is responsive

#### Events Tab

- [ ] Event timeline/scatter chart displays
- [ ] Event table shows all events with dates, types, descriptions
- [ ] Event badges have colors (green=OPEC, red=Geopolitical, orange=Economic)
- [ ] Table is scrollable

#### Statistics Tab

- [ ] All 8 metric cards display (changepoint, mean shift, volatility shift, price impact, before/after prices, before/after volatilities)
- [ ] Values match Bayesian results
- [ ] Warning box about limitations displays

#### Sidebar Filters

- [ ] Date pickers open and allow selection
- [ ] Start/End date filtering works
- [ ] Event type checkboxes toggle
- [ ] "Reset Filters" button clears all filters
- [ ] Filter info shows active filters

### 3. Data Filtering Tests

Test that filters actually change the data:

1. **No filters**: Note the number of data points
2. **Date filter (2018-2020)**: Click Overview → Sidebar → Set start: 2018-01-01, end: 2020-12-31 → Data should reduce
3. **Event filter**: Events tab → Check only "OPEC_Decision" → Only OPEC events show in table
4. **Reset**: Click "Reset Filters" → All data returns

### 4. Responsive Design Tests

Test at different screen sizes:

- [ ] Desktop (1920x1080): Sidebar on left, main content on right
- [ ] Tablet (768px): Sidebar above content
- [ ] Mobile (375px): Single column, charts fit width

Use browser DevTools (F12) → Device toolbar to test.

### 5. Error Handling Tests

#### Backend Errors

1. Stop Flask server → Frontend should show error message
2. Restart Flask → Frontend should recover

#### Invalid Filters

1. Set end date before start date → Should handle gracefully
2. Set dates outside dataset range → Should return empty data or error

#### CORS Test

Open browser console (F12) → Network tab → Look for CORS errors (should be none)

### 6. Performance Tests

- [ ] Initial page load < 3 seconds
- [ ] Filter changes update data < 1 second
- [ ] Charts render smoothly without lag
- [ ] No console errors in browser DevTools

## 🐛 Common Issues

| Issue                 | Solution                                                                 |
| --------------------- | ------------------------------------------------------------------------ |
| Backend won't start   | Check if port 5000 is in use: `netstat -ano \| findstr :5000`            |
| Frontend won't start  | Check if port 3000 is in use, clear npm cache: `npm cache clean --force` |
| CORS errors           | Ensure `flask-cors` is installed: `pip install flask-cors`               |
| "Cannot GET /api/..." | Backend not running or wrong URL                                         |
| Blank page            | Check browser console for errors, ensure backend is running              |
| Charts don't display  | Check data files exist, backend returns data, Recharts installed         |

## 📸 Screenshots

Take screenshots for documentation:

1. **Overview tab** - Full page with metric cards and chart
2. **Price Analysis tab** - Detailed chart with changepoint
3. **Events tab** - Timeline and event table
4. **Statistics tab** - All metric cards
5. **Mobile view** - Responsive design on small screen

Save to: `reports/figures/dashboard/`

Naming convention:

- `dashboard_overview.png`
- `dashboard_price_analysis.png`
- `dashboard_events.png`
- `dashboard_statistics.png`
- `dashboard_mobile.png`

## ✅ Test Results Template

```
DASHBOARD TEST RESULTS
======================

Date: ___________
Tester: _________

Backend Tests:
[ ] All 7 API endpoints return success
[ ] Filtering works (date & event type)
[ ] Error handling for invalid requests

Frontend Tests:
[ ] All 4 tabs render correctly
[ ] Metric cards display accurate data
[ ] Charts visualize data properly
[ ] Event table shows all events
[ ] Tooltips work on hover

Filter Tests:
[ ] Date filtering updates data
[ ] Event type filtering updates data
[ ] Reset button clears filters
[ ] Filter info shows active filters

Responsive Tests:
[ ] Desktop layout correct
[ ] Tablet layout adapts
[ ] Mobile layout readable

Performance:
[ ] Page loads < 3 seconds
[ ] Filters update < 1 second
[ ] No lag or freezing

Issues Found:
1. _______________
2. _______________

Overall Status: [ ] PASS  [ ] FAIL
```

## 🚀 Next Steps After Testing

1. Document any issues found
2. Take screenshots for README
3. Update documentation with any changes
4. Prepare for production deployment
5. Create deployment guide

## 📞 Support

If tests fail, check:

1. [dashboard/SETUP.md](SETUP.md) - Setup instructions
2. [dashboard/backend/README.md](backend/README.md) - API documentation
3. Browser console (F12) for JavaScript errors
4. Flask terminal for Python errors
5. Network tab in DevTools for API call failures

Happy testing! 🎉
