"""
Task 3: Interactive Dashboard for Bayesian Oil Market Insights
A Streamlit application for exploring Brent oil price change point analysis results
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
import json
from pathlib import Path

# Configure page
st.set_page_config(
    page_title="Brent Oil Market Insights",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Define paths
DATA_DIR = Path(__file__).parent.parent / "data"
REPORTS_DIR = Path(__file__).parent.parent / "reports" / "figures"

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #666;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
    .insight-box {
        background-color: #e8f4f8;
        padding: 1.5rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
        border-left: 4px solid #17a2b8;
    }
    .warning-box {
        background-color: #fff3cd;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #ffc107;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    """Load all required data files"""
    # Load price data with change point indicator
    df = pd.read_csv(DATA_DIR / "brent_with_changepoint.csv")
    df['Date'] = pd.to_datetime(df['Date'])
    
    # Load events
    events_df = pd.read_csv(DATA_DIR / "structured_events.csv")
    events_df['Date'] = pd.to_datetime(events_df['Date'])
    
    # Load change point results
    with open(DATA_DIR / "changepoint_results.json", 'r') as f:
        results = json.load(f)
    
    return df, events_df, results

def create_price_chart(df, events_df, results):
    """Create interactive price chart with change point and events"""
    fig = go.Figure()
    
    # Price line
    fig.add_trace(go.Scatter(
        x=df['Date'],
        y=df['Price'],
        mode='lines',
        name='Brent Price',
        line=dict(color='steelblue', width=2),
        hovertemplate='<b>%{x|%Y-%m-%d}</b><br>Price: $%{y:.2f}/barrel<extra></extra>'
    ))
    
    # Change point line - use shape instead of vline to avoid datetime arithmetic issues
    change_date = pd.to_datetime(results['change_point_date'])
    fig.add_shape(
        type="line",
        x0=change_date, x1=change_date,
        y0=0, y1=1,
        yref="paper",
        line=dict(color="red", width=3, dash="dash")
    )
    fig.add_annotation(
        x=change_date,
        y=1,
        yref="paper",
        text=f"Change Point: {results['change_point_date']}",
        showarrow=False,
        yshift=10
    )
    
    # Add events as markers
    event_colors = {
        'OPEC_Decision': 'green',
        'Geopolitical': 'darkred',
        'Economic_Shock': 'orange'
    }
    
    for event_type in events_df['Event_Type'].unique():
        event_data = events_df[events_df['Event_Type'] == event_type]
        
        # Get prices at event dates
        event_prices = []
        for date in event_data['Date']:
            closest_idx = (df['Date'] - date).abs().argmin()
            event_prices.append(df.iloc[closest_idx]['Price'])
        
        fig.add_trace(go.Scatter(
            x=event_data['Date'],
            y=event_prices,
            mode='markers',
            name=event_type.replace('_', ' '),
            marker=dict(
                size=12,
                color=event_colors.get(event_type, 'gray'),
                symbol='diamond',
                line=dict(width=2, color='white')
            ),
            text=event_data['Description'],
            hovertemplate='<b>%{text}</b><br>Date: %{x|%Y-%m-%d}<br>Price: $%{y:.2f}<extra></extra>'
        ))
    
    fig.update_layout(
        title="Brent Oil Prices (2014-2022) with Detected Change Point",
        xaxis_title="Date",
        yaxis_title="Price (USD/barrel)",
        hovermode='x unified',
        height=500,
        template='plotly_white',
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )
    
    return fig

def create_returns_chart(df, results):
    """Create log returns chart with regime means"""
    change_date = pd.to_datetime(results['change_point_date'])
    
    fig = go.Figure()
    
    # Log returns
    fig.add_trace(go.Scatter(
        x=df['Date'],
        y=df['log_return'],
        mode='lines',
        name='Log Returns',
        line=dict(color='darkblue', width=1),
        opacity=0.7,
        hovertemplate='<b>%{x|%Y-%m-%d}</b><br>Return: %{y:.6f}<extra></extra>'
    ))
    
    # Change point line using shape
    fig.add_shape(
        type="line",
        x0=change_date, x1=change_date,
        y0=0, y1=1,
        yref="paper",
        line=dict(color="red", width=2, dash="dash")
    )
    
    # Before regime mean
    before_data = df[df['Date'] < change_date]
    if len(before_data) > 0:
        fig.add_hline(
            y=results['mu_before'],
            line_dash="dot",
            line_color="blue",
            line_width=2,
            annotation_text=f"Before μ={results['mu_before']:.6f}",
            annotation_position="left"
        )
    
    # After regime mean
    after_data = df[df['Date'] >= change_date]
    if len(after_data) > 0:
        fig.add_hline(
            y=results['mu_after'],
            line_dash="dot",
            line_color="red",
            line_width=2,
            annotation_text=f"After μ={results['mu_after']:.6f}",
            annotation_position="right"
        )
    
    fig.update_layout(
        title="Daily Log Returns with Regime Shift",
        xaxis_title="Date",
        yaxis_title="Log Return",
        height=400,
        template='plotly_white',
        hovermode='x unified'
    )
    
    return fig

def create_event_timeline(events_df, results):
    """Create interactive event timeline"""
    change_date = pd.to_datetime(results['change_point_date'])
    
    # Calculate days from change point
    events_df = events_df.copy()
    events_df['days_from_cp'] = (events_df['Date'] - change_date).dt.days
    events_df['abs_days'] = events_df['days_from_cp'].abs()
    events_df = events_df.sort_values('Date')
    
    # Create color mapping
    color_map = {
        'OPEC_Decision': '#2ecc71',
        'Geopolitical': '#e74c3c',
        'Economic_Shock': '#f39c12'
    }
    events_df['color'] = events_df['Event_Type'].map(color_map)
    
    fig = go.Figure()
    
    # Add events as scatter points
    fig.add_trace(go.Scatter(
        x=events_df['Date'],
        y=[1] * len(events_df),
        mode='markers+text',
        marker=dict(
            size=15,
            color=events_df['color'],
            symbol='circle',
            line=dict(width=2, color='white')
        ),
        text=events_df['Event_Type'].str.replace('_', ' '),
        textposition='top center',
        hovertext=events_df.apply(
            lambda row: f"<b>{row['Description']}</b><br>"
                       f"Date: {row['Date'].strftime('%Y-%m-%d')}<br>"
                       f"Type: {row['Event_Type']}<br>"
                       f"Expected Impact: {row['Expected_Impact']}<br>"
                       f"Days from change point: {row['days_from_cp']:+d}",
            axis=1
        ),
        hoverinfo='text',
        name='Events'
    ))
    
    # Add change point reference line using shape
    fig.add_shape(
        type="line",
        x0=change_date, x1=change_date,
        y0=0, y1=1,
        yref="paper",
        line=dict(color="red", width=3, dash="dash")
    )
    fig.add_annotation(
        x=change_date,
        y=1,
        yref="paper",
        text="Change Point",
        showarrow=False,
        yshift=10
    )
    
    fig.update_layout(
        title="Major Oil Market Events Timeline",
        xaxis_title="Date",
        yaxis=dict(
            showticklabels=False,
            range=[0, 2]
        ),
        height=300,
        template='plotly_white',
        hovermode='closest',
        showlegend=False
    )
    
    return fig

def create_impact_metrics(results):
    """Create metrics summary"""
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric(
            label="Change Point Date",
            value=results['change_point_date'],
            delta=f"±{results['change_point_uncertainty_days']:.0f} days"
        )
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        mean_change_pct = results['mean_change'] * 100
        st.metric(
            label="Mean Return Shift",
            value=f"{results['mean_change']:.6f}",
            delta=f"{results['prob_mean_increase']*100:.1f}% prob. increase"
        )
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col3:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric(
            label="Volatility Shift",
            value=f"{results['volatility_change']:.6f}",
            delta=f"{results['prob_volatility_increase']*100:.1f}% prob. increase"
        )
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col4:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric(
            label="Price Impact",
            value=f"${results['price_before']:.2f} → ${results['price_after']:.2f}",
            delta=f"{results['price_change_pct']:+.2f}%"
        )
        st.markdown('</div>', unsafe_allow_html=True)

def main():
    # Header
    st.markdown('<div class="main-header">🛢️ Brent Oil Market Insights Dashboard</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Bayesian Change Point Analysis | 2014-2022</div>', unsafe_allow_html=True)
    
    # Load data
    try:
        df, events_df, results = load_data()
    except Exception as e:
        st.error(f"Error loading data: {e}")
        st.info("Make sure Task 2 notebook has been executed to generate required files.")
        return
    
    # Sidebar
    with st.sidebar:
        st.header("📊 Navigation")
        page = st.radio(
            "Select View:",
            ["Overview", "Price Analysis", "Event Analysis", "Statistical Details", "About"]
        )
        
        st.markdown("---")
        st.header("⚙️ Filters")
        
        # Date range filter
        min_date = df['Date'].min().date()
        max_date = df['Date'].max().date()
        
        date_range = st.date_input(
            "Date Range:",
            value=(min_date, max_date),
            min_value=min_date,
            max_value=max_date
        )
        
        # Event type filter
        event_types = st.multiselect(
            "Event Types:",
            options=events_df['Event_Type'].unique().tolist(),
            default=events_df['Event_Type'].unique().tolist()
        )
        
        st.markdown("---")
        st.markdown("**Data Sources:**")
        st.markdown(f"- {len(df)} price observations")
        st.markdown(f"- {len(events_df)} major events")
        st.markdown(f"- Analysis: PyMC 5.27.1")
    
    # Filter data
    if len(date_range) == 2:
        df_filtered = df[(df['Date'].dt.date >= date_range[0]) & 
                         (df['Date'].dt.date <= date_range[1])]
    else:
        df_filtered = df
    
    events_filtered = events_df[events_df['Event_Type'].isin(event_types)]
    
    # Page content
    if page == "Overview":
        st.header("📈 Executive Summary")
        
        # Key metrics
        create_impact_metrics(results)
        
        st.markdown("---")
        
        # Main visualization
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.subheader("Price Series with Change Point")
            fig = create_price_chart(df_filtered, events_filtered, results)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.subheader("Key Findings")
            st.markdown(f"""
            <div class="insight-box">
            <h4>🎯 Change Point Detected</h4>
            <p><strong>Date:</strong> {results['change_point_date']}</p>
            <p><strong>Uncertainty:</strong> ±{results['change_point_uncertainty_days']:.0f} days</p>
            
            <h4>📊 Regime Shift</h4>
            <p><strong>Before:</strong> μ = {results['mu_before']:.6f}, σ = {results['sigma_before']:.6f}</p>
            <p><strong>After:</strong> μ = {results['mu_after']:.6f}, σ = {results['sigma_after']:.6f}</p>
            
            <h4>💰 Price Impact</h4>
            <p><strong>Average Price Change:</strong> ${results['price_before']:.2f} → ${results['price_after']:.2f}</p>
            <p><strong>Percentage:</strong> {results['price_change_pct']:+.2f}%</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Event timeline
        st.subheader("Event Timeline")
        fig_timeline = create_event_timeline(events_filtered, results)
        st.plotly_chart(fig_timeline, use_container_width=True)
        
        # Interpretation
        st.markdown(f"""
        <div class="warning-box">
        <h4>⚠️ Important Note: Correlation ≠ Causation</h4>
        <p>The detected change point represents a <strong>statistical structural break</strong> in the time series. 
        While we can identify events that occurred near this break, establishing causal relationships requires:</p>
        <ul>
            <li>Exogenous instruments or natural experiments</li>
            <li>Control for confounding variables (USD exchange rates, global demand, inventory levels)</li>
            <li>Domain expertise to assess plausibility of causal mechanisms</li>
        </ul>
        <p>This analysis provides <strong>associative evidence</strong> for hypothesis generation and further investigation.</p>
        </div>
        """, unsafe_allow_html=True)
    
    elif page == "Price Analysis":
        st.header("💹 Detailed Price Analysis")
        
        # Price chart
        fig = create_price_chart(df_filtered, events_filtered, results)
        st.plotly_chart(fig, use_container_width=True)
        
        # Returns analysis
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Log Returns")
            fig_returns = create_returns_chart(df_filtered, results)
            st.plotly_chart(fig_returns, use_container_width=True)
        
        with col2:
            st.subheader("Return Distribution")
            fig_hist = go.Figure()
            fig_hist.add_trace(go.Histogram(
                x=df_filtered['log_return'],
                nbinsx=100,
                name='Log Returns',
                marker_color='steelblue'
            ))
            fig_hist.update_layout(
                title="Distribution of Log Returns",
                xaxis_title="Log Return",
                yaxis_title="Frequency",
                height=400,
                template='plotly_white'
            )
            st.plotly_chart(fig_hist, use_container_width=True)
        
        # Summary statistics
        st.subheader("Summary Statistics")
        
        change_date = pd.to_datetime(results['change_point_date'])
        before = df_filtered[df_filtered['Date'] < change_date]
        after = df_filtered[df_filtered['Date'] >= change_date]
        
        stats_df = pd.DataFrame({
            'Metric': ['Count', 'Mean Price', 'Std Dev', 'Min Price', 'Max Price', 'Mean Return', 'Return Volatility'],
            'Before Change Point': [
                len(before),
                f"${before['Price'].mean():.2f}",
                f"${before['Price'].std():.2f}",
                f"${before['Price'].min():.2f}",
                f"${before['Price'].max():.2f}",
                f"{before['log_return'].mean():.6f}",
                f"{before['log_return'].std():.6f}"
            ],
            'After Change Point': [
                len(after),
                f"${after['Price'].mean():.2f}",
                f"${after['Price'].std():.2f}",
                f"${after['Price'].min():.2f}",
                f"${after['Price'].max():.2f}",
                f"{after['log_return'].mean():.6f}",
                f"{after['log_return'].std():.6f}"
            ]
        })
        
        st.dataframe(stats_df, use_container_width=True, hide_index=True)
    
    elif page == "Event Analysis":
        st.header("🌍 Event Impact Analysis")
        
        # Calculate distances from change point
        change_date = pd.to_datetime(results['change_point_date'])
        events_analysis = events_filtered.copy()
        events_analysis['days_from_changepoint'] = (events_analysis['Date'] - change_date).dt.days
        events_analysis['abs_days'] = events_analysis['days_from_changepoint'].abs()
        events_analysis = events_analysis.sort_values('abs_days')
        
        # Timeline
        fig_timeline = create_event_timeline(events_analysis, results)
        st.plotly_chart(fig_timeline, use_container_width=True)
        
        st.markdown("---")
        
        # Event breakdown
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Events by Type")
            type_counts = events_analysis['Event_Type'].value_counts()
            fig_pie = px.pie(
                values=type_counts.values,
                names=type_counts.index,
                color_discrete_sequence=['#2ecc71', '#e74c3c', '#f39c12']
            )
            fig_pie.update_layout(height=400)
            st.plotly_chart(fig_pie, use_container_width=True)
        
        with col2:
            st.subheader("Closest Events to Change Point")
            closest_events = events_analysis.head(5)[['Date', 'Event_Type', 'Description', 'days_from_changepoint']]
            closest_events['Date'] = closest_events['Date'].dt.strftime('%Y-%m-%d')
            closest_events.columns = ['Date', 'Type', 'Description', 'Days from CP']
            st.dataframe(closest_events, use_container_width=True, hide_index=True)
        
        # Full event table
        st.subheader("All Events")
        display_events = events_analysis[['Date', 'Event_Type', 'Description', 'Expected_Impact', 'days_from_changepoint']].copy()
        display_events['Date'] = display_events['Date'].dt.strftime('%Y-%m-%d')
        display_events.columns = ['Date', 'Type', 'Description', 'Expected Impact', 'Days from CP']
        st.dataframe(display_events, use_container_width=True, hide_index=True)
    
    elif page == "Statistical Details":
        st.header("📐 Statistical Model Details")
        
        st.subheader("Model Specification")
        st.markdown("""
        **Bayesian Change Point Model:**
        
        ```
        τ ~ DiscreteUniform(0, T-1)              # Change point location
        μ_before ~ Normal(0, 0.1)                # Mean return before change point
        μ_after ~ Normal(0, 0.1)                 # Mean return after change point
        σ_before ~ HalfNormal(0.1)               # Volatility before change point
        σ_after ~ HalfNormal(0.1)                # Volatility after change point
        
        μ_t = μ_before if t < τ else μ_after     # Piecewise mean
        σ_t = σ_before if t < τ else σ_after     # Piecewise volatility
        
        r_t ~ Normal(μ_t, σ_t)                   # Likelihood
        ```
        
        **Inference:**
        - MCMC Sampling with PyMC 5.27.1
        - 100 draws, 50 tuning steps, 1 chain
        - Metropolis sampler for discrete τ
        - NUTS sampler for continuous parameters
        """)
        
        st.subheader("Posterior Results")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Change Point:**")
            st.write(f"- Detected: {results['change_point_date']}")
            st.write(f"- Index: {results['change_point_index']}")
            st.write(f"- Uncertainty: ±{results['change_point_uncertainty_days']:.1f} days")
            
            st.markdown("**Before Regime:**")
            st.write(f"- μ_before: {results['mu_before']:.6f}")
            st.write(f"- σ_before: {results['sigma_before']:.6f}")
        
        with col2:
            st.markdown("**After Regime:**")
            st.write(f"- μ_after: {results['mu_after']:.6f}")
            st.write(f"- σ_after: {results['sigma_after']:.6f}")
            
            st.markdown("**Parameter Shifts:**")
            st.write(f"- Δμ: {results['mean_change']:.6f}")
            st.write(f"- Δσ: {results['volatility_change']:.6f}")
        
        st.subheader("Probabilistic Statements")
        
        st.markdown(f"""
        - **{results['prob_mean_increase']*100:.1f}%** posterior probability that mean returns increased
        - **{results['prob_volatility_increase']*100:.1f}%** posterior probability that volatility increased
        - **{results['price_change_pct']:+.2f}%** average price change across regimes
        """)
        
        st.subheader("Model Assumptions & Limitations")
        st.markdown("""
        **Assumptions:**
        1. Single structural break in the time series
        2. Piecewise stationarity (constant parameters within regimes)
        3. Normal likelihood for log returns
        4. Independence of observations (no autocorrelation modeling)
        
        **Limitations:**
        1. May oversimplify complex dynamics (multiple change points possible)
        2. Does not model time-varying volatility (GARCH effects)
        3. Excludes exogenous covariates (USD, inventory, macro indicators)
        4. Association with events does not imply causation
        
        **Future Enhancements:**
        - Multiple change point detection
        - Student-t likelihood for heavy tails
        - GARCH-type volatility modeling
        - Covariate inclusion for event impact quantification
        """)
    
    else:  # About
        st.header("ℹ️ About This Dashboard")
        
        st.markdown("""
        ### Project: Bayesian Oil Market Insights
        
        **Objective:** Analyze Brent oil price structural breaks using Bayesian change point detection 
        and associate detected shifts with major geopolitical and economic events.
        
        **Organization:** Birhan Energies - Data Science Team
        
        **Data Sources:**
        - **Brent Oil Prices:** 2,258 daily observations (2014-2022)
        - **Major Events:** 15 curated geopolitical, OPEC, and economic events
        
        **Methodology:**
        - Bayesian change point model with discrete switch point
        - MCMC inference using PyMC 5.27.1
        - Posterior analysis for uncertainty quantification
        - Event association within temporal windows
        
        **Technology Stack:**
        - **Modeling:** PyMC, ArviZ, NumPy, Pandas
        - **Visualization:** Plotly, Seaborn, Matplotlib
        - **Dashboard:** Streamlit
        - **Data Processing:** Python 3.11+
        
        ### Task Deliverables
        
        ✅ **Task 1:** Exploratory Data Analysis  
        ✅ **Task 2:** Bayesian Change Point Analysis  
        ✅ **Task 3:** Interactive Dashboard (This Application)
        
        ### Stakeholder Value
        
        **📊 For Investors:**
        - Identify regime shifts for portfolio rebalancing
        - Quantify risk through volatility changes
        - Track event impacts on price dynamics
        
        **🏛️ For Policymakers:**
        - Assess effectiveness of policy interventions
        - Understand market responses to geopolitical events
        - Plan strategic reserves and regulations
        
        **⚡ For Energy Companies:**
        - Optimize hedging strategies around structural breaks
        - Forecast price trends in different regimes
        - Align operational planning with market dynamics
        
        ### Key Insights
        
        This analysis reveals that Brent oil prices experienced a significant structural break in 
        {results['change_point_date']}, characterized by a shift in mean returns 
        ({results['mean_change']:+.6f}) and volatility ({results['volatility_change']:+.6f}).
        
        The average price changed from ${results['price_before']:.2f} to ${results['price_after']:.2f} 
        per barrel ({results['price_change_pct']:+.2f}%), providing actionable insights for 
        stakeholders navigating the complex global oil market.
        
        ### Contact & Resources
        
        - **GitHub:** [Bayesian Oil Market Insights](https://github.com/Bekamgenene/bayesian-oil-market-insights)
        - **Documentation:** See project README.md
        - **Data:** Available in `data/` directory
        - **Figures:** Available in `reports/figures/` directory
        
        ### Disclaimer
        
        This analysis is for informational and educational purposes only. The detected associations 
        between events and price changes do not imply causation. Investment and policy decisions 
        should incorporate additional analysis, domain expertise, and risk assessment.
        """)
        
        st.markdown("---")
        st.markdown("**Built with ❤️ using Streamlit | © 2026 Birhan Energies**")

if __name__ == "__main__":
    main()
