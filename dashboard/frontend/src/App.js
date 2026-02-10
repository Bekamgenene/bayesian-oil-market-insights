import React, { useState, useEffect } from "react";
import {
  fetchPrices,
  fetchEvents,
  fetchChangepoint,
  fetchStatistics,
  fetchDateRange,
} from "./services/api";
import PriceChart from "./components/PriceChart";
import EventTimeline from "./components/EventTimeline";
import MetricCards from "./components/MetricCards";
import DateFilter from "./components/DateFilter";
import "./App.css";

function App() {
  const [priceData, setPriceData] = useState([]);
  const [events, setEvents] = useState([]);
  const [changepoint, setChangepoint] = useState(null);
  const [statistics, setStatistics] = useState(null);
  const [dateRange, setDateRange] = useState({ min: null, max: null });
  const [filters, setFilters] = useState({
    startDate: null,
    endDate: null,
    eventTypes: [],
  });
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [activeTab, setActiveTab] = useState("overview");

  useEffect(() => {
    loadInitialData();
  }, []);

  useEffect(() => {
    if (dateRange.min) {
      loadFilteredData();
    }
  }, [filters]);

  const loadInitialData = async () => {
    try {
      setLoading(true);

      const [rangeRes, cpRes] = await Promise.all([
        fetchDateRange(),
        fetchChangepoint(),
      ]);

      setDateRange(rangeRes.data);
      setChangepoint(cpRes.data);

      setFilters({
        startDate: rangeRes.data.min_date,
        endDate: rangeRes.data.max_date,
        eventTypes: [],
      });

      setLoading(false);
    } catch (err) {
      setError(err.message);
      setLoading(false);
    }
  };

  const loadFilteredData = async () => {
    try {
      const [pricesRes, eventsRes, statsRes] = await Promise.all([
        fetchPrices(filters.startDate, filters.endDate),
        fetchEvents(
          filters.startDate,
          filters.endDate,
          filters.eventTypes.join(","),
        ),
        fetchStatistics(filters.startDate, filters.endDate),
      ]);

      setPriceData(pricesRes.data);
      setEvents(eventsRes.data);
      setStatistics(statsRes.data);
    } catch (err) {
      setError(err.message);
    }
  };

  const handleFilterChange = (newFilters) => {
    setFilters({ ...filters, ...newFilters });
  };

  if (loading) {
    return (
      <div className="loading-container">
        <div className="spinner"></div>
        <p>Loading Bayesian Oil Market Insights...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="error-container">
        <h2>Error Loading Data</h2>
        <p>{error}</p>
        <button onClick={loadInitialData}>Retry</button>
      </div>
    );
  }

  return (
    <div className="App">
      <header className="app-header">
        <h1>📈 Bayesian Oil Market Insights</h1>
        <p className="subtitle">
          Change Point Analysis of Brent Oil Prices (2014-2022)
        </p>
      </header>

      <nav className="tab-navigation">
        <button
          className={activeTab === "overview" ? "active" : ""}
          onClick={() => setActiveTab("overview")}
        >
          Overview
        </button>
        <button
          className={activeTab === "prices" ? "active" : ""}
          onClick={() => setActiveTab("prices")}
        >
          Price Analysis
        </button>
        <button
          className={activeTab === "events" ? "active" : ""}
          onClick={() => setActiveTab("events")}
        >
          Events
        </button>
        <button
          className={activeTab === "statistics" ? "active" : ""}
          onClick={() => setActiveTab("statistics")}
        >
          Statistics
        </button>
      </nav>

      <div className="content-wrapper">
        <aside className="sidebar">
          <DateFilter
            dateRange={dateRange}
            filters={filters}
            onFilterChange={handleFilterChange}
          />
        </aside>

        <main className="main-content">
          {activeTab === "overview" && (
            <div className="tab-content">
              <h2>Overview</h2>
              <MetricCards changepoint={changepoint} statistics={statistics} />

              <div className="chart-container">
                <h3>Price Series with Change Point</h3>
                <PriceChart
                  data={priceData}
                  events={events}
                  changepoint={changepoint}
                />
              </div>

              <div className="insight-box">
                <h3>🔍 Key Finding</h3>
                <p>
                  Detected structural break on{" "}
                  <strong>{changepoint?.change_point_date}</strong> with ±
                  {changepoint?.change_point_uncertainty_days.toFixed(0)} days
                  uncertainty.
                </p>
                <p>
                  Volatility increased by{" "}
                  <strong>
                    {(changepoint?.volatility_change * 100).toFixed(2)}%
                  </strong>{" "}
                  with
                  {changepoint?.prob_volatility_increase * 100}% posterior
                  probability.
                </p>
              </div>
            </div>
          )}

          {activeTab === "prices" && (
            <div className="tab-content">
              <h2>Price Analysis</h2>
              <PriceChart
                data={priceData}
                events={events}
                changepoint={changepoint}
                detailed={true}
              />

              <div className="regime-comparison">
                <div className="regime-card before">
                  <h4>Before Change Point</h4>
                  <p>Mean Return: {changepoint?.mu_before.toFixed(6)}</p>
                  <p>Volatility: {changepoint?.sigma_before.toFixed(6)}</p>
                  <p>Avg Price: ${changepoint?.price_before.toFixed(2)}/bbl</p>
                </div>
                <div className="regime-card after">
                  <h4>After Change Point</h4>
                  <p>Mean Return: {changepoint?.mu_after.toFixed(6)}</p>
                  <p>Volatility: {changepoint?.sigma_after.toFixed(6)}</p>
                  <p>Avg Price: ${changepoint?.price_after.toFixed(2)}/bbl</p>
                </div>
              </div>
            </div>
          )}

          {activeTab === "events" && (
            <div className="tab-content">
              <h2>Event Timeline</h2>
              <EventTimeline events={events} changepoint={changepoint} />

              <div className="events-list">
                <h3>Event Details</h3>
                <table className="events-table">
                  <thead>
                    <tr>
                      <th>Date</th>
                      <th>Type</th>
                      <th>Description</th>
                      <th>Expected Impact</th>
                    </tr>
                  </thead>
                  <tbody>
                    {events.map((event, idx) => (
                      <tr key={idx}>
                        <td>{event.Date}</td>
                        <td>
                          <span className={`event-badge ${event.Event_Type}`}>
                            {event.Event_Type.replace("_", " ")}
                          </span>
                        </td>
                        <td>{event.Description}</td>
                        <td>{event.Expected_Impact}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          )}

          {activeTab === "statistics" && statistics && (
            <div className="tab-content">
              <h2>Statistical Summary</h2>

              <div className="stats-grid">
                <div className="stat-card">
                  <h4>Observations</h4>
                  <p className="stat-value">{statistics.count}</p>
                </div>
                <div className="stat-card">
                  <h4>Mean Price</h4>
                  <p className="stat-value">
                    ${statistics.mean_price?.toFixed(2)}
                  </p>
                </div>
                <div className="stat-card">
                  <h4>Price Range</h4>
                  <p className="stat-value">
                    ${statistics.min_price?.toFixed(2)} - $
                    {statistics.max_price?.toFixed(2)}
                  </p>
                </div>
                <div className="stat-card">
                  <h4>Mean Return</h4>
                  <p className="stat-value">
                    {statistics.mean_return?.toFixed(6)}
                  </p>
                </div>
                <div className="stat-card">
                  <h4>Volatility (σ)</h4>
                  <p className="stat-value">
                    {statistics.volatility?.toFixed(6)}
                  </p>
                </div>
                <div className="stat-card">
                  <h4>Std Deviation</h4>
                  <p className="stat-value">
                    ${statistics.std_price?.toFixed(2)}
                  </p>
                </div>
              </div>

              <div className="warning-box">
                <h4>⚠️ Interpretation Note</h4>
                <p>
                  This analysis identifies temporal correlations between events
                  and price changes. Association does not imply causation.
                  Further analysis with exogenous instruments or natural
                  experiments would be needed for causal claims.
                </p>
              </div>
            </div>
          )}
        </main>
      </div>

      <footer className="app-footer">
        <p>
          Bayesian Oil Market Insights | Flask + React Dashboard | Data:
          2014-2022
        </p>
        <p>
          Backend:{" "}
          <a
            href="http://localhost:5000/api/health"
            target="_blank"
            rel="noopener noreferrer"
          >
            API Health Check
          </a>
        </p>
      </footer>
    </div>
  );
}

export default App;
