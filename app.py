import streamlit as st
import pandas as pd
import plotly.express as px
import datetime
from data_fetcher import (
    fetch_real_time_data,
    fetch_crypto_news,
    fetch_current_prices
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

# Apply theme
if st.session_state.theme == 'dark':
    # Dark theme styles
    st.markdown("""
    <style>
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
        }
        [data-testid="stMetric"] label {
            color: #AAAAAA !important;
        }
        [data-testid="stMetric"] [data-testid="stMetricValue"] {
            color: #FFFFFF !important;
        }
        .stTabs [data-baseweb="tab-list"] {
            background-color: #2D2D2D;
        }
        .stTabs [data-baseweb="tab"] {
            color: #FFFFFF;
        }
        .stTabs [aria-selected="true"] {
            background-color: #3D3D3D;
        }
    </style>
    """, unsafe_allow_html=True)
else:
    # Light theme styles (default streamlit)
    st.markdown("""
    <style>
        [data-testid="stMetric"] {
            background-color: #F0F2F6;
            padding: 10px;
            border-radius: 5px;
        }
        [data-testid="stMetric"] label {
            color: #555555 !important;
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
tabs = st.tabs(tab_names)

# Overall summary tab
with tabs[0]:
    st.header("Crypto Exchange Performance Overview")
    
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
