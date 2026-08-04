import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import warnings
import numpy as np
warnings.filterwarnings('ignore')

# Import custom modules
from analytics.portfolio import PortfolioAnalyzer
from analytics.health_score import HealthScoreCalculator
from analytics.recommendations import RecommendationEngine
from analytics.optimizer import PortfolioOptimizer
from analytics.advanced_risk import AdvancedRiskMetrics
from data.data_fetcher import DataFetcher
from data.sector_mapper import SectorMapper

# Page configuration
st.set_page_config(
    page_title="Smart Portfolio Analyzer",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Smart Portfolio Analyzer")
st.markdown("Professional portfolio analysis for wealth management")

# Sidebar input
with st.sidebar:
    st.header("Portfolio Input")
    
    num_stocks = st.number_input("Number of stocks", min_value=1, max_value=10, value=2)
    
    stocks = []
    weights = []
    
    # Pre-filled examples
    default_tickers = ["RELIANCE.NS", "TCS.NS"]
    default_weights = [50, 50]
    
    for i in range(num_stocks):
        col1, col2 = st.columns(2)
        with col1:
            default_ticker = default_tickers[i] if i < len(default_tickers) else ""
            ticker = st.text_input(f"Stock {i+1}", value=default_ticker, key=f"ticker_{i}")
            if ticker:
                stocks.append(ticker)
            else:
                stocks.append("")
        with col2:
            default_weight = default_weights[i] if i < len(default_weights) else 50
            weight = st.number_input(f"Weight %", min_value=0, max_value=100, 
                                    value=default_weight, key=f"weight_{i}")
            weights.append(weight)
    
    # Remove empty entries
    valid_stocks = []
    valid_weights = []
    for stock, weight in zip(stocks, weights):
        if stock and weight > 0:
            valid_stocks.append(stock)
            valid_weights.append(weight)
    
    if valid_weights:
        total_weight = sum(valid_weights)
        if total_weight != 100 and total_weight > 0:
            valid_weights = [w/total_weight*100 for w in valid_weights]
    
    benchmark = st.text_input("Benchmark", value="^NSEI")
    risk_free_rate = st.slider("Risk-Free Rate (%)", 0.0, 10.0, 5.0, 0.5) / 100
    
    analyze_button = st.button("🔍 Analyze Portfolio", type="primary")

# Main content
if analyze_button and valid_stocks and valid_weights:
    with st.spinner("Fetching data and analyzing portfolio..."):
        try:
            st.info(f"Fetching data for: {', '.join(valid_stocks)}")
            
            # 1. Fetch data
            fetcher = DataFetcher(valid_stocks, benchmark)
            price_data = fetcher.fetch_data()
            
            if price_data.empty:
                st.error("No data could be fetched. Please try different tickers.")
                st.stop()
            
            # Get available stocks
            available_stocks = [col for col in valid_stocks if col in price_data.columns]
            if not available_stocks:
                st.error(f"None of the tickers could be found. Please check the ticker symbols.")
                st.info("Try: RELIANCE.NS, TCS.NS, INFY.NS, HDFCBANK.NS, ICICIBANK.NS")
                st.stop()
            
            # Filter to available stocks
            valid_stocks = [s for s in valid_stocks if s in price_data.columns]
            valid_weights = [valid_weights[valid_stocks.index(s)] for s in valid_stocks]
            
            # Normalize
            total_weight = sum(valid_weights)
            if total_weight != 100 and total_weight > 0:
                valid_weights = [w/total_weight*100 for w in valid_weights]
            
            # 2. Calculate returns
            returns_data = price_data.pct_change().dropna()
            
            if 'benchmark' in returns_data.columns:
                benchmark_returns = returns_data['benchmark']
            else:
                benchmark_returns = None
                st.warning("No benchmark data available.")
            
            stock_returns = returns_data[valid_stocks]
            
            # 3. Analyze portfolio
            analyzer = PortfolioAnalyzer(stock_returns, benchmark_returns, valid_weights)
            portfolio_returns = analyzer.calculate_portfolio_returns()
            metrics = analyzer.get_all_metrics(portfolio_returns)
            
            # 4. Sector allocation
            sector_mapper = SectorMapper()
            sector_allocation = sector_mapper.get_sector_allocation(valid_stocks, valid_weights)
            
            # 5. Health score
            health_calculator = HealthScoreCalculator(metrics, valid_weights, sector_allocation)
            health_score = health_calculator.get_health_score()
            
            # 6. Recommendations
            rec_engine = RecommendationEngine(metrics, health_score, sector_allocation)
            recommendations = rec_engine.generate_recommendations()
            
            # ============================================================
            # === DISPLAY SECTION 1: Portfolio Overview ===
            # ============================================================
            st.subheader("📈 Portfolio Overview")
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Health Score", f"{health_score['score']}/100", health_score['rating'])
            with col2:
                st.metric("Total Return", f"{metrics['Total Return']*100:.1f}%")
            with col3:
                st.metric("CAGR", f"{metrics['CAGR']*100:.1f}%")
            with col4:
                st.metric("Sharpe Ratio", f"{metrics['Sharpe Ratio']:.2f}")
            
            # ============================================================
            # === DISPLAY SECTION 2: Charts ===
            # ============================================================
            col1, col2 = st.columns(2)
            
            with col1:
                # Portfolio growth
                cumulative_returns = (1 + portfolio_returns).cumprod()
                fig = go.Figure()
                fig.add_trace(go.Scatter(x=cumulative_returns.index, y=cumulative_returns.values,
                                        mode='lines', name='Portfolio', line=dict(color='blue', width=2)))
                if benchmark_returns is not None:
                    benchmark_cumulative = (1 + benchmark_returns).cumprod()
                    fig.add_trace(go.Scatter(x=benchmark_cumulative.index, y=benchmark_cumulative.values,
                                            mode='lines', name='Benchmark', line=dict(color='gray', width=1.5, dash='dash')))
                fig.update_layout(title='Portfolio Growth', xaxis_title='Date', yaxis_title='Cumulative Return')
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                # Drawdown
                cumulative = (1 + portfolio_returns).cumprod()
                running_max = cumulative.expanding().max()
                drawdown = (cumulative - running_max) / running_max * 100
                fig = go.Figure()
                fig.add_trace(go.Scatter(x=drawdown.index, y=drawdown.values,
                                        mode='lines', name='Drawdown', fill='tozeroy', line=dict(color='red', width=1)))
                fig.update_layout(title='Portfolio Drawdown', xaxis_title='Date', yaxis_title='Drawdown %')
                st.plotly_chart(fig, use_container_width=True)
            
            # ============================================================
            # === DISPLAY SECTION 3: Metrics Table ===
            # ============================================================
            st.subheader("📊 Portfolio Metrics")
            metrics_df = pd.DataFrame({
                'Metric': ['Total Return', 'CAGR', 'Annualized Return', 'Annualized Volatility',
                          'Sharpe Ratio', 'Sortino Ratio', 'Max Drawdown', 'Beta', 'Alpha'],
                'Value': [f"{metrics['Total Return']*100:.1f}%", 
                         f"{metrics['CAGR']*100:.1f}%",
                         f"{metrics['Annualized Return']*100:.1f}%",
                         f"{metrics['Annualized Volatility']*100:.1f}%",
                         f"{metrics['Sharpe Ratio']:.2f}",
                         f"{metrics['Sortino Ratio']:.2f}",
                         f"{metrics['Max Drawdown']*100:.1f}%",
                         f"{metrics['Beta']:.2f}" if metrics['Beta'] is not None else "N/A",
                         f"{metrics['Alpha']*100:.2f}%" if metrics['Alpha'] is not None else "N/A"]
            })
            st.dataframe(metrics_df, use_container_width=True)
            
            # ============================================================
            # === DISPLAY SECTION 4: Health Score Breakdown ===
            # ============================================================
            st.subheader("🏥 Health Score Breakdown")
            health_df = pd.DataFrame({
                'Factor': list(health_score['breakdown'].keys()),
                'Score': list(health_score['breakdown'].values())
            })
            fig = px.bar(health_df, x='Factor', y='Score', 
                        title='Portfolio Health Factors',
                        color='Score', color_continuous_scale='RdYlGn',
                        text='Score')
            fig.update_traces(textposition='outside')
            st.plotly_chart(fig, use_container_width=True)
            
            # ============================================================
            # === DISPLAY SECTION 5: Sector Allocation ===
            # ============================================================
            if sector_allocation:
                st.subheader("🏢 Sector Allocation")
                sector_df = pd.DataFrame({
                    'Sector': list(sector_allocation.keys()),
                    'Allocation %': list(sector_allocation.values())
                })
                fig = px.pie(sector_df, values='Allocation %', names='Sector', 
                            title='Sector Distribution', hole=0.3)
                st.plotly_chart(fig, use_container_width=True)
            
            # ============================================================
            # === DISPLAY SECTION 6: Recommendations ===
            # ============================================================
            st.subheader("💡 Personalized Recommendations")
            for rec in recommendations:
                with st.expander(f"{rec['type']} - {rec['title']}", 
                               expanded=True if rec['severity'] == 'high' else False):
                    st.write(f"**Issue:** {rec['detail']}")
                    st.write(f"**Action:** {rec['action']}")
            
            # ============================================================
            # === DISPLAY SECTION 7: PORTFOLIO REBALANCING & OPTIMIZATION ===
            # ============================================================
            st.subheader("🔄 Portfolio Rebalancing & Optimization")
            
            # Check if we have at least 2 stocks for optimization
            if len(valid_stocks) >= 2:
                try:
                    # Create optimizer
                    optimizer = PortfolioOptimizer(stock_returns, risk_free_rate)
                    
                    # Get optimal weights (max Sharpe)
                    optimal_weights = optimizer.maximize_sharpe_ratio()
                    
                    # Calculate current portfolio performance
                    current_return = metrics['Annualized Return']
                    current_vol = metrics['Annualized Volatility']
                    current_sharpe = metrics['Sharpe Ratio']
                    
                    # Calculate optimal portfolio performance
                    optimal_returns = (stock_returns * optimal_weights).sum(axis=1)
                    optimal_metrics = analyzer.get_all_metrics(optimal_returns)
                    
                    # --- Performance Comparison ---
                    st.write("**📊 Performance Comparison**")
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        improvement_sharpe = optimal_metrics['Sharpe Ratio'] - current_sharpe
                        st.metric(
                            "Sharpe Ratio", 
                            f"{current_sharpe:.2f} → {optimal_metrics['Sharpe Ratio']:.2f}",
                            delta=f"+{improvement_sharpe:.2f}" if improvement_sharpe > 0 else f"{improvement_sharpe:.2f}"
                        )
                    
                    with col2:
                        improvement_return = (optimal_metrics['Annualized Return'] - current_return) * 100
                        st.metric(
                            "Expected Return", 
                            f"{current_return*100:.1f}% → {optimal_metrics['Annualized Return']*100:.1f}%",
                            delta=f"+{improvement_return:.1f}%" if improvement_return > 0 else f"{improvement_return:.1f}%"
                        )
                    
                    with col3:
                        improvement_vol = (optimal_metrics['Annualized Volatility'] - current_vol) * 100
                        st.metric(
                            "Volatility", 
                            f"{current_vol*100:.1f}% → {optimal_metrics['Annualized Volatility']*100:.1f}%",
                            delta=f"{improvement_vol:.1f}%" if improvement_vol < 0 else f"+{improvement_vol:.1f}%"
                        )
                    
                    # --- Weight Comparison Table ---
                    st.write("**📊 Current vs Optimal Allocation**")
                    
                    # Create comparison DataFrame
                    comparison_data = []
                    
                    for stock, current_w, opt_w in zip(valid_stocks, valid_weights, optimal_weights * 100):
                        change = opt_w - current_w
                        comparison_data.append({
                            'Stock': stock,
                            'Current %': f"{current_w:.1f}",
                            'Optimal %': f"{opt_w:.1f}",
                            'Change %': change,
                            'Action': '🔴 SELL' if change < -1 else '🟢 BUY' if change > 1 else '✅ HOLD'
                        })
                    
                    comp_df = pd.DataFrame(comparison_data)
                    st.dataframe(comp_df, use_container_width=True)
                    
                    # --- Rebalancing Instructions ---
                    st.write("**📝 Rebalancing Instructions**")
                    
                    # Check if portfolio needs rebalancing (any stock change > 5%)
                    needs_rebalancing = any(abs(float(row['Change %'])) > 5 for _, row in comp_df.iterrows())
                    
                    if needs_rebalancing:
                        st.warning("⚠️ Your portfolio needs rebalancing. Here's what to do:")
                        
                        # Create rebalancing table with actions
                        for _, row in comp_df.iterrows():
                            change = float(row['Change %'])
                            if abs(change) > 5:
                                current_w = float(row['Current %'])
                                opt_w = float(row['Optimal %'])
                                if change > 0:
                                    st.info(f"**🟢 BUY** {row['Stock']}: Increase from {current_w:.1f}% to {opt_w:.1f}% (Add {change:.1f}% more)")
                                else:
                                    st.warning(f"**🔴 SELL** {row['Stock']}: Decrease from {current_w:.1f}% to {opt_w:.1f}% (Sell {abs(change):.1f}%)")
                    else:
                        st.success("✅ Your portfolio is already well-optimized! No major rebalancing needed.")
                    
                    # --- Efficient Frontier Visualization ---
                    st.write("**📈 Efficient Frontier**")
                    
                    # Get efficient frontier points
                    returns_list, volatilities = optimizer.efficient_frontier_points()
                    
                    if returns_list and volatilities:
                        fig = go.Figure()
                        
                        # Efficient Frontier curve
                        fig.add_trace(go.Scatter(
                            x=volatilities, 
                            y=returns_list,
                            mode='lines',
                            name='Efficient Frontier',
                            line=dict(color='green', width=3)
                        ))
                        
                        # Current portfolio
                        fig.add_trace(go.Scatter(
                            x=[current_vol], 
                            y=[current_return],
                            mode='markers',
                            name='Current Portfolio',
                            marker=dict(size=15, color='blue', symbol='circle', line=dict(width=2, color='darkblue'))
                        ))
                        
                        # Optimal portfolio
                        opt_vol = optimal_metrics['Annualized Volatility']
                        opt_ret = optimal_metrics['Annualized Return']
                        fig.add_trace(go.Scatter(
                            x=[opt_vol], 
                            y=[opt_ret],
                            mode='markers',
                            name='Optimal Portfolio (Max Sharpe)',
                            marker=dict(size=20, color='red', symbol='star', line=dict(width=2, color='darkred'))
                        ))
                        
                        fig.update_layout(
                            title='Efficient Frontier: Current vs Optimal Portfolio',
                            xaxis_title='Annualized Volatility (Risk)',
                            yaxis_title='Annualized Return',
                            hovermode='closest'
                        )
                        
                        st.plotly_chart(fig, use_container_width=True)
                    else:
                        st.info("Could not generate efficient frontier. Try with more stocks.")
                    
                    # --- Risk Contribution Analysis ---
                    st.write("**🎯 Risk Contribution Analysis**")
                    
                    # Calculate risk contribution
                    cov_matrix = stock_returns.cov() * 252
                    portfolio_vol = np.sqrt(np.dot(optimal_weights.T, np.dot(cov_matrix, optimal_weights)))
                    
                    risk_contributions = []
                    for i, stock in enumerate(valid_stocks):
                        marginal_contrib = np.dot(cov_matrix, optimal_weights)[i] / portfolio_vol
                        risk_contrib = optimal_weights[i] * marginal_contrib
                        risk_pct = risk_contrib / portfolio_vol * 100
                        
                        risk_contributions.append({
                            'Stock': stock,
                            'Weight %': f"{optimal_weights[i] * 100:.1f}",
                            'Risk %': f"{risk_pct:.1f}",
                            'Risk/Return Ratio': f"{(risk_pct / (optimal_weights[i] * 100)):.2f}" if optimal_weights[i] > 0 else "N/A"
                        })
                    
                    risk_df = pd.DataFrame(risk_contributions)
                    st.dataframe(risk_df, use_container_width=True)
                    
                    st.caption("""
                    **Understanding Risk Contribution:**
                    - **Risk %** = How much each stock contributes to total portfolio risk
                    - **Risk/Return Ratio** = Risk per unit of allocation (lower is better)
                    - If a stock has high Risk % but low Weight %, it's inefficient
                    """)
                    
                except Exception as e:
                    st.warning(f"Could not perform optimization: {str(e)}")
                    st.info("Optimization requires at least 2 stocks with sufficient historical data.")
            else:
                st.info("ℹ️ Add at least 2 stocks to see portfolio optimization and rebalancing recommendations.")
            
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
            st.info("""
            **Troubleshooting:**
            1. Check internet connection
            2. For Indian stocks use: RELIANCE.NS, TCS.NS, INFY.NS
            3. For US stocks use: AAPL, MSFT, GOOGL
            4. Try: RELIANCE.NS and TCS.NS first
            """)
else:
    st.info("👈 Enter your portfolio details and click 'Analyze Portfolio'")
    
    st.subheader("📝 Try this example:")
    st.code("""
    Stocks: RELIANCE.NS, TCS.NS, INFY.NS, HDFCBANK.NS, ICICIBANK.NS
    Weights: 25, 20, 20, 20, 15
    Benchmark: ^NSEI
    """)