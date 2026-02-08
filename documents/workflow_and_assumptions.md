# Workflow, Assumptions, and Communication Plan

## Executive summary

This brief (1–2 page) document summarizes the analysis workflow used in this project, the key assumptions and limitations that shape interpretation (especially around causality vs correlation), and a targeted communication plan for three primary stakeholder groups: investors, policymakers, and energy companies. The goal is to make results reproducible, actionable, and tailored to audience needs.

## Analysis workflow (concise)

1. Data ingestion
   - Collect raw price and event data (e.g., `BrentOilPrices.csv`, `major_oil_events.csv`).
   - Load structured event dataset from `data/structured_events.csv` containing 15 key geopolitical, OPEC, and macroeconomic events (2014–2022) with dates, types, descriptions, and expected impacts.
   - Apply deterministic cleaning and normalization in `src/data_processing.py` to create a stable processed dataset used for modeling.

2. Event tagging & enrichment
   - Map calendar events from `structured_events.csv` (OPEC decisions, geopolitical shocks, economic disruptions) to price time series.
   - Create binary/annotated event indicators and rolling aggregates used in feature engineering.
   - Generate event window indicators (±7, ±14, ±30 days) for impact assessment.

3. Model specification
   - Use Bayesian change-point models to detect structural breaks and regime shifts in price series.
   - Select priors that reflect domain knowledge (e.g., expected persistence of regimes) and perform sensitivity checks.

4. Inference & diagnostics
   - Run posterior sampling / inference with convergence diagnostics, posterior predictive checks, and model comparison metrics (WAIC, LOO where appropriate).
   - Log and save model artifacts and diagnostics for reproducibility.

5. Interpretation & robustness
   - Quantify uncertainty (credible intervals) for change-point times, regime means/volatilities, and event effects.
   - Run robustness checks: alternative priors, sub-samples, and placebo event tests.

6. Delivery & visualization
   - Produce figures (time series with posterior change-points), tabular summaries, and an interactive dashboard for exploratory analysis.

## Key assumptions and limitations

- Data completeness: analyses assume the provided price and event datasets are representative of the market periods studied. Missing or biased event capture can skew attribution.
- Stationarity within regimes: change-point models assume piecewise-stationary behavior between detected breaks. Rapid continuous drift can be mischaracterized as many small breaks.
- Prior knowledge: Bayesian priors encode domain beliefs; results can be sensitive to strong priors — sensitivity analysis is required.
- Event timing and attribution: we assume event timestamps align closely with market information flow. Delayed reporting or anticipatory trading can complicate attribution.
- External factors: macroeconomic, geopolitical, and inventory data not included may confound results.

Be explicit about these limitations whenever presenting numerical effect sizes or claiming causal relationships.

## Causality vs correlation guidance

- This project focuses on detecting structural changes and associations between events and price behavior. Association (correlation) is primary; causal claims require stronger identification strategies.
- When making causal claims, require at least one of: an exogenous shock (instrument), pre-registered identification strategy, or a natural experiment design with clear counterfactuals.
- Recommended language for reports: "We find strong evidence that X is associated with Y, with posterior median effect Z and 95% credible interval [a, b]. This should be interpreted as association unless an identification strategy is explicitly stated."

## Data handling & reproducibility practices

- All raw inputs remain in `data/` and processed outputs are written to `data/processed_*.csv` (see `src/data_processing.py`).
- Structured event dataset: `data/structured_events.csv` contains 15 curated events with Date, Event_Type (OPEC_Decision, Geopolitical, Economic_Shock), Description, and Expected_Impact columns. This dataset is version-controlled and serves as the canonical event reference for all analyses.
- Version inputs (timestamps or data hashes) and record the processing pipeline steps in a short changelog inside `documents/`.
- Save model code, priors, random seeds, and fitted objects to a `models/` folder (or commit to the repo if small) to allow exact reproduction.

## Communication plan — Stakeholders, channels, and tailoring

Stakeholder groups: investors, policymakers, energy companies.

- Investors
  - Key interests: near-term price risk, volatility regimes, investment timing, trade signals.
  - Channels/deliverables: concise slide deck (3–6 slides) + one-page executive summary + interactive dashboard filters for horizon-specific scenarios.
  - Tailoring: focus on numerical forecasts, scenario probabilities, expected downside/upside, and risk metrics (VaR-like summaries using posterior predictive draws). Highlight actionable trade or hedging implications and probabilities for regime shifts over investment horizons.

- Policymakers
  - Key interests: systemic risks, policy impact, market stability, distributional implications.
  - Channels/deliverables: policy brief (1–2 pages) + technical appendix + slide deck for briefings.
  - Tailoring: emphasize high-level takeaways, uncertainty bounds, how policy or supply changes may alter regime probabilities, and recommended monitoring indicators. Avoid trading advice; provide clear statements about limitations and data assumptions.

- Energy companies (producers, refiners, traders)
  - Key interests: operational risk, supply planning, hedging, scenario planning.
  - Channels/deliverables: technical report (4–8 pages) + dashboard with drill-down views + CSV outputs of scenario simulations and inferred change-points.
  - Tailoring: give operationally relevant timescales (monthly/quarterly), stress scenarios linking events to capacity/inventory impacts, and model parameters (priors, diagnostics) so internal analysts can audit and extend analyses.

## Recommended messaging and visuals

- Visuals: time series plots with shaded credible bands, annotated change-point markers, event ribbons, regime-specific volatility tables, and scenario probability gauges.
- Messaging: Always present central estimate + uncertainty, and clearly label association vs causal wording. Use short bullets for recommendations and a final "confidence & assumptions" box.

## Delivery cadence & governance

- Initial delivery: slide deck + executive summary + interactive dashboard snapshot.
- Follow-up cadence: monthly data refreshes with a short update note; quarterly deeper analysis with model re-calibration.
- Governance: assign a primary analyst responsible for updates, a reviewer (domain expert), and a stakeholder contact for distribution. Maintain a changelog in `documents/`.

## Next steps (suggested)

- Add the document to stakeholder deliverables and include a short changelog entry.
- Run sensitivity checks and export a small set of dashboard-ready CSVs tailored to each stakeholder group.

---

Generated to accompany the analyses in this repository; place and update as needed: [documents/workflow_and_assumptions.md](documents/workflow_and_assumptions.md)
