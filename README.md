# Financial Charting Tool 📈

A real-time financial charting application built with Streamlit and Plotly for analyzing stocks, ETFs, and mutual funds.

## Features

### 📊 Single Symbol Analysis
- **Candlestick Charts** - Traditional OHLC candle patterns with volume
- **OHLC Charts** - Open-High-Low-Close bar charts
- **Line Charts** - Simple price trend visualization
- **Volume Analysis** - Trading volume with price correlation
- **Real-time Metrics** - Current price, 52-week high/low, market cap

### 🔍 Multi-Symbol Comparison
- **Performance Comparison** - Percentage change from period start
- **Multiple Timeframes** - 1 month to 2 years
- **Interactive Charts** - Zoom, pan, hover for details
- **Performance Summary** - Tabular comparison of returns

### 🎯 Supported Assets
- **Stocks** - Individual company stocks (AAPL, GOOGL, MSFT, etc.)
- **ETFs** - Exchange-traded funds (VTI, SPY, QQQ, etc.)
- **Mutual Funds** - Fund symbols supported by Yahoo Finance
- **Indices** - Major market indices (^GSPC, ^DJI, ^IXIC)

## Quick Start

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Installation

1. **Clone or download** this repository
2. **Create virtual environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
4. **Run the application**:
   ```bash
   streamlit run app.py
   ```
5. **Open your browser** to `http://localhost:8501`

## Usage

### Single Symbol Analysis
1. Select **"Single Symbol"** mode in the sidebar
2. Enter a stock symbol (e.g., "VTI", "AAPL")
3. Choose your desired time period
4. Select chart type (Candlestick, Line, or OHLC)
5. Click **"📊 Draw Chart"**

### Multi-Symbol Comparison
1. Select **"Multi-Symbol Comparison"** mode
2. Enter multiple symbols (one per line or comma-separated)
3. Choose time period for comparison
4. Click **"📊 Draw Chart"**
5. View percentage performance comparison

## Technology Stack

- **Frontend**: Streamlit (Python web framework)
- **Charts**: Plotly (Interactive plotting library)
- **Data**: yfinance (Yahoo Finance API wrapper)
- **Analysis**: Pandas, NumPy

## Data Source

This application uses **Yahoo Finance** as its data source through the `yfinance` library. Data includes:
- Real-time and historical stock prices
- Trading volumes
- Company information
- Market indices

## Examples

### Popular Symbols to Try:

**Technology Stocks:**
- AAPL (Apple Inc.)
- GOOGL (Alphabet Inc.)
- MSFT (Microsoft Corp.)
- NVDA (NVIDIA Corp.)

**ETFs:**
- VTI (Total Stock Market ETF)
- SPY (S&P 500 ETF)
- QQQ (NASDAQ-100 ETF)
- VEA (Developed Markets ETF)

**Comparison Ideas:**
- Tech giants: AAPL, GOOGL, MSFT, AMZN
- Market ETFs: VTI, SPY, QQQ
- Sectors: XLF (Financial), XLE (Energy), XLK (Technology)

## License

This project is open source and available under the MIT License.

## Contributing

Contributions are welcome! Feel free to submit issues, feature requests, or pull requests.

---

**⚠️ Disclaimer**: This tool is for educational and informational purposes only. It should not be considered as financial advice. Always consult with a qualified financial advisor before making investment decisions.