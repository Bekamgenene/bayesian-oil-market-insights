# Bayesian Oil Market Insights

### Change Point Analysis and Statistical Modeling of Brent Oil Prices

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![PyMC](https://img.shields.io/badge/PyMC-5.0+-orange.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

## 🎯 Project Overview

This project analyzes how major political and economic events affect Brent oil prices using **Bayesian Change Point Detection**. As a data scientist at **Birhan Energies**, we aim to provide data-driven insights to investors, policymakers, and energy companies navigating the complex global oil market.

### Business Objectives

- 🔍 Identify key events that significantly impacted Brent oil prices (1987-2022)
- 📊 Quantify the magnitude of price changes using Bayesian statistical methods
- 💡 Provide actionable insights for investment strategies, policy development, and operational planning
- 📈 Build an interactive dashboard for stakeholder exploration of results

---

## 📁 Project Structure

```
bayesian-oil-market-insights/
│
├── data/                          # Data files
│   ├── major_oil_events.csv       # Compiled geopolitical events (16 major events, 2014-2022)
│   └── BrentOilPrices.csv         # Historical price data (May 1987 - Sep 2022, 9,013 daily prices)
│
├── notebooks/                     # Jupyter notebooks for analysis
│   └── task1_exploratory_data_analysis.ipynb  # Task 1: Comprehensive EDA
│
├── src/                          # Source code
│   ├── __init__.py               # Package initialization
│   ├── data_processing.py        # ✅ Data loading and preprocessing utilities
│   ├── bayesian_models.py        # PyMC model definitions (Task 2)
│   └── visualization.py          # Plotting utilities (Task 2)
│
├── tests/                        # Unit tests
│   ├── __init__.py
│   └── test_data_processing.py   # ✅ Comprehensive unit tests
│
├── reports/                      # Generated reports and figures
│   ├── figures/                  # All visualization outputs (auto-generated)
│   └── README.md                 # Report documentation
│
├── dashboard/                    # Interactive dashboard (Task 3)
│   ├── backend/                  # Flask API
│   └── frontend/                 # React application
│
├── .github/                      # GitHub Actions workflows
│   └── workflows/
│       ├── ci.yml                # ✅ CI/CD pipeline
│       ├── data-validation.yml   # ✅ Data validation
│       └── notebook-check.yml    # ✅ Notebook quality checks
│
├── documents/                    # Documentation and reports
│
├── pytest.ini                    # ✅ Pytest configuration
├── TESTING.md                    # ✅ Testing guide
├── Task1_Analysis_Plan.md        # ✅ Task 1: Complete analysis workflow (2 pages)
├── TASK1_INTERIM_SUBMISSION.md   # ✅ Task 1: Interim submission summary
├── README.md                     # This file
└── requirements.txt              # Python dependencies
```

---

## ✅ Task 1: Completed Deliverables (Interim Submission)

### 1. Analysis Workflow Document (1-2 pages) ✓

**File:** [Task1_Analysis_Plan.md](Task1_Analysis_Plan.md)

**Includes:**

- Complete 6-step data analysis workflow with EDA findings
- Change point model explanation and Bayesian approach justification
- Time series properties analysis (trend, stationarity, volatility)
- Expected outputs and model limitations
- **Critical discussion on correlation vs. causation**
- Assumptions, limitations, and communication strategy

### 2. Event Dataset (CSV) ✓

**File:** [data/major_oil_events.csv](data/major_oil_events.csv)

**Contains:**

- **16 major events** (2014-2022) covering:
  - OPEC Policy Decisions (6 events)
  - Geopolitical Conflicts (5 events)
  - Economic Sanctions (2 events)
  - Market Volatility (2 events)
  - Government Policy (2 events)

**Key Events:**

- 2014 OPEC production decision
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

**File:** [TASK1_INTERIM_SUBMISSION.md](TASK1_INTERIM_SUBMISSION.md) - Complete overview of all Task 1 deliverables

---

## 🔬 Methodology

### 1. Bayesian Change Point Detection

We employ a **Bayesian approach** using PyMC to:

- Identify structural breaks in oil price time series
- Estimate uncertainty in change point locations
- Quantify before/after parameter shifts (mean, volatility)

### 2. Event Association Analysis

- Compare detected change points with compiled event timeline
- Formulate hypotheses about causal mechanisms
- Acknowledge correlation vs. causation limitations

### 3. Time Series Property Analysis

- **Trend Analysis**: Long-term directional movements
- **Stationarity Testing**: ADF and KPSS tests
- **Volatility Patterns**: GARCH-style variance clustering

---

## 📊 Dataset Summary

### Historical Price Data

**File:** [data/BrentOilPrices.csv](data/BrentOilPrices.csv)

- **Records:** 9,011 daily prices
- **Period:** May 20, 1987 - November 14, 2022 (35+ years)
- **Price Range:** ~$9 to ~$147 per barrel
- **Format:** Date, Price (USD/barrel)

### Major Events Dataset (2014-2022)

**File:** [data/major_oil_events.csv](data/major_oil_events.csv)

Our research identified **16 critical events** across four categories:

| Category                   | Count | Examples                                                                             |
| -------------------------- | ----- | ------------------------------------------------------------------------------------ |
| **Geopolitical Conflicts** | 4     | ISIL Iraq Offensive (2014), Saudi Aramco Attack (2019), Russia-Ukraine War (2022)    |
| **OPEC Policy**            | 6     | Production cuts (2016), Saudi-Russia price war (2020), Historic COVID-19 cuts (2020) |
| **Economic Sanctions**     | 1     | US Iran sanctions (2018)                                                             |
| **Market Volatility**      | 5     | Negative oil prices (2020), Price peaks (2018, 2022)                                 |

---

## 🛠️ Technologies Used

### Analysis & Modeling

- **Python 3.8+**: Core programming language
- **PyMC**: Bayesian inference and MCMC sampling
- **Pandas & NumPy**: Data manipulation
- **Matplotlib, Seaborn, Plotly**: Visualization
- **Statsmodels**: Time series analysis (ADF test, ACF/PACF)

### Dashboard Development

- **Backend**: Flask (REST API)
- **Frontend**: React.js
- **Charts**: Recharts / React Chart.js 2
- **Deployment**: TBD

---

## 🚀 Getting Started

### Prerequisites

```bash
Python 3.8 or higher
pip package manager
Git
```

### Installation

1. **Clone the repository**

```bash
git clone https://github.com/Bekamgenene/bayesian-oil-market-insights.git
cd bayesian-oil-market-insights
```

2. **Create virtual environment** (recommended)

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies** (after requirements.txt is created)

```bash
pip install -r requirements.txt
```

4. **Verify data files**

- ✅ `data/BrentOilPrices.csv` - 9,011 daily prices (May 20, 1987 - Nov 14, 2022)
- ✅ `data/major_oil_events.csv` - 16 major events (2014-2022)

### Running the Analysis

```bash
# Launch Jupyter Notebook
jupyter notebook

# Navigate to notebooks/ folder and run in sequence:
# 1. 01_EDA.ipynb
# 2. 02_Bayesian_Change_Point.ipynb
# 3. 03_Event_Association.ipynb
```

---

## 📈 Key Findings (To Be Updated)

_This section will be populated after completing Task 2 analysis_

### Detected Change Points

- TBD

### Quantified Impacts

- TBD

### Event Associations

- TBD

---

## 📝 Documentation

- **Task 1 Analysis Plan**: [Task1_Analysis_Plan.md](Task1_Analysis_Plan.md)
  - Analysis workflow (6 phases)
  - Change point model explanation
  - Assumptions and limitations
  - Communication strategy
  - Event dataset overview

---

## 🎓 Learning Outcomes

This project develops expertise in:

- ✅ **Change Point Analysis & Interpretation**
- ✅ **Bayesian Inference** (PyMC framework)
- ✅ **Monte Carlo Markov Chain (MCMC)** methods
- ✅ **Statistical Reasoning** and model comparison
- ✅ **Analytical Storytelling** with data
- ✅ **Policy Analysis** communication

---

## 📅 Project Timeline

| Phase                             | Dates         | Status            |
| --------------------------------- | ------------- | ----------------- |
| **Task 1**: Foundation & Planning | Feb 4-5, 2026 | ✅ Completed      |
| **Task 2**: Bayesian Modeling     | Feb 6-7, 2026 | 🚀 Ready to Start |
| **Task 3**: Dashboard Development | Feb 8-9, 2026 | ⏳ Pending        |
| **Final Report & Submission**     | Feb 10, 2026  | ⏳ Pending        |

---

## 👥 Team & Support

**Organization**: Birhan Energies  
**Program**: 10 Academy - AI Mastery Week 11

**Tutors**:

- Kerod
- Filimon
- Mahbubah

**Communication**:

- Slack: `#all-week11`
- Office Hours: Mon–Fri, 08:00–15:00 UTC

---

## ⚠️ Important Notes

### Correlation vs. Causation

This analysis identifies **temporal correlations** between events and price changes. While we propose plausible causal mechanisms using economic reasoning, we **cannot definitively prove causation** due to:

- Confounding factors
- Omitted variables
- Reverse causality
- Potential spurious correlations

All findings are presented as "consistent with" or "suggestive of" rather than "proves."

### Model Limitations

- Assumes normal distribution of returns
- Single change point in basic model (can be extended)
- Instantaneous parameter shifts
- Daily data frequency may miss intraday dynamics

---

## 📚 References

### Change Point Analysis

- [Bayesian Changepoint Detection with PyMC](https://www.pymc.io/)
- [Change Point Detection in Time Series](https://forecastegy.com/posts/change-point-detection-time-series-python/)

### Bayesian Methods

- [MCMC Explained](https://towardsdatascience.com/monte-carlo-markov-chain-mcmc-explained-94e3a6c8de11)
- Steel, M. F. J. "Bayesian Time Series Analysis"

### Oil Market Data

- [EIA - Brent Crude Oil Prices](https://www.eia.gov/)
- [OPEC Monthly Oil Market Reports](https://www.opec.org/)

---

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

## 🤝 Contributing

This is an educational project for 10 Academy's AI Mastery program. Contributions, suggestions, and feedback are welcome!

---

## 📧 Contact

**Developer**: Bekam Genene  
**GitHub**: [@Bekamgenene](https://github.com/Bekamgenene)  
**Project Repository**: [bayesian-oil-market-insights](https://github.com/Bekamgenene/bayesian-oil-market-insights)

---

_Last Updated: February 5, 2026_
