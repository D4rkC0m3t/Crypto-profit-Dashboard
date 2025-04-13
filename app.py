import streamlit as st
import pandas as pd
import plotly.express as px
import datetime
from data_generator import generate_exchange_data
from utils import (
    create_monthly_bar_chart, 
    create_yearly_bar_chart,
    create_commission_pie_chart,
    create_volume_pie_chart,
    create_fees_table,
    create_fee_comparison_chart,
    format_large_number
)

# Page configuration
st.set_page_config(
    page_title="Crypto Exchange Profits Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Title and description
st.title("Crypto Exchange Profits Dashboard")
st.markdown("*Analysis of commissions earned, volume traded, and fee structures across major cryptocurrency exchanges*")

# Generate the exchange data
# In a real application, this would be replaced with data from an API or database
exchange_data = generate_exchange_data()
exchanges = list(exchange_data.keys())

# Sidebar for filters
st.sidebar.header("Dashboard Controls")

# Date range selector for data
today = datetime.date.today()
last_year = today - datetime.timedelta(days=365)

date_range = st.sidebar.date_input(
    "Select Date Range",
    value=(last_year, today),
    min_value=last_year,
    max_value=today
)

# Show a note about the simulated data
st.sidebar.info(
    "⚠️ Note: This dashboard uses simulated data structures that mimic "
    "realistic patterns but are not based on actual exchange data."
)

# Main content - Tabs for each exchange
tab_names = ["Overview"] + exchanges
tabs = st.tabs(tab_names)

# Overall summary tab
with tabs[0]:
    st.header("Crypto Exchange Performance Overview")
    
    # Summary metrics in columns
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
    
    # Distribution charts
    st.subheader("Distribution Analysis")
    col1, col2 = st.columns(2)
    
    with col1:
        # Pie chart for commission distribution
        pie_fig = create_commission_pie_chart(exchange_data)
        st.plotly_chart(pie_fig, use_container_width=True)
    
    with col2:
        # Pie chart for volume distribution
        vol_pie_fig = create_volume_pie_chart(exchange_data)
        st.plotly_chart(vol_pie_fig, use_container_width=True)
    
    # Fee comparison chart
    st.subheader("Exchange Fee Comparison")
    fee_fig = create_fee_comparison_chart(exchange_data)
    st.plotly_chart(fee_fig, use_container_width=True)
    
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
        st.plotly_chart(yearly_comm_fig, use_container_width=True)
    
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
        st.plotly_chart(yearly_vol_fig, use_container_width=True)

# Individual exchange tabs
for i, exchange in enumerate(exchanges, 1):
    with tabs[i]:
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
        
        # Charts
        st.subheader("Performance Charts")
        
        # Monthly charts
        col1, col2 = st.columns(2)
        
        with col1:
            # Monthly commissions earned
            monthly_comm_chart = create_monthly_bar_chart(
                exchange_data[exchange]['monthly_dates'],
                exchange_data[exchange]['monthly_commission'],
                "Monthly Commissions Earned",
                "Commissions ($)",
                color_sequence=['#1E88E5', '#FFC107']
            )
            st.plotly_chart(monthly_comm_chart, use_container_width=True)
        
        with col2:
            # Yearly commissions earned
            yearly_comm_chart = create_yearly_bar_chart(
                exchange_data[exchange]['yearly_dates'],
                exchange_data[exchange]['yearly_commission'],
                "Yearly Commissions Earned",
                "Commissions ($)",
                color_sequence=['#1E88E5', '#FFC107']
            )
            st.plotly_chart(yearly_comm_chart, use_container_width=True)
        
        # Volume charts
        col1, col2 = st.columns(2)
        
        with col1:
            # Monthly volume traded
            monthly_vol_chart = create_monthly_bar_chart(
                exchange_data[exchange]['monthly_dates'],
                exchange_data[exchange]['monthly_volume'],
                "Monthly Volume Traded",
                "Volume ($)",
                color_sequence=['#43A047', '#E53935']
            )
            st.plotly_chart(monthly_vol_chart, use_container_width=True)
        
        with col2:
            # Yearly volume traded
            yearly_vol_chart = create_yearly_bar_chart(
                exchange_data[exchange]['yearly_dates'],
                exchange_data[exchange]['yearly_volume'],
                "Yearly Volume Traded",
                "Volume ($)",
                color_sequence=['#43A047', '#E53935']
            )
            st.plotly_chart(yearly_vol_chart, use_container_width=True)
        
        # Fee structure
        st.subheader("Fee Structure")
        
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

# Add footer
st.markdown("---")
st.markdown("*Dashboard created with Streamlit and Plotly*")
