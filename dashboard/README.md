# Task 3: Interactive Dashboard

## 🎯 Overview

This interactive Streamlit dashboard visualizes the results of the Bayesian change point analysis on Brent oil prices (2014-2022). It provides stakeholders with an intuitive interface to explore structural breaks, regime shifts, and event associations.

## 📊 Features

### 1. **Overview Page**

- Executive summary with key metrics
- Interactive price chart with change point visualization
- Event timeline with clickable markers
- Regime shift statistics

### 2. **Price Analysis**

- Detailed price series visualization
- Log returns analysis with regime means
- Return distribution histograms
- Summary statistics (before/after comparison)

### 3. **Event Analysis**

- Interactive event timeline
- Event breakdown by type (OPEC, Geopolitical, Economic)
- Closest events to detected change point
- Full event table with temporal distances

### 4. **Statistical Details**

- Model specification and assumptions
- Posterior parameter estimates
- Probabilistic statements with credible intervals
- Limitations and future enhancements

### 5. **About**

- Project background and methodology
- Stakeholder value propositions
- Technology stack
- Contact information

## 🚀 Quick Start

### Prerequisites

Ensure Task 2 notebook has been executed to generate required data files:

- `data/brent_with_changepoint.csv`
- `data/structured_events.csv`
- `data/changepoint_results.json`

### Installation

1. **Navigate to dashboard directory:**

```bash
cd dashboard
```

2. **Install dependencies:**

```bash
pip install -r requirements.txt
```

### Running the Dashboard

**Option 1: From dashboard directory**

```bash
streamlit run app.py
```

**Option 2: From project root**

```bash
streamlit run dashboard/app.py
```

The dashboard will open automatically in your browser at `http://localhost:8501`

## 📁 File Structure

```
dashboard/
├── app.py                 # Main Streamlit application
├── requirements.txt       # Dashboard dependencies
└── README.md             # This file
```

## 🎨 Dashboard Pages

### Navigation

Use the sidebar radio buttons to navigate between pages:

- **Overview** - Executive summary and key visualizations
- **Price Analysis** - Detailed price and returns analysis
- **Event Analysis** - Event timeline and impact assessment
- **Statistical Details** - Model specification and results
- **About** - Project information and methodology

### Filters

The sidebar provides interactive filters:

- **Date Range:** Adjust analysis window
- **Event Types:** Select which event categories to display

## 📈 Visualizations

All charts are interactive (powered by Plotly):

- **Hover** over data points for details
- **Zoom** by clicking and dragging
- **Pan** by holding shift and dragging
- **Reset** view with double-click
- **Download** as PNG using camera icon

## 🎯 Stakeholder Use Cases

### For Investors 📊

- Identify optimal entry/exit points based on regime shifts
- Quantify risk through volatility changes
- Track historical event impacts for pattern recognition

### For Policymakers 🏛️

- Assess market responses to policy interventions
- Understand structural break timing and magnitude
- Plan strategic reserves and regulations

### For Energy Companies ⚡

- Optimize hedging strategies around detected breaks
- Forecast price trends in different regimes
- Align operational planning with market dynamics

## 🔧 Customization

### Modify Visualizations

Edit the following functions in `app.py`:

- `create_price_chart()` - Price series visualization
- `create_returns_chart()` - Log returns analysis
- `create_event_timeline()` - Event timeline
- `create_impact_metrics()` - Metric cards

### Add New Pages

1. Add page option in sidebar radio button
2. Create corresponding `elif` block in main()
3. Implement page content with Streamlit components

### Update Styling

Modify the CSS in the `st.markdown()` block at the top of `app.py`

## 📊 Data Sources

The dashboard loads data from:

```python
DATA_DIR = Path(__file__).parent.parent / "data"
REPORTS_DIR = Path(__file__).parent.parent / "reports" / "figures"
```

Required files:

- `brent_with_changepoint.csv` - Price data with regime indicator
- `structured_events.csv` - Curated event dataset
- `changepoint_results.json` - Bayesian analysis results

## 🐛 Troubleshooting

### Dashboard won't start

**Issue:** `FileNotFoundError` for data files  
**Solution:** Run Task 2 notebook completely to generate required files

### Charts not displaying

**Issue:** Plotly charts show blank  
**Solution:** Ensure `plotly>=5.17.0` is installed: `pip install --upgrade plotly`

### Slow performance

**Issue:** Dashboard loads slowly  
**Solution:** Data is cached with `@st.cache_data` - clear cache with 'c' key in browser

### Port already in use

**Issue:** Error: "Port 8501 is in use"  
**Solution:** Specify different port: `streamlit run app.py --server.port 8502`

## 🚀 Deployment

### Streamlit Cloud (Recommended)

1. **Push to GitHub:**

```bash
git add dashboard/
git commit -m "Add Task 3 dashboard"
git push origin task-2
```

2. **Deploy on Streamlit Cloud:**

- Visit [share.streamlit.io](https://share.streamlit.io)
- Connect your GitHub repository
- Select `dashboard/app.py` as main file
- Click "Deploy"

3. **Environment Variables:**
   No secrets required for this dashboard

### Alternative: Local Server

```bash
# Run with custom configuration
streamlit run dashboard/app.py \
  --server.port 8080 \
  --server.headless true \
  --server.enableCORS false
```

## 📝 Technical Details

**Framework:** Streamlit 1.28+  
**Visualization:** Plotly 5.17+  
**Data Processing:** Pandas 2.0+  
**Layout:** Wide mode with expandable sidebar  
**Caching:** Data loaded once per session  
**Responsiveness:** Adapts to screen size automatically

## 🎓 Educational Value

This dashboard demonstrates:

- **Bayesian Inference:** Change point detection with uncertainty quantification
- **Time Series Analysis:** Structural breaks and regime shifts
- **Event Studies:** Association analysis (with causality caveats)
- **Interactive Visualization:** Plotly charts with Streamlit
- **Data Science Communication:** Translating technical results for stakeholders

## 📖 Further Reading

- [Streamlit Documentation](https://docs.streamlit.io)
- [Plotly Python](https://plotly.com/python/)
- [PyMC Tutorials](https://www.pymc.io/welcome.html)
- [ArviZ Documentation](https://python.arviz.org/)

## ⚠️ Disclaimer

This dashboard presents statistical associations between events and price changes. These associations **do not imply causation**. Investment and policy decisions should incorporate additional analysis, domain expertise, and risk assessment.

## 📞 Support

For issues or questions:

- **GitHub Issues:** [Report bugs](https://github.com/Bekamgenene/bayesian-oil-market-insights/issues)
- **Documentation:** See main project README.md
- **Data:** Review notebooks/ for analysis workflow

---

**Built with ❤️ using Streamlit | © 2026 Birhan Energies**
