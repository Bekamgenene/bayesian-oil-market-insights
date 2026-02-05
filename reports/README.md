# Reports Directory

This directory contains generated reports and visualizations from the analysis.

## Structure

```
reports/
├── figures/              # All visualization outputs
│   ├── 01_brent_oil_prices_full_series.png
│   ├── 02_moving_averages.png
│   ├── 03_log_returns_analysis.png
│   ├── 04_volatility_analysis.png
│   ├── 05_autocorrelation.png
│   └── 06_focus_period_2014_2022.png
└── README.md             # This file
```

## Generated Figures

All figures are automatically generated when running the Jupyter notebooks:

### Task 1: Exploratory Data Analysis

- **01_brent_oil_prices_full_series.png**: Full historical price series (1987-2022) with major events
- **02_moving_averages.png**: Price trends with 30/90/365-day moving averages
- **03_log_returns_analysis.png**: Log returns time series and distribution
- **04_volatility_analysis.png**: Rolling volatility analysis (30/90-day windows)
- **05_autocorrelation.png**: ACF and PACF plots for log returns
- **06_focus_period_2014_2022.png**: Recent period (2014-2022) with event annotations

### Figure Specifications

- **Format**: PNG
- **Resolution**: 300 DPI (publication quality)
- **Size**: Optimized for reports and presentations
- **Naming**: Sequential numbering with descriptive names

## Usage

Figures are automatically saved when running:

```bash
jupyter notebook notebooks/task1_exploratory_data_analysis.ipynb
```

All figures are saved to `reports/figures/` directory.

## Note

Generated figure files (_.png, _.jpg, \*.pdf) are excluded from git version control via `.gitignore` to keep repository size small. Run the notebooks to regenerate them.
