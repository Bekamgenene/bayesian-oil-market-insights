# Quick Reference: Understanding Bayesian Change Point Models

## What is a Change Point?

A **change point** (τ, tau) is a specific moment in time when the statistical properties of a data-generating process fundamentally shift.

**In oil markets:** A change point might represent when:

- Average price level jumps from $50/barrel to $80/barrel
- Market volatility doubles or halves
- Price trend reverses from increasing to decreasing

---

## Why Bayesian Approach?

### Classical Methods

- Give a single "best guess" for change point
- Example: "Change occurred on Day 5,047"

### Bayesian Methods

- Give full probability distribution
- Example: "95% confident change occurred between Days 5,040-5,055"
- Quantify uncertainty explicitly
- Natural for decision-making under uncertainty

---

## Model Components

### 1. The Switch Point (τ)

```
Prior: τ ~ DiscreteUniform(0, T)
```

- τ can be any day in dataset
- Before seeing data, all days equally likely
- After inference, posterior tells us most probable timing

### 2. Before/After Parameters

```
Before change:  μ₁ (mean), σ₁ (volatility)
After change:   μ₂ (mean), σ₂ (volatility)
```

### 3. The Switch Function

```python
mean = pm.math.switch(t < τ, μ₁, μ₂)
# If day t is before τ, use μ₁
# If day t is after τ, use μ₂
```

### 4. Likelihood (How data is generated)

```
Price[t] ~ Normal(mean[t], σ[t])
```

---

## How MCMC Works (Simplified)

**MCMC** = Markov Chain Monte Carlo

Think of it as intelligent random sampling:

1. **Start** with random guesses for τ, μ₁, μ₂, σ₁, σ₂
2. **Propose** small changes to parameters
3. **Accept** changes that make data more likely
4. **Repeat** thousands of times
5. **Result**: Distribution of plausible parameter values

**Why useful?** Exact calculation is mathematically impossible for complex models. MCMC approximates the answer through simulation.

---

## Interpreting Results

### Posterior Distribution of τ

**Sharp Peak:**

```
      ▁▂▅█▅▂▁
Day: 5045  5050  5055
```

✅ High certainty: Change point very likely around Day 5,050

**Broad Distribution:**

```
   ▁▂▃▄▅▅▄▃▂▁
Day: 5000    5050    5100
```

⚠️ Uncertainty: Change could be anywhere in wide range

### R-hat (Convergence Diagnostic)

- **R-hat ≈ 1.00**: ✅ Chains converged, results trustworthy
- **R-hat > 1.01**: ⚠️ Chains haven't converged, run longer
- **R-hat > 1.1**: ❌ Results unreliable, debug model

### Effective Sample Size (ESS)

- **ESS > 1000**: ✅ Good
- **ESS < 100**: ⚠️ High autocorrelation, may need more samples

---

## Example Interpretation

**Scenario:** Analyzing 2020 oil price collapse

**Model Output:**

```
τ posterior: Day 5,020 (95% HPD: 5,015-5,025)
μ₁ = $65.3/barrel (before)
μ₂ = $35.1/barrel (after)
Δμ = -$30.2/barrel (-46%)
```

**Translation:**
"We detect a structural break around March 9, 2020 (Day 5,020), with 95% confidence the change occurred within ±5 days. Average daily price dropped from $65.30 to $35.10, a 46% decline."

**Event Association:**
March 9, 2020: Saudi-Russia price war begins → Consistent timing!

---

## Common Pitfalls

### ❌ Claiming Causation

**Wrong:** "The Saudi-Russia price war _caused_ the change point."
**Right:** "The detected change point coincides with the Saudi-Russia price war, consistent with a causal relationship."

### ❌ Ignoring Uncertainty

**Wrong:** "Change occurred on Day 5,020."
**Right:** "Change most likely occurred around Day 5,020 (95% credible interval: Days 5,015-5,025)."

### ❌ Over-interpreting Single Model

**Wrong:** "This proves there was exactly one regime shift."
**Right:** "Our single-change-point model identifies the most prominent shift, but multiple changes likely occurred."

---

## Time Series Properties Checklist

Before modeling, understand your data:

### ✅ Trend

- **Definition:** Long-term directional movement
- **Test:** Visual inspection, moving averages
- **Impact:** Non-stationary trend suggests differencing or modeling trend explicitly

### ✅ Stationarity

- **Definition:** Constant mean and variance over time
- **Test:** Augmented Dickey-Fuller (ADF) test
  - p-value < 0.05: Stationary ✅
  - p-value > 0.05: Non-stationary ⚠️
- **Impact:** Non-stationary data needs transformation (log returns, differencing)

### ✅ Volatility Clustering

- **Definition:** Periods where large changes follow large changes
- **Test:** Plot squared returns, ACF of squared returns
- **Impact:** May need to model changing variance (σ₁ ≠ σ₂)

---

## Practical Tips

### 1. Start Simple

- Begin with single change point model
- Add complexity only if needed

### 2. Visual Inspection First

- Plot raw data before modeling
- Eyeball likely change points
- Use as sanity check for results

### 3. Multiple Chains

- Run 3-4 MCMC chains
- Check they converge to same answer
- If diverge → model issue

### 4. Prior Sensitivity

- Try different priors
- If results change drastically → data is weak, be cautious

### 5. Event Timeline

- Keep detailed event log
- Note exact dates
- Cross-reference with change points

---

## Glossary

| Term            | Definition                                    |
| --------------- | --------------------------------------------- |
| **τ (tau)**     | Change point location (day index)             |
| **μ (mu)**      | Mean parameter                                |
| **σ (sigma)**   | Standard deviation (volatility)               |
| **Prior**       | Beliefs before seeing data                    |
| **Posterior**   | Updated beliefs after seeing data             |
| **Likelihood**  | How probable data is given parameters         |
| **MCMC**        | Sampling algorithm for Bayesian inference     |
| **Trace**       | Sequence of sampled parameter values          |
| **HPD**         | Highest Posterior Density (credible interval) |
| **Convergence** | MCMC chains reaching stable distribution      |

---

## Python Code Skeleton

```python
import pymc as pm
import numpy as np

# Assume data loaded as price_data (array of daily prices)
n_data = len(price_data)

with pm.Model() as model:
    # Prior for change point location
    tau = pm.DiscreteUniform('tau', lower=0, upper=n_data-1)

    # Priors for before/after means
    mu_1 = pm.Normal('mu_before', mu=50, sigma=20)
    mu_2 = pm.Normal('mu_after', mu=50, sigma=20)

    # Priors for before/after volatilities
    sigma_1 = pm.HalfNormal('sigma_before', sigma=10)
    sigma_2 = pm.HalfNormal('sigma_after', sigma=10)

    # Switch function
    idx = np.arange(n_data)
    mu = pm.math.switch(idx < tau, mu_1, mu_2)
    sigma = pm.math.switch(idx < tau, sigma_1, sigma_2)

    # Likelihood
    obs = pm.Normal('obs', mu=mu, sigma=sigma, observed=price_data)

    # Sample
    trace = pm.sample(2000, tune=1000, chains=4)

# Analyze results
pm.summary(trace)
pm.plot_trace(trace)
```

---

**Created:** February 5, 2026  
**Purpose:** Task 1 Reference for Bayesian Change Point Analysis  
**Author:** Data Science Team, Birhan Energies
