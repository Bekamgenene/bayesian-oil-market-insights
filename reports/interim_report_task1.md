# Interim Report — Task 1 (Concise)

## 1. Objective (6 pts)

Task 1 focus: perform exploratory data analysis (EDA) on Brent crude prices (2014–2022), assemble an initial event dataset, and demonstrate that a Bayesian change-point approach is an appropriate next-step for detecting structural shifts related to major political/economic events.

Stakeholder alignment:

- Investors: early signals of regime and volatility changes to inform timing and hedging.
- Policymakers: initial evidence on market responses to policy/supply shocks.
- Energy companies: operational implications from identified volatility regimes.

Why Bayesian change-point detection: it yields posterior distributions over change-point dates and regime parameters (means/volatilities), providing principled uncertainty quantification needed for decision-making.

## 2. Completed work & initial analysis (6 pts)

Workflow performed (Task 1 scope):

- Data ingestion & cleaning: loaded `data/BrentOilPrices.csv` and applied resampling/cleaning via `src/data_processing.py`. Generated `data/processed_brent_prices_2014_2022.csv` for EDA.
- Event dataset creation: compiled and structured 15 key events in `data/structured_events.csv` with Date, Event_Type (OPEC_Decision, Geopolitical, Economic_Shock), Description, and Expected_Impact columns.
- Exploratory analysis: plotted levels, log-returns, autocorrelation, and rolling volatility to summarize trend and heteroskedasticity.
- Event mapping (initial): mapped events from `structured_events.csv` to the price series for preliminary tagging and impact assessment.
- Initial model test: fitted a prototype Bayesian change-point model on log-prices/returns to verify detectability of clear historical breaks (e.g., 2014–2016 decline, 2020 pandemic shock, 2022 supply shock).

Structured event dataset (15 items in `data/structured_events.csv`):

1. 2014-11-27 — OPEC_Decision: OPEC decides not to cut production despite falling prices
2. 2015-01-15 — Economic_Shock: Continued global oversupply and China growth concerns
3. 2016-11-30 — OPEC_Decision: OPEC agrees to cut production by 1.2M bpd
4. 2018-05-08 — Geopolitical: U.S. withdraws from Iran nuclear deal; sanctions risk
5. 2019-09-14 — Geopolitical: Attacks on Saudi Aramco facilities (5.7M bpd offline)
6. 2020-03-06 — OPEC_Decision: Russia-Saudi price war begins; OPEC+ fails to agree
7. 2020-03-11 — Economic_Shock: COVID-19 declared pandemic; demand collapse
8. 2020-04-12 — OPEC_Decision: OPEC+ agrees to historic cuts of 9.7M bpd
9. 2020-04-20 — Economic_Shock: WTI futures go negative; storage capacity concerns
10. 2021-07-01 — Economic_Shock: Demand recovery amid Delta variant concerns
11. 2021-11-04 — OPEC_Decision: OPEC+ maintains gradual production increase
12. 2022-02-24 — Geopolitical: Russia invades Ukraine; major supply risk
13. 2022-03-08 — Geopolitical: U.S. and EU ban Russian oil imports
14. 2022-06-02 — OPEC_Decision: OPEC+ accelerates production increases
15. 2022-10-05 — OPEC_Decision: OPEC+ announces 2M bpd production cut

Preliminary time-series summary:

- Trend: clear non-linear multi-year movements (2014–2016 decline, 2016–2018 recovery, 2020 collapse, 2021–2022 rise).
- Stationarity: non-stationary in levels; returns are closer to stationary but contain regime-driven deviations.
- Volatility: pronounced spikes at 2014–2016, 2020, and 2022.

Change-point model (Task 1 prototype):

- Specification: piecewise model estimating unknown change-point dates with regime-specific mean and volatility (Student-t or Gaussian likelihood depending on tail behavior).
- Rationale: captures piecewise-stationary behavior and quantifies uncertainty on break dates, aligning with Task 1 goals to map events to structural shifts.

## 3. Next steps & focus areas (4 pts)

Planned Task 1 follow-ups:

- Finalize and vet the event list sources and exact timestamps in `data/structured_events.csv`; add source attribution column if needed.
- Run sensitivity checks on prototype: alternative likelihoods (Student-t), priors, and return vs level specifications.
- Produce a one-page visualization pack: time series with posterior change-point credible bands and event annotations for stakeholder review.

Validation priorities:

- Avoid causal wording; present associations with uncertainty.
- Compare model fits (LOO/WAIC) and posterior predictive checks to ensure model adequacy for Task 1 signals.

## 4. Structure, clarity, conciseness (4 pts)

This document is intentionally concise (≈1 page) and focused solely on Task 1: objectives, completed EDA and event mapping, initial model prototype, and immediate next steps. Key artifacts are located in the repository: `data/processed_brent_prices_2014_2022.csv`, `data/structured_events.csv`, `notebooks/task1_exploratory_data_analysis.ipynb`, and `src/data_processing.py`.

The structured event dataset is now available at `data/structured_events.csv` for use in modeling and analysis pipelines.

---

Saved as: `reports/interim_report_task1.md`
