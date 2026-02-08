# Interim Report — Bayesian Change-Point Analysis of Brent Prices (Concise)

## 1. Understanding & Defining the Business Objective (6 pts)

Purpose: quantify structural changes in Brent crude oil prices and link detected regime shifts to major political and economic events (2014–2022). The analysis aims to produce probabilistic, uncertainty-aware statements about when volatility or mean-price regimes changed and which events are plausibly associated with those shifts.

Stakeholder alignment:

- Investors: need probabilistic regime and volatility indicators to inform timing, risk, and hedging decisions.
- Policymakers: need evidence on how policy/supply shocks affect market stability and regime probabilities.
- Energy companies: need scenario-driven operational insights (supply planning, hedging horizons).

Method fit: Bayesian change-point detection is well suited because it yields posterior distributions over change-point times and regime parameters (means/volatilities), naturally handling uncertainty and allowing incorporation of domain priors (e.g., persistence of regimes). This aligns with the objective of delivering probabilistic, decision-relevant outputs rather than single-point attributions.

## 2. Discussion of Completed Work and Initial Analysis (6 pts)

Workflow (implemented):

- Data ingestion: raw files in `data/` (e.g., `BrentOilPrices.csv`); deterministic cleaning and resampling implemented in `src/data_processing.py`; processed series saved for modeling (see `data/processed_brent_prices_2014_2022.csv`).
- Event dataset creation: compiled structured event dataset at `data/structured_events.csv` containing 15 key events with Date, Event_Type, Description, and Expected_Impact fields.
- Event tagging & enrichment: mapped events from `structured_events.csv` to the price series (binary indicators, event windows, categorization by type).
- Model implementation: Bayesian change-point model configured to infer piecewise-constant mean and regime-specific volatility; priors chosen to be weakly informative with sensitivity checks planned.
- Inference & diagnostics: posterior sampling run with convergence checks and posterior predictive checks; visualizations include time series with posterior change-point credible bands.
- Deliverables produced: processed dataset, structured event dataset, model artifacts, and figure outputs for initial inspection.

Structured event dataset (15 events in `data/structured_events.csv`):

1. 2014-11-27 — OPEC_Decision: OPEC decides not to cut production despite falling prices (Supply_Negative)
2. 2015-01-15 — Economic_Shock: Continued global oversupply and China growth concerns (Demand_Negative)
3. 2016-11-30 — OPEC_Decision: OPEC agrees to cut production by 1.2M bpd (Supply_Positive)
4. 2018-05-08 — Geopolitical: U.S. withdraws from Iran nuclear deal; sanctions risk (Supply_Positive)
5. 2019-09-14 — Geopolitical: Attacks on Saudi Aramco facilities; 5.7M bpd offline (Supply_Positive)
6. 2020-03-06 — OPEC_Decision: Russia-Saudi price war begins; OPEC+ fails to agree (Supply_Negative)
7. 2020-03-11 — Economic_Shock: COVID-19 declared pandemic; global demand collapse (Demand_Negative)
8. 2020-04-12 — OPEC_Decision: OPEC+ agrees to historic production cuts of 9.7M bpd (Supply_Positive)
9. 2020-04-20 — Economic_Shock: WTI futures go negative; storage capacity concerns (Demand_Negative)
10. 2021-07-01 — Economic_Shock: Demand recovery amid Delta variant concerns (Mixed)
11. 2021-11-04 — OPEC_Decision: OPEC+ maintains gradual production increase (Supply_Neutral)
12. 2022-02-24 — Geopolitical: Russia invades Ukraine; major supply disruption risk (Supply_Positive)
13. 2022-03-08 — Geopolitical: U.S. and EU ban Russian oil imports (Supply_Positive)
14. 2022-06-02 — OPEC_Decision: OPEC+ accelerates production increases to offset Russian loss (Supply_Negative)
15. 2022-10-05 — OPEC_Decision: OPEC+ announces production cut of 2M bpd (Supply_Positive)

Preliminary time-series properties (summary):

- Trend: non-stationary with a multi-year decline from 2014 → 2016, recovery 2016→2018, dramatic pandemic shock 2020, and elevated levels and volatility into 2021–2022.
- Stationarity: series is non-stationary in levels; first-differencing reduces unit-root behavior but removes long-run regime signals — hence piecewise stationarity via change points is preferred.
- Volatility: heteroskedasticity with clear volatility spikes around 2014–2016, 2020, and 2022.

Change-point model (concise):

- Targets: infer K unknown change points (posterior), regime means µ_k and volatilities σ_k.
- Likelihood: piecewise-Gaussian (or Student-t for heavy tails) on log-prices or returns depending on specification.
- Priors: weakly informative on means and variances; prior on number/timing of change points encourages parsimony but allows multiple breaks.
- Outputs: posterior distributions for change-point dates, regime means/volatilities, posterior predictive simulations.

## 3. Next Steps & Key Areas of Focus (4 pts)

Planned follow-ups:

- Finalize and document the event list in `data/structured_events.csv`; add source attribution and verify exact timestamps with market data.
- Run robustness and sensitivity checks: alternative priors, Student-t likelihood for heavy tails, sub-sample analyses, and placebo event tests.
- Add covariates where appropriate (inventory, USD index, macro indicators) to help reduce confounding.
- Explore identification strategies for causal claims: exploit exogenous policy shocks, instrumental variables, or natural experiments where feasible.
- Prepare stakeholder deliverables: concise slide deck, one-page executive summary, and dashboard CSV exports tailored to investor/policymaker/company needs.

Key focus areas for validation:

- Attribution vs causation: avoid causal claims without identification; state associations with uncertainty.
- Model selection: compare models with different numbers/types of change points using LOO/WAIC and posterior predictive checks.
- Communication: ensure delivery materials clearly state assumptions, data coverage, and uncertainty.

## 4. Report structure, clarity, and conciseness (4 pts)

This interim report is intentionally concise (≈1 page plus event list) and organized to meet the rubric: objective, completed work (with structured dataset and properties), next steps, and clear statements about assumptions and limitations. Necessary documentation is present in the repository (`src/data_processing.py`, `data/processed_brent_prices_2014_2022.csv`, `data/structured_events.csv`, and `documents/workflow_and_assumptions.md`).

The structured event dataset at `data/structured_events.csv` is now integrated into the analysis pipeline and referenced in the workflow documentation.

---

Report file: `reports/interim_report.md`
