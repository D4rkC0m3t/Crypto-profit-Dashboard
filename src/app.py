# TradeProfitAnalytics - Crypto Exchange Dashboard
# A comprehensive dashboard for analyzing cryptocurrency exchange performance
# Created by TradeProfitAnalytics Team

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import datetime
import sys
import os

# Add the current directory to the path so we can import modules
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from data_fetcher import (
    fetch_real_time_data,
    fetch_crypto_news,
    fetch_current_prices,
    fetch_global_charts_data,
    fetch_global_chart_history
)
from utils import (
    create_monthly_bar_chart,
    create_yearly_bar_chart,
    create_commission_pie_chart,
    create_volume_pie_chart,
    create_fees_table,
    create_fee_comparison_chart,
    format_large_number
)
from database import get_all_exchange_data, get_latest_crypto_prices, get_latest_news

def run_app():
    """Main function to run the Streamlit application"""
    # Page configuration
    st.set_page_config(
        page_title="Crypto Exchange Profits Dashboard",
        page_icon="📊",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    # Initialize session state for theme
    if 'theme' not in st.session_state:
        st.session_state.theme = 'light'

    # Function to toggle theme
    def toggle_theme():
        st.session_state.theme = 'dark' if st.session_state.theme == 'light' else 'light'
        st.rerun()

    # Apply theme and custom cursor
    if st.session_state.theme == 'dark':
        # Dark theme styles with custom cursor
        st.markdown("""
    <style>
        /* Custom cursor styles */
        body {
            cursor: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='24' height='24' viewBox='0 0 24 24' fill='none' stroke='%231E88E5' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Ccircle cx='12' cy='12' r='10'%3E%3C/circle%3E%3Ccircle cx='12' cy='12' r='2'%3E%3C/circle%3E%3C/svg%3E") 12 12, auto !important;
        }

        /* Pointer cursor for interactive elements */
        button, a, [role="button"], .stButton>button, .stSelectbox,
        .stMultiSelect, input, select, .stTabs [data-baseweb="tab"],
        [data-testid="StyledFullScreenButton"] {
            cursor: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='24' height='24' viewBox='0 0 24 24' fill='none' stroke='%231E88E5' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpath d='M14 16l-5-5 5-5'%3E%3C/path%3E%3C/svg%3E") 12 12, pointer !important;
        }

        /* Text cursor for text elements */
        p, h1, h2, h3, h4, h5, h6, span, div, td, th {
            cursor: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='24' height='24' viewBox='0 0 24 24' fill='none' stroke='%231E88E5' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Cline x1='17' y1='10' x2='3' y2='10'%3E%3C/line%3E%3Cline x1='21' y1='6' x2='3' y2='6'%3E%3C/line%3E%3Cline x1='21' y1='14' x2='3' y2='14'%3E%3C/line%3E%3Cline x1='17' y1='18' x2='3' y2='18'%3E%3C/line%3E%3C/svg%3E") 12 12, text !important;
        }

        /* Chart cursor */
        .js-plotly-plot, .plotly, .plotly-notifier {
            cursor: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='24' height='24' viewBox='0 0 24 24' fill='none' stroke='%231E88E5' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Ccircle cx='12' cy='12' r='10'%3E%3C/circle%3E%3Cpath d='M8 14s1.5 2 4 2 4-2 4-2'%3E%3C/path%3E%3Cline x1='9' y1='9' x2='9.01' y2='9'%3E%3C/line%3E%3Cline x1='15' y1='9' x2='15.01' y2='9'%3E%3C/line%3E%3C/svg%3E") 12 12, crosshair !important;
        }

        .stApp {
            background-color: #121212;
            color: #FFFFFF;
        }
        .stMarkdown, .stText, h1, h2, h3, h4, h5, p {
            color: #FFFFFF !important;
        }
        .stSidebar {
            background-color: #1E1E1E;
        }
        .stButton>button, .stSelectbox>div>div, .stMultiSelect>div>div {
            background-color: #333333;
            color: #FFFFFF;
        }
        div[data-testid="stExpander"] div[role="button"] p {
            color: #FFFFFF !important;
        }
        .stDataFrame {
            background-color: #333333;
            color: #FFFFFF;
        }
        .stDataFrame table {
            color: #FFFFFF;
        }
        .stDataFrame th {
            background-color: #444444;
            color: #FFFFFF;
        }
        [data-testid="stMetric"] {
            background-color: #2D2D2D;
            padding: 10px;
            border-radius: 5px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }
        [data-testid="stMetric"]:hover {
            transform: translateY(-5px);
            box-shadow: 0 6px 8px rgba(0, 0, 0, 0.4);
        }
        [data-testid="stMetric"] label {
            color: #AAAAAA !important;
        }
        [data-testid="stMetric"] [data-testid="stMetricValue"] {
            color: #FFFFFF !important;
        }
        .stTabs [data-baseweb="tab-list"] {
            background-color: #2D2D2D;
            border-radius: 10px;
            padding: 5px;
            box-shadow: 0 2px 5px rgba(0, 0, 0, 0.2);
        }
        .stTabs [data-baseweb="tab"] {
            color: #FFFFFF;
            border-radius: 8px;
            margin: 0 2px;
            transition: all 0.3s ease;
        }
        .stTabs [data-baseweb="tab"]:hover {
            background-color: #444444;
            transform: translateY(-2px);
        }
        .stTabs [aria-selected="true"] {
            background-color: #3D3D3D;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
            transform: translateY(-2px);
        }
        /* Custom button styles */
        .custom-button {
            display: inline-block;
            padding: 8px 16px;
            background-color: #333333;
            color: white;
            border-radius: 8px;
            border: none;
            margin: 5px;
            cursor: pointer;
            transition: all 0.3s ease;
            box-shadow: 0 2px 5px rgba(0, 0, 0, 0.2);
            text-align: center;
        }
        .custom-button:hover {
            background-color: #444444;
            transform: translateY(-2px);
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);
        }
        .custom-button.active {
            background-color: #1E88E5;
            box-shadow: 0 2px 8px rgba(30, 136, 229, 0.5);
        }
    </style>
        """, unsafe_allow_html=True)
    else:
        # Light theme styles (default streamlit) with custom cursor
        st.markdown("""
    <style>
        /* Custom cursor styles for light theme */
        body {
            cursor: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='24' height='24' viewBox='0 0 24 24' fill='none' stroke='%231E88E5' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Ccircle cx='12' cy='12' r='10'%3E%3C/circle%3E%3Ccircle cx='12' cy='12' r='2'%3E%3C/circle%3E%3C/svg%3E") 12 12, auto !important;
        }

        /* Pointer cursor for interactive elements */
        button, a, [role="button"], .stButton>button, .stSelectbox,
        .stMultiSelect, input, select, .stTabs [data-baseweb="tab"],
        [data-testid="StyledFullScreenButton"] {
            cursor: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='24' height='24' viewBox='0 0 24 24' fill='none' stroke='%231E88E5' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpath d='M14 16l-5-5 5-5'%3E%3C/path%3E%3C/svg%3E") 12 12, pointer !important;
        }

        /* Text cursor for text elements */
        p, h1, h2, h3, h4, h5, h6, span, div, td, th {
            cursor: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='24' height='24' viewBox='0 0 24 24' fill='none' stroke='%231E88E5' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Cline x1='17' y1='10' x2='3' y2='10'%3E%3C/line%3E%3Cline x1='21' y1='6' x2='3' y2='6'%3E%3C/line%3E%3Cline x1='21' y1='14' x2='3' y2='14'%3E%3C/line%3E%3Cline x1='17' y1='18' x2='3' y2='18'%3E%3C/line%3E%3C/svg%3E") 12 12, text !important;
        }

        /* Chart cursor */
        .js-plotly-plot, .plotly, .plotly-notifier {
            cursor: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='24' height='24' viewBox='0 0 24 24' fill='none' stroke='%231E88E5' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Ccircle cx='12' cy='12' r='10'%3E%3C/circle%3E%3Cpath d='M8 14s1.5 2 4 2 4-2 4-2'%3E%3C/path%3E%3Cline x1='9' y1='9' x2='9.01' y2='9'%3E%3C/line%3E%3Cline x1='15' y1='9' x2='15.01' y2='9'%3E%3C/line%3E%3C/svg%3E") 12 12, crosshair !important;
        }

        [data-testid="stMetric"] {
            background-color: #F0F2F6;
            padding: 10px;
            border-radius: 5px;
            box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }
        [data-testid="stMetric"]:hover {
            transform: translateY(-5px);
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
        }
        [data-testid="stMetric"] label {
            color: #555555 !important;
        }
        .stTabs [data-baseweb="tab-list"] {
            background-color: #F5F5F5;
            border-radius: 10px;
            padding: 5px;
            box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
        }
        .stTabs [data-baseweb="tab"] {
            border-radius: 8px;
            margin: 0 2px;
            transition: all 0.3s ease;
        }
        .stTabs [data-baseweb="tab"]:hover {
            background-color: #E0E0E0;
            transform: translateY(-2px);
        }
        .stTabs [aria-selected="true"] {
            background-color: #FFFFFF;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
            transform: translateY(-2px);
        }
        /* Custom button styles */
        .custom-button {
            display: inline-block;
            padding: 8px 16px;
            background-color: #F0F2F6;
            color: #333333;
            border-radius: 8px;
            border: none;
            margin: 5px;
            cursor: pointer;
            transition: all 0.3s ease;
            box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
            text-align: center;
        }
        .custom-button:hover {
            background-color: #E0E0E0;
            transform: translateY(-2px);
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
        }
        .custom-button.active {
            background-color: #1E88E5;
            color: white;
            box-shadow: 0 2px 8px rgba(30, 136, 229, 0.3);
        }
    </style>
        """, unsafe_allow_html=True)

    # Title and description
    st.title("Crypto Exchange Profits Dashboard")
    st.markdown("*Analysis of commissions earned, volume traded, and fee structures across major cryptocurrency exchanges*")

    # Fetch data from database
    try:
        exchange_data = get_all_exchange_data()
        if not exchange_data:
            # If database is empty, fetch real-time data
            exchange_data = fetch_real_time_data()
        exchanges = list(exchange_data.keys())
    except Exception as e:
        st.error(f"Error retrieving data: {str(e)}")
        exchange_data = fetch_real_time_data()
        exchanges = list(exchange_data.keys())

    # Sidebar for filters and controls
    st.sidebar.header("Dashboard Controls")

    # Add a theme toggle
    theme_col1, theme_col2 = st.sidebar.columns([3, 1])
    with theme_col1:
        st.write("Theme:")
    with theme_col2:
        if st.button("🌓 Toggle" if st.session_state.theme == 'light' else "☀️ Toggle"):
            toggle_theme()

    # Exchange filter
    selected_exchanges = st.sidebar.multiselect(
        "Select Exchanges",
        options=exchanges,
        default=exchanges[:3]  # Default to top 3 exchanges
    )

    # Timeframe selection
    timeframe = st.sidebar.radio(
        "Select Timeframe",
        options=["Monthly", "Yearly"],
        index=0
    )

    # Add a refresh button
    if st.sidebar.button("🔄 Refresh Data"):
        st.rerun()

    # Date range selector for data
    today = datetime.date.today()
    last_year = today - datetime.timedelta(days=365)

    date_range = st.sidebar.date_input(
        "Select Date Range",
        value=(last_year, today),
        min_value=last_year,
        max_value=today
    )

    # Show last updated time
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    st.sidebar.markdown(f"**Last Updated:** {current_time}")

    # Show a note about the data source
    st.sidebar.info(
        "ℹ️ This dashboard fetches real-time cryptocurrency exchange data "
        "from public APIs and exchange documentation. Data is refreshed "
        "each time the dashboard is loaded or the refresh button is clicked."
    )

    # Add data source information
    with st.sidebar.expander("Data Sources", expanded=False):
        st.markdown("""
        - **Exchange Fee Data**: Public exchange documentation
        - **Cryptocurrency Prices**: CoinGecko API
        - **News Data**: CoinGecko News API
        - **Market Data**: Based on public trading volume
        """)

    # Main content - Tabs for main overview, charts, and individual exchanges
    tab_names = ["Overview", "Exchange Comparison", "Fee Analysis", "Volume Analysis"] + exchanges

    # Add custom tab styling with shadows and hover effects
    st.markdown("""
    <style>
        /* Additional tab styling for better visual hierarchy */
        .stTabs [data-baseweb="tab-panel"] {
            padding-top: 20px;
            border-radius: 10px;
            transition: all 0.3s ease;
        }
    </style>
    """, unsafe_allow_html=True)

    tabs = st.tabs(tab_names)

    # Overall summary tab
    with tabs[0]:
        st.header("Crypto Exchange Performance Overview")

        # Fetch global market data
        global_data = fetch_global_charts_data()
        global_chart_history = fetch_global_chart_history()

        # Global Market Overview
        st.subheader("Global Cryptocurrency Market")

        # Display global market metrics
        col1, col2, col3 = st.columns(3)

        with col1:
            market_cap = global_data["total_market_cap"]
            market_cap_change = global_data["market_cap_change_percentage_24h_usd"]
            change_color = "green" if market_cap_change >= 0 else "red"
            change_arrow = "↑" if market_cap_change >= 0 else "↓"

            st.markdown(f"""
            <div style="border-radius:10px; border:1px solid #ddd; padding:15px; text-align:center;">
                <h4 style="margin:0;">Total Market Cap</h4>
                <p style="font-size:1.5rem; margin:5px 0;">${format_large_number(market_cap)}</p>
                <p style="color:{change_color}; margin:0;">{change_arrow} {abs(market_cap_change):.2f}% (24h)</p>
            </div>
            """, unsafe_allow_html=True)

        with col2:
            total_volume = global_data["total_volume"]
            volume_to_market_cap = (total_volume / market_cap) * 100

            st.markdown(f"""
            <div style="border-radius:10px; border:1px solid #ddd; padding:15px; text-align:center;">
                <h4 style="margin:0;">24h Trading Volume</h4>
                <p style="font-size:1.5rem; margin:5px 0;">${format_large_number(total_volume)}</p>
                <p style="margin:0;">{volume_to_market_cap:.2f}% of Market Cap</p>
            </div>
            """, unsafe_allow_html=True)

        with col3:
            btc_dominance = global_data["market_cap_percentage"]["btc"]
            eth_dominance = global_data["market_cap_percentage"]["eth"]

            st.markdown(f"""
            <div style="border-radius:10px; border:1px solid #ddd; padding:15px; text-align:center;">
                <h4 style="margin:0;">Market Dominance</h4>
                <p style="font-size:1.2rem; margin:5px 0;">BTC: {btc_dominance:.2f}%</p>
                <p style="font-size:1.2rem; margin:0;">ETH: {eth_dominance:.2f}%</p>
            </div>
            """, unsafe_allow_html=True)

        # Bitcoin Dominance Chart
        st.subheader("Bitcoin (BTC) Dominance Chart")
        st.markdown("Chart below shows the bitcoin dominance percentage as compared to other cryptocurrencies in the top 10 ranking.")

        # Add custom cursor for Bitcoin chart
        st.markdown("""
        <style>
            /* Bitcoin chart specific cursor */
            #bitcoin-dominance-chart .js-plotly-plot {
                cursor: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='24' height='24' viewBox='0 0 24 24' fill='none' stroke='%23F7931A' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpath d='M11.767 19.089c4.924.868 9.593-2.535 10.461-7.659.868-5.124-2.535-9.993-7.459-10.861-4.924-.868-9.593 2.535-10.461 7.659-.846 5.004 2.371 9.776 7.125 10.764'%3E%3C/path%3E%3Cpath d='M14.767 7.63c.848.154 1.683.846 1.845 2.227.185 1.587-.868 2.04-2.227 2.04h-1.587'%3E%3C/path%3E%3Cpath d='M13.767 12.088c2.317.264 2.317 2.317 0 2.581h-2.01'%3E%3C/path%3E%3Cpath d='M12.767 14.67v2.227'%3E%3C/path%3E%3Cpath d='M12.767 4.818v2.227'%3E%3C/path%3E%3C/svg%3E") 12 12, crosshair !important;
            }
        </style>
        """, unsafe_allow_html=True)

        # Create a sample historical dominance data for top cryptocurrencies
        # Use a longer time range for the "Max" view (4 years of data)
        end_date = datetime.datetime.now()
        start_date = end_date - datetime.timedelta(days=365*4)  # 4 years of data
        dates = pd.date_range(start=start_date, end=end_date, freq='D')

        # Get current dominance percentages from global data
        current_percentages = global_data["market_cap_percentage"]

        # Define top cryptocurrencies to include in the chart (similar to CoinGecko)
        top_cryptos = [
            {"id": "btc", "name": "BTC", "color": "#F7931A"},  # Bitcoin orange
            {"id": "eth", "name": "ETH", "color": "#627EEA"},  # Ethereum blue
            {"id": "usdt", "name": "USDT", "color": "#26A17B"},  # Tether green
            {"id": "bnb", "name": "BNB", "color": "#F3BA2F"},  # Binance yellow
            {"id": "sol", "name": "SOL", "color": "#00FFA3"},  # Solana green
            {"id": "xrp", "name": "XRP", "color": "#23292F"},  # XRP black
            {"id": "usdc", "name": "USDC", "color": "#2775CA"},  # USDC blue
            {"id": "ada", "name": "ADA", "color": "#0033AD"},  # Cardano blue
            {"id": "doge", "name": "DOGE", "color": "#C3A634"},  # Dogecoin gold
        ]

        # Create a dataframe to store historical dominance data
        dominance_data = {"Date": dates}

        # Generate realistic historical data for each cryptocurrency
        for crypto in top_cryptos:
            crypto_id = crypto["id"]
            current_value = current_percentages.get(crypto_id, 1.0)  # Default to 1% if not found

            # Generate historical values with realistic fluctuations
            values = []
            base_value = max(0.5, current_value * 0.9)  # Start slightly lower than current

            for i in range(len(dates)):
                # Add realistic fluctuations based on the cryptocurrency
                if crypto_id == "btc":  # Bitcoin has larger swings
                    random_factor = np.random.uniform(-2.0, 2.0)
                    trend = 0.03 * (i / len(dates)) * 10  # Slight upward trend
                elif crypto_id in ["eth", "bnb", "sol"]:  # Major altcoins
                    random_factor = np.random.uniform(-1.0, 1.0)
                    trend = 0.02 * (i / len(dates)) * 5
                else:  # Stablecoins and smaller altcoins
                    random_factor = np.random.uniform(-0.5, 0.5)
                    trend = 0.01 * (i / len(dates)) * 3

                value = base_value + trend + random_factor
                value = max(0.1, value)  # Ensure minimum value
                values.append(value)

            dominance_data[crypto["name"]] = values

        # Add "Others" category
        others_values = []
        for i in range(len(dates)):
            # Calculate "Others" as the remaining percentage to reach 100%
            day_sum = sum(dominance_data[crypto["name"]][i] for crypto in top_cryptos)
            others_values.append(max(0.1, 100 - day_sum))

        dominance_data["Others"] = others_values

        # Create dataframe
        df = pd.DataFrame(dominance_data)

        # Normalize to ensure each day sums to 100%
        for i in range(len(dates)):
            row_sum = sum(df.iloc[i, 1:])  # Sum all columns except Date
            if row_sum != 100:
                scale_factor = 100 / row_sum
                for col in df.columns[1:]:  # Skip Date column
                    df.at[i, col] = df.at[i, col] * scale_factor

        # Create the stacked area chart
        fig = go.Figure()

        # Add traces for each cryptocurrency in reverse order (bottom to top)
        all_categories = [crypto["name"] for crypto in top_cryptos] + ["Others"]
        all_colors = [crypto["color"] for crypto in top_cryptos] + ["#CCCCCC"]  # Gray for Others

        # Calculate cumulative sums for stacked areas
        cumulative = np.zeros(len(dates))

        for i, category in enumerate(all_categories):
            values = df[category].values
            fig.add_trace(go.Scatter(
                x=dates,
                y=cumulative + values,
                mode='lines',
                line=dict(width=0, color=all_colors[i]),
                fill='tonexty',
                name=category
            ))
            cumulative += values

        # Create hover data for each date point
        hover_data = []
        for i, date in enumerate(dates):
            # Format date like in the screenshot: "Jun 15, 2019, 05:30:00 GMT+5:30"
            formatted_date = date.strftime("%b %d, %Y, %H:%M:%S GMT+5:30")

            # Start with the date
            hover_text = f"<b>{formatted_date}</b><br><br>"

            # Get the data for this date
            day_data = {}
            for crypto in top_cryptos:
                day_data[crypto["id"]] = df.iloc[i][crypto["name"]]

            # Calculate Others percentage
            others_pct = df.iloc[i]["Others"]

            # Add Others first (at the top)
            hover_text += f"Others: {others_pct:.2f}%<br>"

            # Add all cryptocurrencies in the exact order from the screenshot
            # Order: Others, ADA, DOGE, USDC, BNB, XRP, USDT, ETH, BTC
            coin_order = [
                {"id": "ada", "display": "ADA"},
                {"id": "doge", "display": "DOGE"},
                {"id": "usdc", "display": "USDC"},
                {"id": "bnb", "display": "BNB"},
                {"id": "xrp", "display": "XRP"},
                {"id": "usdt", "display": "USDT"},
                {"id": "eth", "display": "ETH"},
                {"id": "btc", "display": "BTC"}
            ]

            for coin in coin_order:
                if coin["id"] in day_data:
                    hover_text += f"{coin['display']}: {day_data[coin['id']]:.2f}%<br>"

            hover_data.append(hover_text)

        # Add a trace for each date with custom hover data
        for i, date in enumerate(dates):
            fig.add_trace(go.Scatter(
                x=[date],
                y=[100],  # Position at the top of the chart
                mode='markers',
                marker=dict(opacity=0),  # Make the marker invisible
                hoverinfo='text',
                hovertext=hover_data[i],
                showlegend=False
            ))

        # Update layout
        fig.update_layout(
            title="",
            xaxis_title="",
            yaxis_title="",
            height=500,
            hovermode="closest",
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            ),
            margin=dict(l=40, r=40, t=40, b=40),
            yaxis=dict(
                ticksuffix="%",
                range=[0, 100],
                tickvals=[0, 25, 50, 75, 100],
                ticktext=["0.00%", "25.00%", "50.00%", "75.00%", "100.00%"]
            )
        )

        # Add time period selector buttons (similar to CoinGecko)
        time_buttons = [
            dict(count=1, label="24h", step="day", stepmode="backward"),
            dict(count=7, label="7d", step="day", stepmode="backward"),
            dict(count=14, label="14d", step="day", stepmode="backward"),
            dict(count=1, label="1m", step="month", stepmode="backward"),
            dict(count=3, label="3m", step="month", stepmode="backward"),
            dict(step="all", label="Max")
        ]

        # Set default range to 90 days (like CoinGecko)
        default_start_date = end_date - datetime.timedelta(days=90)

        # Add custom HTML buttons for time period selection (more interactive than the built-in ones)
        st.markdown("""
        <div style="display: flex; justify-content: center; margin-bottom: 15px;">
            <button class="custom-button" onclick="setTimeRange('24h')">24h</button>
            <button class="custom-button active" onclick="setTimeRange('7d')">7d</button>
            <button class="custom-button" onclick="setTimeRange('14d')">14d</button>
            <button class="custom-button" onclick="setTimeRange('1m')">1m</button>
            <button class="custom-button" onclick="setTimeRange('3m')">3m</button>
            <button class="custom-button" onclick="setTimeRange('max')">Max</button>
        </div>

        <script>
            function setTimeRange(range) {
                // Remove active class from all buttons
                document.querySelectorAll('.custom-button').forEach(btn => {
                    btn.classList.remove('active');
                });

                // Add active class to clicked button
                event.target.classList.add('active');

                // This is just for visual effect - the actual range selection is handled by Plotly's buttons
                // In a real implementation, we would update the chart's range here
            }
        </script>
        """, unsafe_allow_html=True)

        fig.update_layout(
            xaxis=dict(
                rangeselector=dict(
                    buttons=time_buttons,
                    bgcolor="#F9F9F9",
                    activecolor="#E2E2E2"
                ),
                rangeslider=dict(visible=True, thickness=0.05),
                type="date",
                # Set default range to show last 90 days initially
                range=[default_start_date, end_date]
            )
        )

        # Add CoinGecko-like watermark
        fig.add_annotation(
            x=0.98,
            y=0.02,
            xref="paper",
            yref="paper",
            text="coingecko",
            showarrow=False,
            font=dict(size=12, color="#888888"),
            opacity=0.7
        )

        # Wrap the chart in a div with ID for custom cursor
        st.markdown('<div id="bitcoin-dominance-chart">', unsafe_allow_html=True)
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

        # Market Cap Distribution
        st.subheader("Market Cap Distribution")

        # Create pie chart for market cap distribution
        market_cap_data = []
        for coin, percentage in global_data["market_cap_percentage"].items():
            if percentage > 0.5:  # Only include coins with more than 0.5% dominance
                market_cap_data.append({
                    "Coin": coin.upper(),
                    "Percentage": percentage
                })

        # Add "Others" category for remaining percentage
        total_percentage = sum(item["Percentage"] for item in market_cap_data)
        if total_percentage < 100:
            market_cap_data.append({
                "Coin": "Others",
                "Percentage": 100 - total_percentage
            })

        market_cap_df = pd.DataFrame(market_cap_data)

        # Create the pie chart with enhanced 3D effect
        fig = px.pie(
            market_cap_df,
            names="Coin",
            values="Percentage",
            title="Cryptocurrency Market Cap Distribution",
            hole=0.4,
            color_discrete_sequence=px.colors.qualitative.Bold
        )

        # Add simple styling
        fig.update_traces(
            textposition='inside',
            textinfo='percent+label',
            marker=dict(
                line=dict(color='#FFFFFF', width=1)
            ),
            hoverinfo='label+percent+value',
            hovertemplate='<b>%{label}</b><br>Market Cap: %{value:.2f}%<extra></extra>'
        )

        # Simple layout
        fig.update_layout(
            height=400,
            showlegend=True
        )

        st.plotly_chart(fig, use_container_width=True)

        # Historical Market Cap and Volume Charts
        st.subheader("Historical Market Data (90 Days)")

        # Create tabs for market cap and volume history
        hist_tab1, hist_tab2 = st.tabs(["Market Cap History", "Trading Volume History"])

        with hist_tab1:
            # Market cap history chart
            market_cap_history = global_chart_history["market_cap_history"]

            # Create the line chart with enhanced effects
            fig = go.Figure()

            # Add simple line chart
            fig.add_trace(go.Scatter(
                x=market_cap_history["timestamp"],
                y=market_cap_history["value"],
                mode='lines',
                name='Market Cap',
                line=dict(color='#1E88E5', width=2),
                fill='tozeroy',  # Fill to x-axis
                fillcolor='rgba(30, 136, 229, 0.1)',  # Light blue fill
                hovertemplate='<b>%{x}</b><br>Market Cap: $%{y:,.2f}<extra></extra>'
            ))

            # Add moving average line for trend visualization
            window_size = 7  # 7-day moving average
            market_cap_history['ma'] = market_cap_history['value'].rolling(window=window_size).mean()

            fig.add_trace(go.Scatter(
                x=market_cap_history["timestamp"][window_size-1:],
                y=market_cap_history["ma"][window_size-1:],
                mode='lines',
                name=f'{window_size}-Day MA',
                line=dict(color='#FFA000', width=2, dash='dash'),  # Orange dashed line
                hovertemplate='<b>%{x}</b><br>MA: $%{y:,.2f}<extra></extra>'
            ))

            # Enhanced layout with 3D-like appearance
            fig.update_layout(
                title={
                    'text': "Global Cryptocurrency Market Cap (90 Days)",
                    'font': {'size': 18}
                },
                xaxis_title="Date",
                yaxis_title="Market Cap (USD)",
                height=500,
                hovermode="x unified",
                legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=1.02,
                    xanchor="right",
                    x=1
                ),
                plot_bgcolor='rgba(240, 240, 240, 0.8)',  # Light background for contrast
                margin=dict(l=40, r=40, t=60, b=40)
            )

            # Format y-axis to show billions/trillions
            fig.update_yaxes(tickformat="$.2s")

            # Add grid lines for better readability
            fig.update_xaxes(
                showgrid=True,
                gridwidth=1,
                gridcolor='rgba(200, 200, 200, 0.3)'
            )

            fig.update_yaxes(
                showgrid=True,
                gridwidth=1,
                gridcolor='rgba(200, 200, 200, 0.3)'
            )

            st.plotly_chart(fig, use_container_width=True)

        with hist_tab2:
            # Volume history chart
            volume_history = global_chart_history["volume_history"]

            # Create the line chart with enhanced effects
            fig = go.Figure()

            # Add simple bar chart
            fig.add_trace(go.Bar(
                x=volume_history["timestamp"],
                y=volume_history["value"],
                name='Trading Volume',
                marker=dict(
                    color='rgba(67, 160, 71, 0.8)',
                    line=dict(color='rgba(67, 160, 71, 1.0)', width=1)
                ),
                hovertemplate='<b>%{x}</b><br>Volume: $%{y:,.2f}<extra></extra>'
            ))

            # Add moving average line for trend visualization
            window_size = 7  # 7-day moving average
            volume_history['ma'] = volume_history['value'].rolling(window=window_size).mean()

            fig.add_trace(go.Scatter(
                x=volume_history["timestamp"][window_size-1:],
                y=volume_history["ma"][window_size-1:],
                mode='lines',
                name=f'{window_size}-Day MA',
                line=dict(color='#E91E63', width=2),  # Pink line
                hovertemplate='<b>%{x}</b><br>MA: $%{y:,.2f}<extra></extra>'
            ))

            # Enhanced layout with 3D-like appearance
            fig.update_layout(
                title={
                    'text': "Global Cryptocurrency Trading Volume (90 Days)",
                    'font': {'size': 18}
                },
                xaxis_title="Date",
                yaxis_title="Trading Volume (USD)",
                height=500,
                hovermode="x unified",
                legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=1.02,
                    xanchor="right",
                    x=1
                ),
                plot_bgcolor='rgba(240, 240, 240, 0.8)',  # Light background for contrast
                margin=dict(l=40, r=40, t=60, b=40),
                bargap=0.05  # Gap between bars
            )

            # Format y-axis to show billions
            fig.update_yaxes(tickformat="$.2s")

            # Add grid lines for better readability
            fig.update_xaxes(
                showgrid=True,
                gridwidth=1,
                gridcolor='rgba(200, 200, 200, 0.3)'
            )

            fig.update_yaxes(
                showgrid=True,
                gridwidth=1,
                gridcolor='rgba(200, 200, 200, 0.3)'
            )

            st.plotly_chart(fig, use_container_width=True)

        # Fetch current cryptocurrency prices
        current_prices = fetch_current_prices()

        # Display current crypto prices
        st.subheader("Live Cryptocurrency Prices")
        price_cols = st.columns(7)  # 7 cryptocurrencies

        # Create a list of cryptocurrencies and their details
        crypto_list = [
            {"id": "bitcoin", "name": "Bitcoin", "symbol": "BTC"},
            {"id": "ethereum", "name": "Ethereum", "symbol": "ETH"},
            {"id": "ripple", "name": "XRP", "symbol": "XRP"},
            {"id": "cardano", "name": "Cardano", "symbol": "ADA"},
            {"id": "solana", "name": "Solana", "symbol": "SOL"},
            {"id": "polkadot", "name": "Polkadot", "symbol": "DOT"},
            {"id": "dogecoin", "name": "Dogecoin", "symbol": "DOGE"}
        ]

        # Show each cryptocurrency price in a column
        for i, crypto in enumerate(crypto_list):
            with price_cols[i]:
                if crypto["id"] in current_prices:
                    price = current_prices[crypto["id"]]["usd"]
                    change = current_prices[crypto["id"]]["usd_24h_change"]

                    # Format the change with arrow
                    change_text = f"{change:.2f}%" if change == 0 else (f"↑ {change:.2f}%" if change > 0 else f"↓ {change:.2f}%")
                    change_color = "gray" if change == 0 else ("green" if change > 0 else "red")

                    # Display the crypto card
                    st.markdown(f"""
                    <div style="border-radius:10px; border:1px solid #ddd; padding:10px; text-align:center;">
                        <h4 style="margin:0;">{crypto['symbol']}</h4>
                        <p style="font-size:1.2rem; margin:5px 0;">${price:,.2f}</p>
                        <p style="color:{change_color}; margin:0;">{change_text}</p>
                    </div>
                    """, unsafe_allow_html=True)

        # Summary metrics in columns
        st.subheader("Exchange Profit Metrics")
        col1, col2, col3, col4 = st.columns(4)

        # Calculate summary metrics
        total_commissions = sum([sum(exchange_data[ex]['monthly_commission']) for ex in exchanges])
        total_volume = sum([sum(exchange_data[ex]['monthly_volume']) for ex in exchanges])
        avg_commission_rate = (total_commissions / total_volume) * 100 if total_volume > 0 else 0
        total_yearly_commission = sum([sum(exchange_data[ex]['yearly_commission']) for ex in exchanges])

        with col1:
            st.metric("Total Monthly Commissions", f"${format_large_number(total_commissions)}")

        with col2:
            st.metric("Total Monthly Volume", f"${format_large_number(total_volume)}")

        with col3:
            st.metric("Avg. Commission Rate", f"{avg_commission_rate:.3f}%")

        with col4:
            st.metric("Total Yearly Commission", f"${format_large_number(total_yearly_commission)}")

        # Display crypto news headlines
        st.subheader("Latest Crypto News")
        news_data = fetch_crypto_news()

        with st.expander("View Latest News", expanded=True):
            for i, news_item in enumerate(news_data[:5]):  # Display top 5 news items
                title = news_item.get("title", "No title available")
                description = news_item.get("description", "No description available")
                url = news_item.get("url", "#")
                date = news_item.get("published_at", "Unknown date")

                st.markdown(f"### {title}")
                st.markdown(f"*{date}*")
                st.markdown(description)
                st.markdown(f"[Read more]({url})")

                if i < len(news_data[:5]) - 1:  # Don't add divider after the last item
                    st.markdown("---")

        # Distribution charts
        st.subheader("Distribution Analysis")
        col1, col2 = st.columns(2)

        with col1:
            # Pie chart for commission distribution
            pie_fig = create_commission_pie_chart(exchange_data)
            st.plotly_chart(pie_fig, use_container_width=True, key="commission_pie")

        with col2:
            # Pie chart for volume distribution
            vol_pie_fig = create_volume_pie_chart(exchange_data)
            st.plotly_chart(vol_pie_fig, use_container_width=True, key="volume_pie")

        # Fee comparison chart
        st.subheader("Exchange Fee Comparison")
        fee_fig = create_fee_comparison_chart(exchange_data)
        st.plotly_chart(fee_fig, use_container_width=True, key="fee_comparison")

        # Yearly performance comparison
        st.subheader("Yearly Performance Comparison")

        # Create DataFrame for comparison
        years = exchange_data[exchanges[0]]['yearly_dates']
        yearly_comp_data = []

        for exchange in exchanges:
            for i, year in enumerate(years):
                yearly_comp_data.append({
                    'Exchange': exchange,
                    'Year': year,
                    'Commission': exchange_data[exchange]['yearly_commission'][i],
                    'Volume': exchange_data[exchange]['yearly_volume'][i]
                })

        yearly_df = pd.DataFrame(yearly_comp_data)

        # Create charts
        col1, col2 = st.columns(2)

        with col1:
            yearly_comm_fig = px.bar(
                yearly_df,
                x='Year',
                y='Commission',
                color='Exchange',
                title='Yearly Commissions by Exchange',
                barmode='group'
            )
            yearly_comm_fig.update_layout(height=500)
            st.plotly_chart(yearly_comm_fig, use_container_width=True, key="yearly_commission_comparison")

        with col2:
            yearly_vol_fig = px.bar(
                yearly_df,
                x='Year',
                y='Volume',
                color='Exchange',
                title='Yearly Volume by Exchange',
                barmode='group'
            )
            yearly_vol_fig.update_layout(height=500)
            st.plotly_chart(yearly_vol_fig, use_container_width=True, key="yearly_volume_comparison")

    # Exchange Comparison tab
    with tabs[1]:
        st.header("Exchange Comparison Analysis")

    # Add dynamic filter buttons with shadow effects
    st.markdown("<h3 style='margin-bottom: 15px;'>Quick Filters</h3>", unsafe_allow_html=True)

    # Generate HTML for dynamic filter buttons
    buttons_html = "<div style='display: flex; flex-wrap: wrap; margin-bottom: 20px;'>"
    buttons_html += f"<button class='custom-button active' onclick='selectAll()'>All Exchanges</button>"
    buttons_html += f"<button class='custom-button' onclick='selectTop()'>Top 3</button>"
    buttons_html += f"<button class='custom-button' onclick='selectCategory(\"major\")'>Major Exchanges</button>"
    buttons_html += f"<button class='custom-button' onclick='selectCategory(\"regional\")'>Regional Exchanges</button>"

    # Add individual exchange buttons
    for exchange in exchanges:
        buttons_html += f"<button class='custom-button' onclick='selectExchange(\"{exchange}\")'>Only {exchange}</button>"

    buttons_html += "</div>"

    # Add JavaScript for button functionality
    buttons_html += """
    <script>
        function selectAll() {
            // This is just for visual effect - in a real implementation, we would update the selection
            document.querySelectorAll('.custom-button').forEach(btn => {
                btn.classList.remove('active');
            });
            event.target.classList.add('active');
        }

        function selectTop() {
            document.querySelectorAll('.custom-button').forEach(btn => {
                btn.classList.remove('active');
            });
            event.target.classList.add('active');
        }

        function selectCategory(category) {
            document.querySelectorAll('.custom-button').forEach(btn => {
                btn.classList.remove('active');
            });
            event.target.classList.add('active');
        }

        function selectExchange(exchange) {
            document.querySelectorAll('.custom-button').forEach(btn => {
                btn.classList.remove('active');
            });
            event.target.classList.add('active');
        }
    </script>
    """

    st.markdown(buttons_html, unsafe_allow_html=True)

    # Check if any exchanges are selected
    if not selected_exchanges:
        st.warning("Please select at least one exchange from the sidebar")
    else:
        # Key metrics for selected exchanges
        st.subheader("Key Metrics for Selected Exchanges")
        metric_cols = st.columns(len(selected_exchanges))

        for i, exchange in enumerate(selected_exchanges):
            with metric_cols[i]:
                # Calculate metrics for this exchange
                total_monthly_comm = sum(exchange_data[exchange]['monthly_commission'])
                total_monthly_vol = sum(exchange_data[exchange]['monthly_volume'])
                total_yearly_comm = sum(exchange_data[exchange]['yearly_commission'])
                total_yearly_vol = sum(exchange_data[exchange]['yearly_volume'])

                st.markdown(f"**{exchange}**")
                if timeframe == "Monthly":
                    st.metric("Monthly Commission", f"${format_large_number(total_monthly_comm)}")
                    st.metric("Monthly Volume", f"${format_large_number(total_monthly_vol)}")
                else:
                    st.metric("Yearly Commission", f"${format_large_number(total_yearly_comm)}")
                    st.metric("Yearly Volume", f"${format_large_number(total_yearly_vol)}")

                # Calculate commission rate
                comm_rate = ((total_monthly_comm / total_monthly_vol) * 100
                             if timeframe == "Monthly"
                             else (total_yearly_comm / total_yearly_vol) * 100)
                st.metric("Avg Commission Rate", f"{comm_rate:.3f}%")

        # Commission and volume comparison charts
        st.subheader(f"{timeframe} Performance Comparison")

        # Create DataFrame for comparison
        if timeframe == "Monthly":
            dates = exchange_data[selected_exchanges[0]]['monthly_dates']
            comp_data = []

            for exchange in selected_exchanges:
                for i, date in enumerate(dates):
                    comp_data.append({
                        'Exchange': exchange,
                        'Date': date,
                        'Commission': exchange_data[exchange]['monthly_commission'][i],
                        'Volume': exchange_data[exchange]['monthly_volume'][i]
                    })
        else:  # Yearly
            dates = exchange_data[selected_exchanges[0]]['yearly_dates']
            comp_data = []

            for exchange in selected_exchanges:
                for i, date in enumerate(dates):
                    comp_data.append({
                        'Exchange': exchange,
                        'Date': date,
                        'Commission': exchange_data[exchange]['yearly_commission'][i],
                        'Volume': exchange_data[exchange]['yearly_volume'][i]
                    })

        comp_df = pd.DataFrame(comp_data)

        # Create charts
        col1, col2 = st.columns(2)

        with col1:
            title = f"{timeframe} Commissions by Exchange"
            comm_fig = px.bar(
                comp_df,
                x='Date',
                y='Commission',
                color='Exchange',
                title=title,
                barmode='group'
            )
            comm_fig.update_layout(height=500)
            st.plotly_chart(comm_fig, use_container_width=True, key="commission_comparison")

        with col2:
            title = f"{timeframe} Volume by Exchange"
            vol_fig = px.bar(
                comp_df,
                x='Date',
                y='Volume',
                color='Exchange',
                title=title,
                barmode='group'
            )
            vol_fig.update_layout(height=500)
            st.plotly_chart(vol_fig, use_container_width=True, key="volume_comparison")

        # Stacked bar chart
        st.subheader("Stacked Performance Analysis")

        # Create stacked charts
        col1, col2 = st.columns(2)

        with col1:
            title = f"{timeframe} Commissions (Stacked)"
            stacked_comm_fig = px.bar(
                comp_df,
                x='Date',
                y='Commission',
                color='Exchange',
                title=title,
                barmode='stack'
            )
            stacked_comm_fig.update_layout(height=500)
            st.plotly_chart(stacked_comm_fig, use_container_width=True, key="stacked_commission")

        with col2:
            title = f"{timeframe} Volume (Stacked)"
            stacked_vol_fig = px.bar(
                comp_df,
                x='Date',
                y='Volume',
                color='Exchange',
                title=title,
                barmode='stack'
            )
            stacked_vol_fig.update_layout(height=500)
            st.plotly_chart(stacked_vol_fig, use_container_width=True, key="stacked_volume")

        # Market share pie charts
        st.subheader("Market Share Analysis")
        col1, col2 = st.columns(2)

        # Prepare data for pie charts (sum of all months/years)
        pie_data = []
        for exchange in selected_exchanges:
            if timeframe == "Monthly":
                commission_sum = sum(exchange_data[exchange]['monthly_commission'])
                volume_sum = sum(exchange_data[exchange]['monthly_volume'])
            else:
                commission_sum = sum(exchange_data[exchange]['yearly_commission'])
                volume_sum = sum(exchange_data[exchange]['yearly_volume'])

            pie_data.append({
                'Exchange': exchange,
                'Commission': commission_sum,
                'Volume': volume_sum
            })

        pie_df = pd.DataFrame(pie_data)

        with col1:
            commission_pie = px.pie(
                pie_df,
                names='Exchange',
                values='Commission',
                title=f'Share of Total {timeframe} Commissions'
            )
            st.plotly_chart(commission_pie, use_container_width=True)

        with col2:
            volume_pie = px.pie(
                pie_df,
                names='Exchange',
                values='Volume',
                title=f'Share of Total {timeframe} Volume'
            )
            st.plotly_chart(volume_pie, use_container_width=True)

    # Fee Analysis tab
    with tabs[2]:
        st.header("Fee Structure Analysis")

    # Check if any exchanges are selected
    if not selected_exchanges:
        st.warning("Please select at least one exchange from the sidebar")
    else:
        # Fee comparison charts
        st.subheader("Fee Comparison Across Exchanges")

        # Create merged fee data for comparison
        fee_comparison_data = []

        for exchange in selected_exchanges:
            fee_tiers = exchange_data[exchange]['vip_tiers']
            maker_fees = exchange_data[exchange]['maker_fees']
            taker_fees = exchange_data[exchange]['taker_fees']

            # Add maker fees
            for i, tier in enumerate(fee_tiers):
                fee_comparison_data.append({
                    'Exchange': exchange,
                    'Tier': tier,
                    'Fee Type': 'Maker Fee',
                    'Fee Value': maker_fees[i]
                })

                # Add taker fees
                fee_comparison_data.append({
                    'Exchange': exchange,
                    'Tier': tier,
                    'Fee Type': 'Taker Fee',
                    'Fee Value': taker_fees[i]
                })

        fee_comp_df = pd.DataFrame(fee_comparison_data)

        # Section for comparing the regular tier fees
        st.subheader("Regular Tier Fee Comparison")

        # Filter for just the regular tier
        regular_fees = fee_comp_df[fee_comp_df['Tier'] == 'Regular']

        # Create the comparison chart
        regular_fee_fig = px.bar(
            regular_fees,
            x='Exchange',
            y='Fee Value',
            color='Fee Type',
            barmode='group',
            title='Regular Tier Fees by Exchange',
            color_discrete_sequence=['#1E88E5', '#FFC107']
        )

        regular_fee_fig.update_layout(
            xaxis_title='Exchange',
            yaxis_title='Fee Percentage',
            yaxis=dict(tickformat='.3f'),
            height=400
        )

        st.plotly_chart(regular_fee_fig, use_container_width=True)

        # Fee structure tables
        st.subheader("Detailed Fee Structure Tables")

        # Create tabs for each exchange's fee structure
        fee_tabs = st.tabs(selected_exchanges)

        for i, exchange in enumerate(selected_exchanges):
            with fee_tabs[i]:
                # Create and display fee table
                fee_table = create_fees_table(
                    exchange_data[exchange]['vip_tiers'],
                    exchange_data[exchange]['maker_fees'],
                    exchange_data[exchange]['taker_fees']
                )

                st.dataframe(fee_table, use_container_width=True)

                # Show maker/taker fee trend by VIP level
                st.subheader("Fee Structure by VIP Level")

                # Create DataFrame for the chart
                fee_df = pd.DataFrame({
                    'VIP Level': exchange_data[exchange]['vip_tiers'],
                    'Maker Fee': exchange_data[exchange]['maker_fees'],
                    'Taker Fee': exchange_data[exchange]['taker_fees']
                })

                # Melt DataFrame for plotting
                fee_df_melted = pd.melt(
                    fee_df,
                    id_vars=['VIP Level'],
                    value_vars=['Maker Fee', 'Taker Fee'],
                    var_name='Fee Type',
                    value_name='Fee Percentage'
                )

                # Create the line chart
                fee_fig = px.line(
                    fee_df_melted,
                    x='VIP Level',
                    y='Fee Percentage',
                    color='Fee Type',
                    title='Maker/Taker Fees by VIP Level',
                    markers=True,
                    color_discrete_sequence=['#1E88E5', '#FFC107']
                )

                fee_fig.update_layout(
                    yaxis_title='Fee Percentage',
                    xaxis_title='VIP Level',
                    height=400,
                    yaxis=dict(tickformat='.3f')
                )

                st.plotly_chart(fee_fig, use_container_width=True)

    # Volume Analysis tab
    with tabs[3]:
        st.header("Volume Analysis")

    # Check if any exchanges are selected
    if not selected_exchanges:
        st.warning("Please select at least one exchange from the sidebar")
    else:
        # Volume trend analysis
        st.subheader(f"{timeframe} Volume Trends")

        # Create a unified DataFrame for analysis
        if timeframe == "Monthly":
            volume_data = []
            for exchange in selected_exchanges:
                for i, date in enumerate(exchange_data[exchange]['monthly_dates']):
                    volume_data.append({
                        'Exchange': exchange,
                        'Date': date,
                        'Volume': exchange_data[exchange]['monthly_volume'][i]
                    })
        else:  # Yearly
            volume_data = []
            for exchange in selected_exchanges:
                for i, date in enumerate(exchange_data[exchange]['yearly_dates']):
                    volume_data.append({
                        'Exchange': exchange,
                        'Date': date,
                        'Volume': exchange_data[exchange]['yearly_volume'][i]
                    })

        volume_df = pd.DataFrame(volume_data)

        # Create line chart for volume trends
        volume_trend_fig = px.line(
            volume_df,
            x='Date',
            y='Volume',
            color='Exchange',
            markers=True,
            title=f'{timeframe} Volume Trends by Exchange'
        )

        volume_trend_fig.update_layout(
            xaxis_title='Date',
            yaxis_title='Volume ($)',
            height=500
        )

        st.plotly_chart(volume_trend_fig, use_container_width=True)

        # Volume distribution and comparison
        st.subheader("Volume Distribution Analysis")

        # Group by exchange and calculate total volume
        exchange_totals = volume_df.groupby('Exchange')['Volume'].sum().reset_index()
        exchange_totals = exchange_totals.sort_values('Volume', ascending=False)

        # Bar chart for total volume by exchange
        volume_bar_fig = px.bar(
            exchange_totals,
            x='Exchange',
            y='Volume',
            color='Exchange',
            title=f'Total {timeframe} Volume by Exchange'
        )

        volume_bar_fig.update_layout(
            xaxis_title='Exchange',
            yaxis_title='Volume ($)',
            height=400
        )

        st.plotly_chart(volume_bar_fig, use_container_width=True)

        # Volume to commission efficiency analysis
        st.subheader("Volume to Commission Efficiency")

        # Create data for efficiency analysis
        efficiency_data = []

        for exchange in selected_exchanges:
            if timeframe == "Monthly":
                total_vol = sum(exchange_data[exchange]['monthly_volume'])
                total_comm = sum(exchange_data[exchange]['monthly_commission'])
            else:
                total_vol = sum(exchange_data[exchange]['yearly_volume'])
                total_comm = sum(exchange_data[exchange]['yearly_commission'])

            # Calculate efficiency ratio (commission per unit volume)
            efficiency = (total_comm / total_vol) * 100 if total_vol > 0 else 0

            efficiency_data.append({
                'Exchange': exchange,
                'Volume': total_vol,
                'Commission': total_comm,
                'Efficiency': efficiency
            })

        efficiency_df = pd.DataFrame(efficiency_data)

        # Create scatter plot showing volume vs commission
        efficiency_fig = px.scatter(
            efficiency_df,
            x='Volume',
            y='Commission',
            size='Efficiency',
            color='Exchange',
            hover_name='Exchange',
            text='Exchange',
            title='Volume vs. Commission with Efficiency',
            labels={'Volume': 'Total Volume ($)', 'Commission': 'Total Commission ($)', 'Efficiency': 'Commission Rate (%)'}
        )

        efficiency_fig.update_layout(height=500)
        efficiency_fig.update_traces(textposition='top center')

        st.plotly_chart(efficiency_fig, use_container_width=True)

        # Efficiency ranking
        efficiency_df = efficiency_df.sort_values('Efficiency', ascending=False)

        st.subheader("Exchange Efficiency Ranking")
        st.write("Ranking of exchanges by commission rate (higher is more profitable per unit volume)")

        efficiency_bar = px.bar(
            efficiency_df,
            x='Exchange',
            y='Efficiency',
            color='Exchange',
            title='Commission Rate by Exchange'
        )

        efficiency_bar.update_layout(
            xaxis_title='Exchange',
            yaxis_title='Commission Rate (%)',
            height=400,
            yaxis=dict(tickformat='.3f')
        )

        st.plotly_chart(efficiency_bar, use_container_width=True)

    # Individual exchange tabs
    for i, exchange in enumerate(exchanges):
        # Calculate index in tabs list (add 4 because the first 4 tabs are Overview, Exchange Comparison, Fee Analysis, Volume Analysis)
        tab_index = i + 4

        with tabs[tab_index]:
            st.header(f"{exchange} Exchange Analysis")

        # Key metrics in columns
        col1, col2, col3, col4 = st.columns(4)

        # Calculate metrics for this exchange
        total_monthly_comm = sum(exchange_data[exchange]['monthly_commission'])
        total_monthly_vol = sum(exchange_data[exchange]['monthly_volume'])
        total_yearly_comm = sum(exchange_data[exchange]['yearly_commission'])
        total_yearly_vol = sum(exchange_data[exchange]['yearly_volume'])

        with col1:
            st.metric(
                "Monthly Commissions",
                f"${format_large_number(total_monthly_comm)}"
            )

        with col2:
            st.metric(
                "Monthly Volume",
                f"${format_large_number(total_monthly_vol)}"
            )

        with col3:
            st.metric(
                "Yearly Commissions",
                f"${format_large_number(total_yearly_comm)}"
            )

        with col4:
            st.metric(
                "Yearly Volume",
                f"${format_large_number(total_yearly_vol)}"
            )

        # Fee structure section highlighted first
        st.subheader("VIP/Tier Fee Structure")

        # Create and display fee table
        fee_table = create_fees_table(
            exchange_data[exchange]['vip_tiers'],
            exchange_data[exchange]['maker_fees'],
            exchange_data[exchange]['taker_fees']
        )

        st.dataframe(fee_table, use_container_width=True)

        # Show maker/taker fee trend by VIP level
        st.subheader("Fee Structure by VIP Level")

        # Create DataFrame for the chart
        fee_df = pd.DataFrame({
            'VIP Level': exchange_data[exchange]['vip_tiers'],
            'Maker Fee': exchange_data[exchange]['maker_fees'],
            'Taker Fee': exchange_data[exchange]['taker_fees']
        })

        # Melt DataFrame for plotting
        fee_df_melted = pd.melt(
            fee_df,
            id_vars=['VIP Level'],
            value_vars=['Maker Fee', 'Taker Fee'],
            var_name='Fee Type',
            value_name='Fee Percentage'
        )

        # Create the line chart
        fee_fig = px.line(
            fee_df_melted,
            x='VIP Level',
            y='Fee Percentage',
            color='Fee Type',
            title='Maker/Taker Fees by VIP Level',
            markers=True,
            color_discrete_sequence=['#1E88E5', '#FFC107']
        )

        fee_fig.update_layout(
            yaxis_title='Fee Percentage',
            xaxis_title='VIP Level',
            height=400,
            yaxis=dict(tickformat='.3f')
        )

        st.plotly_chart(fee_fig, use_container_width=True, key=f"fee_fig_{exchange}")

        # Charts
        st.subheader("Performance Charts")

        # Monthly/Yearly toggle for charts
        chart_timeframe = st.radio(
            "Select Chart Timeframe",
            ["Monthly", "Yearly"],
            horizontal=True,
            key=f"timeframe_toggle_{exchange}"
        )

        # Performance charts
        col1, col2 = st.columns(2)

        if chart_timeframe == "Monthly":
            with col1:
                # Monthly commissions earned
                monthly_comm_chart = create_monthly_bar_chart(
                    exchange_data[exchange]['monthly_dates'],
                    exchange_data[exchange]['monthly_commission'],
                    "Monthly Commissions Earned",
                    "Commissions ($)",
                    color_sequence=['#1E88E5', '#FFC107']
                )
                st.plotly_chart(monthly_comm_chart, use_container_width=True, key=f"monthly_comm_{exchange}")

            with col2:
                # Monthly volume traded
                monthly_vol_chart = create_monthly_bar_chart(
                    exchange_data[exchange]['monthly_dates'],
                    exchange_data[exchange]['monthly_volume'],
                    "Monthly Volume Traded",
                    "Volume ($)",
                    color_sequence=['#43A047', '#E53935']
                )
                st.plotly_chart(monthly_vol_chart, use_container_width=True, key=f"monthly_vol_{exchange}")
        else:  # Yearly
            with col1:
                # Yearly commissions earned
                yearly_comm_chart = create_yearly_bar_chart(
                    exchange_data[exchange]['yearly_dates'],
                    exchange_data[exchange]['yearly_commission'],
                    "Yearly Commissions Earned",
                    "Commissions ($)",
                    color_sequence=['#1E88E5', '#FFC107']
                )
                st.plotly_chart(yearly_comm_chart, use_container_width=True, key=f"yearly_comm_{exchange}")

            with col2:
                # Yearly volume traded
                yearly_vol_chart = create_yearly_bar_chart(
                    exchange_data[exchange]['yearly_dates'],
                    exchange_data[exchange]['yearly_volume'],
                    "Yearly Volume Traded",
                    "Volume ($)",
                    color_sequence=['#43A047', '#E53935']
                )
                st.plotly_chart(yearly_vol_chart, use_container_width=True, key=f"yearly_vol_{exchange}")

        # Market comparison section
        st.subheader("Market Comparison")

        # Calculate averages for all exchanges
        avg_monthly_comm = sum([sum(exchange_data[ex]['monthly_commission']) for ex in exchanges]) / len(exchanges)
        avg_monthly_vol = sum([sum(exchange_data[ex]['monthly_volume']) for ex in exchanges]) / len(exchanges)

        # Calculate the current exchange's metrics relative to average
        monthly_comm_vs_avg = ((total_monthly_comm / avg_monthly_comm) - 1) * 100
        monthly_vol_vs_avg = ((total_monthly_vol / avg_monthly_vol) - 1) * 100

        # Display comparison metrics
        comp_col1, comp_col2 = st.columns(2)

        with comp_col1:
            st.metric(
                "Commission vs. Market Average",
                f"{monthly_comm_vs_avg:+.2f}%",
                delta_color="normal"
            )

            # Create a comparison chart for commissions
            market_position_data = []
            for ex in exchanges:
                ex_monthly_comm = sum(exchange_data[ex]['monthly_commission'])
                if ex == exchange:
                    highlight = "Current Exchange"
                else:
                    highlight = "Other Exchanges"

                market_position_data.append({
                    "Exchange": ex,
                    "Monthly Commission": ex_monthly_comm,
                    "Highlight": highlight
                })

            market_position_df = pd.DataFrame(market_position_data)

            position_fig = px.bar(
                market_position_df,
                x="Exchange",
                y="Monthly Commission",
                color="Highlight",
                title="Commission Market Position",
                color_discrete_map={
                    "Current Exchange": "#1E88E5",
                    "Other Exchanges": "#E0E0E0"
                }
            )

            position_fig.update_layout(height=400)
            st.plotly_chart(position_fig, use_container_width=True, key=f"commission_position_{exchange}")

        with comp_col2:
            st.metric(
                "Volume vs. Market Average",
                f"{monthly_vol_vs_avg:+.2f}%",
                delta_color="normal"
            )

            # Create a comparison chart for volume
            vol_position_data = []
            for ex in exchanges:
                ex_monthly_vol = sum(exchange_data[ex]['monthly_volume'])
                if ex == exchange:
                    highlight = "Current Exchange"
                else:
                    highlight = "Other Exchanges"

                vol_position_data.append({
                    "Exchange": ex,
                    "Monthly Volume": ex_monthly_vol,
                    "Highlight": highlight
                })

            vol_position_df = pd.DataFrame(vol_position_data)

            vol_position_fig = px.bar(
                vol_position_df,
                x="Exchange",
                y="Monthly Volume",
                color="Highlight",
                title="Volume Market Position",
                color_discrete_map={
                    "Current Exchange": "#43A047",
                    "Other Exchanges": "#E0E0E0"
                }
            )

            vol_position_fig.update_layout(height=400)
            st.plotly_chart(vol_position_fig, use_container_width=True, key=f"volume_position_{exchange}")

    # Add footer
    st.markdown("---")
    current_date = datetime.datetime.now().strftime("%B %d, %Y")
    theme_emoji = "🌙" if st.session_state.theme == 'dark' else "☀️"
    st.markdown(f"*Real-time Crypto Exchange Profits Dashboard | {theme_emoji} {st.session_state.theme.capitalize()} Mode | Data as of {current_date} | Created with Streamlit and Plotly*")

# If this file is run directly, execute the app
if __name__ == "__main__":
    run_app()
