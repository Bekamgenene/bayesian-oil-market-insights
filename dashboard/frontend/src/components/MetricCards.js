import React from "react";

const MetricCards = ({ changepoint, statistics }) => {
  if (!changepoint) {
    return <div className="loading-message">Loading changepoint data...</div>;
  }

  const formatPercent = (value) => `${(value * 100).toFixed(1)}%`;
  const formatPrice = (value) => `$${value.toFixed(2)}`;
  const formatValue = (value, decimals = 6) => value.toFixed(decimals);

  return (
    <div className="metric-cards-container">
      <div className="metric-card changepoint-card">
        <div className="metric-icon">📍</div>
        <div className="metric-content">
          <h3>Change Point Detected</h3>
          <p className="metric-value">{changepoint.change_point_date}</p>
          <p className="metric-subtitle">
            Uncertainty: ±
            {changepoint.change_point_uncertainty_days?.toFixed(0)} days
          </p>
        </div>
      </div>

      <div className="metric-card mean-shift-card">
        <div className="metric-icon">📈</div>
        <div className="metric-content">
          <h3>Mean Return Shift</h3>
          <p className="metric-value">{formatValue(changepoint.mean_change)}</p>
          <p className="metric-subtitle">
            {formatPercent(changepoint.prob_mean_increase)} probability of
            increase
          </p>
        </div>
      </div>

      <div className="metric-card volatility-card">
        <div className="metric-icon">📊</div>
        <div className="metric-content">
          <h3>Volatility Shift</h3>
          <p className="metric-value">
            {formatValue(changepoint.volatility_change)}
          </p>
          <p className="metric-subtitle">
            {formatPercent(changepoint.prob_volatility_increase)} probability of
            increase
          </p>
        </div>
      </div>

      <div className="metric-card price-impact-card">
        <div className="metric-icon">💰</div>
        <div className="metric-content">
          <h3>Price Impact</h3>
          <p className="metric-value">
            {formatPrice(changepoint.price_before)} →{" "}
            {formatPrice(changepoint.price_after)}
          </p>
          <p className="metric-subtitle">
            {changepoint.price_change_pct > 0 ? "+" : ""}
            {changepoint.price_change_pct.toFixed(2)}% change
          </p>
        </div>
      </div>

      {statistics && (
        <>
          <div className="metric-card stats-card">
            <div className="metric-icon">📉</div>
            <div className="metric-content">
              <h3>Average Price (Before)</h3>
              <p className="metric-value">
                {formatPrice(changepoint.price_before)}
              </p>
              <p className="metric-subtitle">
                μ = {formatValue(changepoint.mu_before)}
              </p>
            </div>
          </div>

          <div className="metric-card stats-card">
            <div className="metric-icon">📈</div>
            <div className="metric-content">
              <h3>Average Price (After)</h3>
              <p className="metric-value">
                {formatPrice(changepoint.price_after)}
              </p>
              <p className="metric-subtitle">
                μ = {formatValue(changepoint.mu_after)}
              </p>
            </div>
          </div>

          <div className="metric-card stats-card">
            <div className="metric-icon">🎯</div>
            <div className="metric-content">
              <h3>Volatility (Before)</h3>
              <p className="metric-value">
                {formatValue(changepoint.sigma_before)}
              </p>
              <p className="metric-subtitle">Standard deviation</p>
            </div>
          </div>

          <div className="metric-card stats-card">
            <div className="metric-icon">🎲</div>
            <div className="metric-content">
              <h3>Volatility (After)</h3>
              <p className="metric-value">
                {formatValue(changepoint.sigma_after)}
              </p>
              <p className="metric-subtitle">Standard deviation</p>
            </div>
          </div>
        </>
      )}
    </div>
  );
};

export default MetricCards;
