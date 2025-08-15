import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
import numpy as np

# Page configuration
st.set_page_config(
    page_title="Financial Charting Tool",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Force deployment refresh

# Title and description
st.title("📈 Financial Charting Tool")
st.markdown("Real-time stock, ETF, and mutual fund analysis with interactive charts")

# Sidebar for controls
with st.sidebar:
    st.header("Chart Configuration")
    
    # Mode selection
    mode = st.radio(
        "Select Mode:",
        ["Single Symbol", "Multi-Symbol Comparison"],
        index=0
    )
    
    if mode == "Single Symbol":
        # Single symbol inputs
        symbol = st.text_input("Enter Symbol", value="VTI", help="e.g., AAPL, VTI, SPY").upper()
        
        period_options = {
            "1 Month": "1mo",
            "3 Months": "3mo", 
            "6 Months": "6mo",
            "YTD": "ytd",
            "1 Year": "1y",
            "2 Years": "2y",
            "5 Years": "5y"
        }
        
        period_label = st.selectbox("Time Period", list(period_options.keys()), index=3)
        period = period_options[period_label]
        
        chart_type = st.selectbox(
            "Chart Type",
            ["Candlestick", "Line Chart", "OHLC"],
            index=0
        )
        
    else:
        # Multi-symbol comparison
        symbols_input = st.text_area(
            "Enter Symbols (one per line or comma-separated)", 
            value="VTI\nBRK-B\nHARD",
            help="Enter multiple symbols to compare"
        )
        
        # Parse symbols
        if '\n' in symbols_input:
            symbols = [s.strip().upper() for s in symbols_input.split('\n') if s.strip()]
        else:
            symbols = [s.strip().upper() for s in symbols_input.split(',') if s.strip()]
            
        period_options = {
            "1 Month": "1mo",
            "3 Months": "3mo",
            "6 Months": "6mo", 
            "YTD": "ytd",
            "1 Year": "1y",
            "2 Years": "2y"
        }
        
        period_label = st.selectbox("Time Period", list(period_options.keys()), index=3)
        period = period_options[period_label]

# Main content area
if st.sidebar.button("📊 Draw Chart", type="primary", use_container_width=True):
    
    if mode == "Single Symbol":
        if symbol:
            try:
                with st.spinner(f"Fetching data for {symbol}..."):
                    # Download data
                    ticker = yf.Ticker(symbol)
                    data = ticker.history(period=period)
                    
                    if data.empty:
                        st.error(f"No data found for symbol: {symbol}")
                    else:
                        # Create main chart
                        col1, col2 = st.columns([3, 1])
                        
                        with col1:
                            st.subheader(f"{symbol} - {period_label}")
                            
                            fig = go.Figure()
                            
                            if chart_type == "Candlestick":
                                fig.add_trace(go.Candlestick(
                                    x=data.index,
                                    open=data['Open'],
                                    high=data['High'],
                                    low=data['Low'],
                                    close=data['Close'],
                                    name=symbol,
                                    increasing_line_color='#00d4aa',
                                    decreasing_line_color='#ff6b6b'
                                ))
                            elif chart_type == "OHLC":
                                # Custom OHLC implementation with proper bars
                                # Calculate appropriate tick width based on data range
                                date_range = data.index[-1] - data.index[0]
                                tick_width = date_range / (len(data) * 8)  # Proportional to data density
                                
                                # Create OHLC bars
                                for i, (date, row) in enumerate(data.iterrows()):
                                    color = '#00d4aa' if row['Close'] >= row['Open'] else '#ff6b6b'
                                    
                                    # High-Low vertical line
                                    fig.add_trace(go.Scatter(
                                        x=[date, date],
                                        y=[row['Low'], row['High']],
                                        mode='lines',
                                        line=dict(color=color, width=2),
                                        showlegend=False,
                                        hoverinfo='skip'
                                    ))
                                    
                                    # Open tick (left horizontal line)
                                    fig.add_trace(go.Scatter(
                                        x=[date - tick_width, date],
                                        y=[row['Open'], row['Open']],
                                        mode='lines',
                                        line=dict(color=color, width=3),
                                        showlegend=False,
                                        hoverinfo='skip'
                                    ))
                                    
                                    # Close tick (right horizontal line)
                                    fig.add_trace(go.Scatter(
                                        x=[date, date + tick_width],
                                        y=[row['Close'], row['Close']],
                                        mode='lines',
                                        line=dict(color=color, width=3),
                                        showlegend=False,
                                        hoverinfo='skip'
                                    ))
                                
                                # Add invisible scatter for hover info
                                fig.add_trace(go.Scatter(
                                    x=data.index,
                                    y=data['Close'],
                                    mode='markers',
                                    marker=dict(size=0, opacity=0),
                                    name=symbol,
                                    customdata=list(zip(data['Open'], data['High'], data['Low'], data['Close'])),
                                    hovertemplate="<b>%{fullData.name}</b><br>" +
                                                "Date: %{x}<br>" +
                                                "Open: $%{customdata[0]:.2f}<br>" +
                                                "High: $%{customdata[1]:.2f}<br>" +
                                                "Low: $%{customdata[2]:.2f}<br>" +
                                                "Close: $%{customdata[3]:.2f}<br>" +
                                                "<extra></extra>"
                                ))
                            else:  # Line Chart
                                fig.add_trace(go.Scatter(
                                    x=data.index,
                                    y=data['Close'],
                                    mode='lines',
                                    name=f"{symbol} Close",
                                    line=dict(color='#1f77b4', width=2)
                                ))
                            
                            fig.update_layout(
                                title=f"{symbol} Stock Price - {chart_type}",
                                xaxis_title="Date",
                                template="plotly_white",
                                height=500,
                                showlegend=False,
                                xaxis_rangeslider_visible=False
                            )
                            
                            # Add invisible trace to activate right Y-axis
                            fig.add_trace(go.Scatter(
                                x=data.index,
                                y=data['Close'],
                                yaxis="y2",
                                mode='lines',
                                line=dict(color='rgba(0,0,0,0)'),  # Invisible line
                                showlegend=False,
                                hoverinfo='skip'
                            ))
                            
                            # Update Y-axes to show SAME scale on both sides
                            fig.update_layout(
                                yaxis=dict(
                                    title="Price ($)",
                                    side="left"
                                ),
                                yaxis2=dict(
                                    title="Price ($)",
                                    overlaying="y", 
                                    side="right",
                                    showgrid=False
                                )
                            )
                            
                            st.plotly_chart(fig, use_container_width=True)
                            
                            # Volume chart
                            st.subheader("Trading Volume")
                            vol_fig = go.Figure()
                            vol_fig.add_trace(go.Bar(
                                x=data.index,
                                y=data['Volume'],
                                name="Volume",
                                marker_color='rgba(31, 119, 180, 0.6)'
                            ))
                            
                            vol_fig.update_layout(
                                title="Trading Volume",
                                xaxis_title="Date",
                                template="plotly_white",
                                height=200,
                                showlegend=False
                            )
                            
                            # Add invisible trace to activate right Y-axis for volume
                            vol_fig.add_trace(go.Bar(
                                x=data.index,
                                y=data['Volume'],
                                yaxis="y2",
                                marker_color='rgba(0,0,0,0)',  # Invisible bars
                                showlegend=False,
                                hoverinfo='skip'
                            ))
                            
                            # Update Y-axes to show SAME scale on both sides
                            vol_fig.update_layout(
                                yaxis=dict(
                                    title="Volume",
                                    side="left"
                                ),
                                yaxis2=dict(
                                    title="Volume",
                                    overlaying="y",
                                    side="right",
                                    showgrid=False
                                )
                            )
                            
                            st.plotly_chart(vol_fig, use_container_width=True)
                        
                        with col2:
                            # Stock info panel
                            st.subheader("Stock Information")
                            
                            # Get current price info
                            current_price = data['Close'].iloc[-1]
                            previous_price = data['Close'].iloc[-2] if len(data) > 1 else current_price
                            price_change = current_price - previous_price
                            price_change_pct = (price_change / previous_price) * 100
                            
                            # Display metrics
                            st.metric(
                                label="Current Price",
                                value=f"${current_price:.2f}",
                                delta=f"{price_change:+.2f} ({price_change_pct:+.2f}%)"
                            )
                            
                            # Additional metrics
                            high_52w = data['High'].max()
                            low_52w = data['Low'].min()
                            avg_volume = data['Volume'].mean()
                            
                            st.metric("52W High", f"${high_52w:.2f}")
                            st.metric("52W Low", f"${low_52w:.2f}")
                            st.metric("Avg Volume", f"{avg_volume:,.0f}")
                            
                            # Get company info
                            try:
                                info = ticker.info
                                if 'longName' in info:
                                    st.write(f"**Company:** {info['longName']}")
                                if 'sector' in info:
                                    st.write(f"**Sector:** {info['sector']}")
                                if 'marketCap' in info:
                                    market_cap = info['marketCap']
                                    if market_cap > 1e12:
                                        st.write(f"**Market Cap:** ${market_cap/1e12:.2f}T")
                                    elif market_cap > 1e9:
                                        st.write(f"**Market Cap:** ${market_cap/1e9:.2f}B")
                                    else:
                                        st.write(f"**Market Cap:** ${market_cap/1e6:.2f}M")
                            except:
                                pass
            
            except Exception as e:
                st.error(f"Error fetching data: {str(e)}")
        else:
            st.warning("Please enter a symbol")
    
    else:  # Multi-symbol comparison
        if symbols and len(symbols) > 1:
            try:
                with st.spinner(f"Fetching data for {len(symbols)} symbols..."):
                    # Download data for all symbols
                    comparison_data = {}
                    valid_symbols = []
                    
                    for symbol in symbols:
                        try:
                            ticker = yf.Ticker(symbol)
                            data = ticker.history(period=period)
                            if not data.empty:
                                comparison_data[symbol] = data['Close']
                                valid_symbols.append(symbol)
                        except:
                            st.warning(f"Could not fetch data for {symbol}")
                    
                    if valid_symbols:
                        # Create comparison DataFrame
                        df = pd.DataFrame(comparison_data)
                        
                        # Calculate percentage change from start
                        pct_change_df = df.pct_change(periods=len(df)-1).iloc[-1:] * 100
                        for col in df.columns:
                            df[f"{col}_pct"] = ((df[col] / df[col].iloc[0]) - 1) * 100
                        
                        # Create comparison chart
                        st.subheader(f"Multi-Symbol Comparison - {period_label}")
                        st.markdown("**Percentage change from period start**")
                        
                        fig = go.Figure()
                        
                        colors = px.colors.qualitative.Set1[:len(valid_symbols)]
                        
                        for i, symbol in enumerate(valid_symbols):
                            fig.add_trace(go.Scatter(
                                x=df.index,
                                y=df[f"{symbol}_pct"],
                                mode='lines',
                                name=symbol,
                                line=dict(color=colors[i], width=2),
                                hovertemplate=f"<b>{symbol}</b><br>" +
                                            "Date: %{x}<br>" +
                                            "Change: %{y:.2f}%<br>" +
                                            "<extra></extra>"
                            ))
                        
                        fig.update_layout(
                            title="Symbol Performance Comparison",
                            xaxis_title="Date",
                            template="plotly_white",
                            height=600,
                            legend=dict(
                                yanchor="top",
                                y=0.99,
                                xanchor="left",
                                x=0.01
                            ),
                            hovermode='x unified'
                        )
                        
                        # Get the Y-axis range from the data to ensure both axes match exactly
                        all_values = []
                        for symbol in valid_symbols:
                            all_values.extend(df[f"{symbol}_pct"].tolist())
                        y_min = min(all_values)
                        y_max = max(all_values)
                        
                        # Add some padding
                        y_padding = (y_max - y_min) * 0.1
                        y_range = [y_min - y_padding, y_max + y_padding]
                        
                        # Add minimal invisible trace to activate right Y-axis
                        fig.add_trace(go.Scatter(
                            x=[df.index[0], df.index[-1]],  # Just first and last points
                            y=[y_range[0], y_range[1]],     # Just min and max values
                            yaxis="y2",
                            mode='markers',
                            marker=dict(size=0, opacity=0),  # Completely invisible
                            showlegend=False,
                            hoverinfo='skip'
                        ))
                        
                        # Update Y-axes to show SAME scale on both sides with exact range
                        fig.update_layout(
                            yaxis=dict(
                                title="Percentage Change (%)",
                                side="left",
                                range=y_range
                            ),
                            yaxis2=dict(
                                title="Percentage Change (%)",
                                overlaying="y", 
                                side="right",
                                showgrid=False,
                                range=y_range  # Force same range
                            )
                        )
                        
                        # Add zero line
                        fig.add_hline(y=0, line_dash="dash", line_color="gray", opacity=0.5)
                        
                        st.plotly_chart(fig, use_container_width=True)
                        
                        # Performance summary table
                        st.subheader("Performance Summary")
                        
                        summary_data = []
                        for symbol in valid_symbols:
                            current_price = df[symbol].iloc[-1]
                            start_price = df[symbol].iloc[0]
                            total_return = ((current_price / start_price) - 1) * 100
                            
                            summary_data.append({
                                "Symbol": symbol,
                                "Start Price": f"${start_price:.2f}",
                                "Current Price": f"${current_price:.2f}",
                                "Total Return": f"{total_return:+.2f}%"
                            })
                        
                        summary_df = pd.DataFrame(summary_data)
                        st.dataframe(summary_df, use_container_width=True, hide_index=True)
                        
                    else:
                        st.error("No valid symbols found")
                        
            except Exception as e:
                st.error(f"Error fetching comparison data: {str(e)}")
        else:
            st.warning("Please enter at least 2 symbols for comparison")

else:
    # Welcome screen
    st.markdown("""
    ## Welcome to the Financial Charting Tool! 📊
    
    **Features:**
    - 📈 **Single Symbol Analysis**: Detailed candlestick, OHLC, and line charts
    - 🔍 **Multi-Symbol Comparison**: Compare percentage performance of multiple stocks
    - 📊 **Real-time Data**: Powered by Yahoo Finance
    - 🎯 **Interactive Charts**: Zoom, pan, and hover for details
    
    ### How to Use:
    1. **Choose your mode** in the sidebar (Single Symbol or Multi-Symbol Comparison)
    2. **Enter symbol(s)** - stocks, ETFs, mutual funds (e.g., AAPL, VTI, SPY)
    3. **Select time period** - from 1 month to 5 years
    4. **Click "Draw Chart"** to generate your analysis
    
    ### Popular Symbols:
    - **Stocks**: AAPL, GOOGL, MSFT, TSLA, NVDA
    - **ETFs**: VTI, SPY, QQQ, VEA, BND
    - **Indices**: ^GSPC (S&P 500), ^DJI (Dow Jones), ^IXIC (NASDAQ)
    
    👈 **Get started with the controls in the sidebar!**
    """)
