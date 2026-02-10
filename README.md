# Bayesian Oil Market Insights

**Bayesian Change Point Detection for Brent Oil Price Analysis (2014-2022)**

![Python](https://img.shields.io/badge/python-3.11-blue.svg)
![PyMC](https://img.shields.io/badge/PyMC-5.27-orange.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28-red.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

## 🎯 Overview

Probabilistic analysis of Brent oil prices using Bayesian change point detection to identify structural breaks and their association with major geopolitical and economic events. This project provides data-driven insights for investors, policymakers, and energy companies through statistical modeling and interactive visualization.

## 🚀 Quick Start

```bash
# Clone repository
git clone https://github.com/Bekamgenene/bayesian-oil-market-insights.git
cd bayesian-oil-market-insights

# Install dependencies
pip install -r requirements.txt

# Run interactive dashboard
streamlit run dashboard/app.py
```

## 📊 Key Findings

**Detected Change Point:** June 26, 2018 (±1 day uncertainty)

| Metric             | Before     | After      | Change    | Probability   |
| ------------------ | ---------- | ---------- | --------- | ------------- |
| **Mean Return**    | -0.000403  | +0.000909  | +0.001312 | 80% increase  |
| **Volatility (σ)** | 0.021250   | 0.040032   | +0.018782 | 100% increase |
| **Avg Price**      | $63.06/bbl | $69.33/bbl | +9.95%    | —             |

**Interpretation:** Significant regime shift with increased returns and doubled volatility, indicating fundamental market structure change post-mid-2018.

## 📁 Project Structure

```
bayesian-oil-market-insights/
├── data/                               # Datasets
│   ├── BrentOilPrices.csv             # Raw price data (1987-2022)
│   ├── processed_brent_prices_2014_2022.csv
│   ├── structured_events.csv          # 15 major events
│   ├── brent_with_changepoint.csv     # Enhanced with regime indicator
│   └── changepoint_results.json       # Bayesian model outputs
│
├── notebooks/                          # Analysis notebooks
│   ├── task1_exploratory_data_analysis.ipynb
│   └── task2_bayesian_changepoint_analysis.ipynb
│
├── dashboard/                          # Streamlit app
│   ├── app.py                         # Main dashboard (5 pages)
│   ├── requirements.txt
│   └── README.md
│
├── reports/figures/                    # Generated visualizations
│   ├── 01_price_series_with_events.png
│   ├── 04_changepoint_posterior.png
│   ├── 06_changepoint_visualization.png
│   └── dashboard/
│
├── src/                               # Source code
│   └── data_processing.py
│
└── tests/                             # Unit tests
    └── test_data_processing.py
- 2020 Saudi-Russia price war & COVID crash
- 2019 Saudi Aramco attacks
- 2022 Russia-Ukraine invasion
- US-Iran sanctions

### 3. Comprehensive EDA Notebook ✓

**File:** [notebooks/task1_exploratory_data_analysis.ipynb](notebooks/task1_exploratory_data_analysis.ipynb)

**Analysis Includes:**

- ✓ Data loading and preparation (9,013 daily prices)
- ✓ Visual inspection with event annotations
- ✓ Trend analysis (30/90/365-day moving averages)
- ✓ **Stationarity testing (ADF):** Raw prices NON-STATIONARY, Log returns STATIONARY
- ✓ **Volatility analysis:** Strong volatility clustering detected
- ✓ **Distributional analysis:** Heavy tails confirmed (high kurtosis)
- ✓ Autocorrelation analysis (ACF/PACF)
- ✓ Focused analysis on 2014-2022 period

**Key Findings:**

- Price range: $9.10 - $143.95/barrel
- Multiple regime shifts identified
- Log returns suitable for Bayesian modeling
- Must model both mean (μ) and variance (σ) changes

### Summary Document

```

## 🔬 Methodology

### Bayesian Change Point Model

**Model Specification:**

- **Switch Point (τ)**: Discrete uniform prior over time indices
- **Regime Parameters**: Separate means (μ₁, μ₂) and volatilities (σ₁, σ₂)
- **Likelihood**: Normal distribution with switched parameters
- **Inference**: MCMC sampling with PyMC (100 draws, 1 chain)

**Advantages:**

- Probabilistic uncertainty quantification
- No arbitrary threshold selection
- Natural parameter estimation with credible intervals

## 🛠️ Technologies

| Category          | Tools                                |
| ----------------- | ------------------------------------ |
| **Modeling**      | PyMC 5.27, ArviZ 0.23, NumPy, Pandas |
| **Visualization** | Matplotlib, Seaborn, Plotly 5.17     |
| **Dashboard**     | Streamlit 1.28                       |
| **Environment**   | Python 3.11, Jupyter                 |

## 📈 Dashboard Features

Interactive Streamlit application with 5 pages:

1. **Overview**: Key metrics and change point visualization
2. **Price Analysis**: Interactive time series with event markers
3. **Event Analysis**: Timeline of 15 major events (2014-2022)
4. **Statistical Details**: Posterior distributions and regime comparisons
5. **About**: Methodology and project documentation

**Launch:** `streamlit run dashboard/app.py`

## 📊 Analysis Highlights

### Task 1: Exploratory Data Analysis

- 2,258 price observations (2014-2022 focus period)
- 15 structured events (OPEC decisions, geopolitical conflicts, economic shocks)
- Volatility clustering detection
- 6 comprehensive visualizations

### Task 2: Bayesian Change Point Detection

- Single structural break detected: **June 26, 2018**
- Convergence validated (r_hat ≈ 1.0)
- 95% credible intervals for all parameters
- Posterior predictive checks confirm model fit
- 7 statistical visualizations

### Task 3: Interactive Dashboard

- Real-time data filtering (date range, event types)
- 6+ interactive Plotly charts
- Metric cards with key statistics
- Professional UI with custom CSS
- Deployment-ready architecture

## 📁 Key Files

| File                                                                                             | Description                        |
| ------------------------------------------------------------------------------------------------ | ---------------------------------- |
| [task1_exploratory_data_analysis.ipynb](notebooks/task1_exploratory_data_analysis.ipynb)         | Complete EDA with 6 visualizations |
| [task2_bayesian_changepoint_analysis.ipynb](notebooks/task2_bayesian_changepoint_analysis.ipynb) | Bayesian modeling (35 cells)       |
| [dashboard/app.py](dashboard/app.py)                                                             | Streamlit dashboard (700+ lines)   |
| [data/changepoint_results.json](data/changepoint_results.json)                                   | Model outputs and statistics       |
| [data/structured_events.csv](data/structured_events.csv)                                         | Curated event dataset              |

## 🚀 Usage

### Run Analysis Notebooks

```bash
# Activate environment
source .venv/bin/activate  # Windows: .venv\Scripts\Activate.ps1

# Launch Jupyter
jupyter notebook notebooks/

# Run cells in order:
# 1. task1_exploratory_data_analysis.ipynb
# 2. task2_bayesian_changepoint_analysis.ipynb
```

### Launch Dashboard

````bash
streamlit run dashboard/app.py
# Opens at http://localhost:8501

```bash
pip install -r requirements.txt
````

4. **Verify data files**

- ✅ `data/BrentOilPrices.csv` - 9,011 daily prices (May 20, 1987 - Nov 14, 2022)
- ✅ `data/major_oil_events.csv` - 16 major events (2014-2022)

````

## 🧪 Testing

```bash
# Run unit tests
pytest tests/

# Test coverage
pytest --cov=src tests/
````

## 📊 Results & Insights

### Statistical Significance

- **Change Point Certainty**: ±1 day uncertainty (highly precise)
- **Mean Shift**: 80% posterior probability of positive shift
- **Volatility Shift**: 100% posterior probability of increase
- **Model Convergence**: All parameters r_hat ≈ 1.0 (excellent)

### Business Implications

1. **Risk Management**: Volatility doubled post-2018, requiring adjusted hedging strategies
2. **Investment Timing**: Regime shift suggests fundamental market structure change
3. **Policy Context**: No single event within ±60 days, indicating systemic transition

### Limitations

- Single change point model (may oversimplify complex dynamics)
- Association ≠ causation (temporal correlation only)
- External factors not modeled (inventory, USD strength, macroeconomic conditions)

## 📈 Visualization Gallery

**Task 1 (EDA - 6 Figures)**

- Price series with events
- Moving averages and volatility
- Log returns analysis
- Autocorrelation patterns

**Task 2 (Bayesian - 7 Figures)**

- Trace plots (MCMC diagnostics)
- Changepoint posterior distribution
- Parameter posteriors (before/after comparison)
- Change point visualization on price series
- Posterior predictive checks

**Task 3 (Dashboard - 6+ Charts)**

- Interactive price chart with event markers
- Log returns with regime means
- Event timeline
- Regime comparison tables
- Probability distributions

## 🔗 Resources

**Documentation:**

- [Dashboard User Guide](dashboard/README.md)
- [Bayesian Quick Reference](documents/Bayesian_Change_Point_Quick_Reference.md)

**Notebooks:**

- [Task 1: EDA](notebooks/task1_exploratory_data_analysis.ipynb)
- [Task 2: Bayesian Analysis](notebooks/task2_bayesian_changepoint_analysis.ipynb)

**Data Sources:**

- U.S. Energy Information Administration (EIA)
- OPEC Monthly Oil Market Reports
- Reuters, Bloomberg (event data)

## 👥 Credits

**Developer:** Bekam Genene  
**Organization:** Birhan Energies  
**Program:** 10 Academy AI Mastery - Week 11  
**Tutors:** Kerod, Filimon, Mahbubah

## 📄 License

MIT License - See [LICENSE](LICENSE) file

## 📧 Contact

**GitHub:** [@Bekamgenene](https://github.com/Bekamgenene)  
**Repository:** [bayesian-oil-market-insights](https://github.com/Bekamgenene/bayesian-oil-market-insights)

---

⭐ **Star this repo** if you find it useful for Bayesian time series analysis!

_Last Updated: February 10, 2026_
