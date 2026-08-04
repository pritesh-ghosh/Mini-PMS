# 📊 Smart Portfolio Analyzer

> A professional-grade portfolio analysis tool for wealth management and investment advisors

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.25.0-red.svg)](https://streamlit.io/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

## 📖 Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Screenshots](#screenshots)
- [Technology Stack](#technology-stack)
- [Installation](#installation)
- [Usage Guide](#usage-guide)
- [Understanding the Metrics](#understanding-the-metrics)
- [Project Structure](#project-structure)
- [How It Works](#how-it-works)
- [Finance Concepts Implemented](#finance-concepts-implemented)
- [Future Roadmap](#future-roadmap)
- [Contributing](#contributing)
- [License](#license)

---

## 🎯 Overview

**Smart Portfolio Analyzer** is a Python-based application that helps investment advisors and individual investors make better portfolio decisions. It automates the collection of market data, calculates professional-grade financial metrics, and provides actionable recommendations—all through an interactive web dashboard.

### What Problem Does It Solve?

- **For Investors**: Get professional portfolio analysis without expensive software
- **For Advisors**: Generate client-ready reports and recommendations quickly
- **For Students**: Learn financial concepts through practical implementation
- **For Analysts**: Automate repetitive portfolio analysis tasks

### Who Is It For?

- 💼 Wealth Management Professionals
- 📊 Investment Analysts
- 🎓 Finance Students
- 💰 Individual Investors
- 🏦 Financial Advisors

---

## ✨ Features

### 1. 📥 Portfolio Input
- Enter stocks with custom weights
- Automatic weight normalization to 100%
- Benchmark selection (default: NIFTY 50)
- Risk-free rate adjustment

### 2. 📈 Performance Analysis
- **Return Metrics**: Total Return, CAGR, Annualized Return
- **Risk Metrics**: Volatility, Maximum Drawdown
- **Risk-Adjusted Metrics**: Sharpe Ratio, Sortino Ratio
- **Market Metrics**: Beta (vs Benchmark), Alpha

### 3. 🏥 Portfolio Health Score (0-100)
| Factor | Weight | What It Measures |
|--------|--------|------------------|
| Diversification | 30% | Sector and stock distribution |
| Volatility | 25% | Price stability |
| Concentration | 20% | Single-stock risk |
| Drawdown | 15% | Downside protection |
| Performance | 10% | Risk-adjusted returns |

**Scoring Categories:**
- 🟢 80-100: Excellent Portfolio
- 🔵 65-79: Good Portfolio
- 🟡 50-64: Fair Portfolio
- 🟠 35-49: Needs Improvement
- 🔴 < 35: High Risk

### 4. 💡 Smart Recommendations
- Sector concentration alerts
- Risk-adjusted return feedback
- Volatility management suggestions
- Drawdown protection advice
- Portfolio rebalancing recommendations

### 5. 🔄 Portfolio Rebalancing & Optimization
- **Optimal Weights**: Finds allocation maximizing Sharpe Ratio
- **Rebalancing Instructions**: Exact BUY/SELL recommendations
- **Efficient Frontier**: Visual of optimal risk-return trade-offs
- **Risk Contribution**: Identify which stocks drive portfolio risk

### 6. 📊 Interactive Visualizations
- Portfolio Growth vs Benchmark
- Drawdown Analysis
- Sector Allocation Pie Chart
- Health Score Breakdown
- Efficient Frontier Chart
- Correlation Heatmap (coming soon)

### 7. 📋 Professional Metrics Table
- All key metrics in one view
- Interactive sorting
- Export-ready format

---

## 📸 Screenshots

### Portfolio Overview Dashboard
```
┌─────────────────────────────────────────────────────────────┐
│  📊 Smart Portfolio Analyzer                              │
│  Professional portfolio analysis for wealth management    │
├─────────────────────────────────────────────────────────────┤
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐ │
│  │Health    │  │Total     │  │CAGR      │  │Sharpe    │ │
│  │Score     │  │Return    │  │          │  │Ratio     │ │
│  │82.5/100  │  │28.5%     │  │8.7%      │  │0.85      │ │
│  │Excellent │  │          │  │          │  │          │ │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘ │
├─────────────────────────────────────────────────────────────┤
│  📈 Portfolio Growth     📉 Portfolio Drawdown            │
│  [Interactive Chart]     [Interactive Chart]              │
├─────────────────────────────────────────────────────────────┤
│  💡 Personalized Recommendations                          │
│  ▼ ⚠️ Sector Concentration - High Energy Exposure         │
│    Issue: 25% in Energy, above 20% threshold             │
│    Action: Diversify with technology/financial stocks    │
├─────────────────────────────────────────────────────────────┤
│  🔄 Portfolio Rebalancing & Optimization                  │
│  📊 Current vs Optimal Allocation                         │
│  ┌──────────┬─────────┬──────────┬──────────┬──────────┐ │
│  │ Stock    │Current %│Optimal % │Change %  │Action    │ │
│  │RELIANCE  │25.0     │15.0      │-10.0     │🔴 SELL   │ │
│  │TCS       │20.0     │30.0      │+10.0     │🟢 BUY    │ │
│  └──────────┴─────────┴──────────┴──────────┴──────────┘ │
│  📈 Efficient Frontier                                    │
│  [Interactive Chart]                                      │
└─────────────────────────────────────────────────────────────┘
```

---

## 🛠️ Technology Stack

### Core Technologies
| Technology | Version | Purpose |
|------------|---------|---------|
| Python | 3.8+ | Core programming language |
| Streamlit | 1.25.0 | Interactive web framework |
| Pandas | 2.0.3 | Data manipulation |
| NumPy | 1.24.3 | Numerical computations |
| yfinance | 0.2.28 | Market data fetching |
| Plotly | 5.15.0 | Interactive visualizations |
| SciPy | 1.11.1 | Optimization algorithms |

### Additional Libraries
- **matplotlib**: Static chart generation
- **seaborn**: Statistical visualizations
- **scikit-learn**: Advanced analytics (future)
- **fpdf**: PDF report generation

---

## 🚀 Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)
- Internet connection (for data fetching)

### Step 1: Clone the Repository
```bash
git clone https://github.com/yourusername/portfolio-analyzer.git
cd portfolio-analyzer
```

### Step 2: Create Virtual Environment (Recommended)

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Verify Installation
```bash
python -c "import yfinance; print('✅ All dependencies installed!')"
```

### Step 5: Run the Application
```bash
streamlit run app.py
```

### Step 6: Open in Browser
The application will automatically open at: `http://localhost:8501`

---

## 📖 Usage Guide

### 1. Enter Your Portfolio

#### Example Portfolio (Indian Market):
```
Stocks: RELIANCE.NS, TCS.NS, INFY.NS, HDFCBANK.NS, ICICIBANK.NS
Weights: 25, 20, 20, 20, 15
Benchmark: ^NSEI (NIFTY 50)
Risk-Free Rate: 5.0%
```

#### Example Portfolio (US Market):
```
Stocks: AAPL, MSFT, GOOGL, AMZN, TSLA
Weights: 25, 25, 20, 20, 10
Benchmark: ^GSPC (S&P 500)
Risk-Free Rate: 4.0%
```

### 2. Understanding Your Results

#### Health Score
- **What it means**: Overall portfolio quality
- **How to use**: A score > 65 indicates a well-managed portfolio
- **Action**: Focus on the lowest-scoring components

#### Sharpe Ratio
- **> 1.0**: Good (portfolio beats risk-free rate)
- **> 2.0**: Excellent (very good risk-adjusted returns)
- **< 1.0**: Needs improvement

#### Beta
- **> 1.0**: More volatile than market
- **= 1.0**: Same as market
- **< 1.0**: Less volatile than market

#### Maximum Drawdown
- **< 10%**: Excellent downside protection
- **10-25%**: Moderate risk
- **> 35%**: High risk, needs attention

### 3. Rebalancing Your Portfolio

The rebalancing section shows:
1. **Current vs Optimal Allocation**: Where you are vs where you should be
2. **BUY/SELL Recommendations**: Exact actions to take
3. **Efficient Frontier**: Visual representation of risk-return trade-off
4. **Risk Contribution**: Which stocks drive portfolio risk

### 4. Interpreting Recommendations

| Recommendation | What It Means | What To Do |
|----------------|---------------|------------|
| High Sector Concentration | >40% in one sector | Add stocks from other sectors |
| Low Sharpe Ratio | <1.0 | Reduce risk or improve returns |
| High Volatility | >25% | Add defensive stocks |
| High Drawdown | >35% | Add bonds or gold |

---

## 📊 Understanding the Metrics

### Return Metrics

#### Total Return
- **Formula**: `(Final Value - Initial Value) / Initial Value`
- **What it shows**: Overall portfolio performance
- **Example**: If portfolio went from ₹1,00,000 to ₹1,28,500, total return = 28.5%

#### CAGR (Compound Annual Growth Rate)
- **Formula**: `(Final Value / Initial Value)^(1/years) - 1`
- **What it shows**: Smooth annualized return
- **Example**: 28.5% over 3 years = 8.7% CAGR

#### Annualized Return
- **Formula**: `Average Daily Return × 252`
- **What it shows**: Average yearly return
- **Why 252?**: Number of trading days in a year

### Risk Metrics

#### Annualized Volatility
- **Formula**: `Standard Deviation of Returns × √252`
- **What it shows**: Price fluctuation magnitude
- **Interpretation**: Higher = more risk

#### Maximum Drawdown
- **Formula**: `(Current Value - Peak Value) / Peak Value` (minimum)
- **What it shows**: Worst peak-to-trough loss
- **Example**: -32% means portfolio lost 32% from its peak

### Risk-Adjusted Metrics

#### Sharpe Ratio
- **Formula**: `(Return - Risk-Free Rate) / Volatility`
- **What it shows**: Return per unit of total risk
- **Interpretation**: Higher is better (more return per risk)

#### Sortino Ratio
- **Formula**: `(Return - Risk-Free Rate) / Downside Deviation`
- **What it shows**: Return per unit of downside risk
- **Difference from Sharpe**: Only penalizes bad volatility

### Market Metrics

#### Beta
- **Formula**: `Covariance(Portfolio, Market) / Variance(Market)`
- **What it shows**: Market sensitivity
- **Interpretation**: 
  - 1.0 = Moves with market
  - 1.5 = 50% more volatile than market
  - 0.5 = 50% less volatile than market

#### Alpha
- **Formula**: `Portfolio Return - [Risk-Free + Beta × (Market Return - Risk-Free)]`
- **What it shows**: Excess return beyond expected
- **Interpretation**: Positive = outperformed, Negative = underperformed

---

## 📁 Project Structure

```
portfolio-analyzer/
│
├── app.py                          # Main Streamlit application
├── requirements.txt                # Python dependencies
├── README.md                       # This file
├── SETUP_GUIDE.md                  # Detailed setup instructions
│
├── data/
│   ├── __init__.py                # Makes data a package
│   ├── data_fetcher.py            # Fetches stock data from Yahoo Finance
│   └── sector_mapper.py           # Maps stocks to sectors/industries
│
├── analytics/
│   ├── __init__.py                # Makes analytics a package
│   ├── portfolio.py               # Core portfolio calculations
│   ├── optimizer.py               # Portfolio optimization (Efficient Frontier)
│   ├── advanced_risk.py           # Advanced risk metrics
│   ├── health_score.py            # Portfolio health scoring
│   └── recommendations.py         # Recommendation engine
│
├── visualization/
│   ├── __init__.py                # Makes visualization a package
│   └── charts.py                  # Chart generation functions
│
├── utils/
│   ├── __init__.py                # Makes utils a package
│   └── helpers.py                 # Utility functions
│
└── report/
    ├── __init__.py                # Makes report a package
    └── report_generator.py        # PDF report generation
```

### Module Descriptions

| Module | Purpose | Key Functions |
|--------|---------|---------------|
| **data/data_fetcher.py** | Fetch market data | Fetch prices, handle multiple ticker formats |
| **data/sector_mapper.py** | Map stocks to sectors | Get sector and industry information |
| **analytics/portfolio.py** | Core calculations | CAGR, Sharpe, Beta, Alpha |
| **analytics/optimizer.py** | Portfolio optimization | Max Sharpe, Efficient Frontier |
| **analytics/advanced_risk.py** | Advanced metrics | Omega, Calmar, Ulcer Index |
| **analytics/health_score.py** | Health scoring | 0-100 score with breakdown |
| **analytics/recommendations.py** | Generate advice | Personalized recommendations |
| **app.py** | Main application | Streamlit UI and orchestration |

---

## 🔧 How It Works

### Data Flow

```
1. User Input
   └── Stocks, Weights, Benchmark, Risk-Free Rate
         ↓
2. Data Collection (yfinance)
   └── Fetches 3 years of historical closing prices
         ↓
3. Returns Calculation
   └── Calculates daily returns from prices
         ↓
4. Portfolio Analysis
   ├── Return Metrics (CAGR, Total Return)
   ├── Risk Metrics (Volatility, Drawdown)
   ├── Risk-Adjusted Metrics (Sharpe, Sortino)
   └── Market Metrics (Beta, Alpha)
         ↓
5. Portfolio Optimization
   ├── Max Sharpe Portfolio
   ├── Efficient Frontier
   └── Risk Contribution Analysis
         ↓
6. Health Score
   ├── Diversification Score
   ├── Volatility Score
   ├── Concentration Score
   ├── Drawdown Score
   └── Performance Score
         ↓
7. Recommendations
   ├── Sector Concentration Warning
   ├── Sharpe Ratio Alert
   ├── Volatility Warning
   └── Rebalancing Instructions
         ↓
8. Display Results
   ├── Interactive Charts
   ├── Metrics Table
   ├── Health Score Breakdown
   └── Rebalancing Recommendations
```

### Key Algorithms

#### 1. Portfolio Optimization (Max Sharpe)
```python
Objective: Maximize (Portfolio Return - Risk-Free Rate) / Portfolio Volatility
Constraints: 
  - Sum of weights = 1 (100%)
  - 0 ≤ weight ≤ 1 (no short selling)
Method: Sequential Least Squares Programming (SLSQP)
```

#### 2. Efficient Frontier Generation
```python
For each target return:
  - Minimize Portfolio Volatility
  - Subject to: Weighted return = target return
  - Record resulting volatility
Result: Set of optimal portfolios
```

#### 3. Health Score Calculation
```python
Score = (Diversification × 0.30) + 
        (Volatility × 0.25) + 
        (Concentration × 0.20) + 
        (Drawdown × 0.15) + 
        (Performance × 0.10)
```

---

## 📈 Finance Concepts Implemented

### Modern Portfolio Theory (MPT)
- **Risk-Return Tradeoff**: Higher returns require higher risk
- **Efficient Frontier**: Optimal portfolios that maximize return for given risk
- **Diversification Benefit**: Uncorrelated assets reduce portfolio risk
- **Implementation**: PortfolioOptimizer class with optimization algorithms

### Capital Asset Pricing Model (CAPM)
- **Beta**: Measures systematic risk (market risk)
- **Alpha**: Measures excess return over benchmark
- **Risk-Free Rate**: Return on risk-free assets
- **Implementation**: PortfolioAnalyzer class with Beta/Alpha calculations

### Risk Management
- **Downside Risk**: Focus on negative returns (Sortino, Max Drawdown)
- **Tail Risk**: Extreme event probability (Skewness, Kurtosis)
- **Drawdown Analysis**: Loss severity and recovery time
- **Implementation**: AdvancedRiskMetrics class

### Portfolio Optimization
- **Mean-Variance Optimization**: Maximize Sharpe Ratio
- **Efficient Frontier**: Visualize optimal portfolios
- **Risk Contribution**: Identify risk drivers
- **Implementation**: PortfolioOptimizer class

### Performance Attribution
- **Sector Analysis**: Identify sector concentration
- **Risk Decomposition**: Understand risk sources
- **Performance Metrics**: Compare to benchmark
- **Implementation**: SectorMapper and RecommendationEngine

---

## 🔮 Future Roadmap

### Version 2.0 - Advanced Features
- [ ] AI-powered portfolio advisor
- [ ] Monte Carlo retirement simulations
- [ ] Efficient Frontier optimization with constraints
- [ ] Automated portfolio rebalancing
- [ ] Tax optimization (LTCG/STCG calculations)

### Version 3.0 - Enhanced Analytics
- [ ] DCF valuation engine
- [ ] Company screener
- [ ] Mutual fund analyzer
- [ ] News sentiment analysis
- [ ] LLM-based portfolio explanations

### Version 4.0 - Production Ready
- [ ] User authentication
- [ ] Portfolio tracking
- [ ] Email reports
- [ ] Mobile responsive design
- [ ] API integration with brokerages

---

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. **Fork the repository**
2. **Create a feature branch**
   ```bash
   git checkout -b feature/amazing-feature
   ```
3. **Make your changes**
4. **Test your changes**
5. **Commit your changes**
   ```bash
   git commit -m 'Add amazing feature'
   ```
6. **Push to the branch**
   ```bash
   git push origin feature/amazing-feature
   ```
7. **Open a Pull Request**

### Guidelines
- Follow PEP 8 style guide
- Write meaningful commit messages
- Add comments for complex logic
- Update documentation
- Write tests for new features

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- **Yahoo Finance**: For providing free market data through yfinance
- **Streamlit**: For making data apps accessible
- **Financial Mathematics Community**: For developing the concepts used
- **Open Source Community**: For the amazing libraries

---

## 📞 Contact

- **Author**: Pritesh Ghosh
- **Email**: priteshghosh2003@gmail.com

---

## ⭐ If you find this useful...

Please star the repository! It helps others discover the project.

---

## 📚 Additional Resources

- [Modern Portfolio Theory](https://www.investopedia.com/terms/m/modernportfoliotheory.asp)
- [Understanding Sharpe Ratio](https://www.investopedia.com/terms/s/sharperatio.asp)
- [Efficient Frontier Explained](https://www.investopedia.com/terms/e/efficientfrontier.asp)
- [yfinance Documentation](https://github.com/ranaroussi/yfinance)
- [Streamlit Documentation](https://docs.streamlit.io/)

---

**Built with ❤️ by Pritesh Ghosh**

---

*Last Updated: August 2026*