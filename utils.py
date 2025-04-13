import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import streamlit as st

def format_large_number(num):
    """Format large numbers to K, M, B notation"""
    if num >= 1_000_000_000:
        return f"{num/1_000_000_000:.2f}B"
    elif num >= 1_000_000:
        return f"{num/1_000_000:.2f}M"
    elif num >= 1_000:
        return f"{num/1_000:.2f}K"
    else:
        return f"{num:.2f}"

def create_monthly_bar_chart(dates, values, title, y_axis_title, color_sequence=None):
    """Create a monthly bar chart using Plotly"""
    if color_sequence is None:
        color_sequence = px.colors.qualitative.Plotly
    
    # Create a DataFrame for the chart
    df = pd.DataFrame({
        'Date': dates,
        'Value': values
    })
    
    # Create the bar chart
    fig = px.bar(
        df, 
        x='Date', 
        y='Value',
        title=title,
        labels={'Date': 'Month', 'Value': y_axis_title},
        color_discrete_sequence=[color_sequence[0]]
    )
    
    # Update layout for better appearance
    fig.update_layout(
        plot_bgcolor='white',
        margin=dict(l=40, r=40, t=40, b=40),
        hovermode='closest',
        xaxis_title='',
        yaxis_title=y_axis_title,
        height=400
    )
    
    # Add hover information
    fig.update_traces(
        hovertemplate='Date: %{x}<br>'+y_axis_title+': %{y:.2f}',
    )
    
    return fig

def create_yearly_bar_chart(dates, values, title, y_axis_title, color_sequence=None):
    """Create a yearly bar chart using Plotly"""
    if color_sequence is None:
        color_sequence = px.colors.qualitative.Plotly
    
    # Create a DataFrame for the chart
    df = pd.DataFrame({
        'Year': dates,
        'Value': values
    })
    
    # Create the bar chart
    fig = px.bar(
        df, 
        x='Year', 
        y='Value',
        title=title,
        labels={'Year': 'Year', 'Value': y_axis_title},
        color_discrete_sequence=[color_sequence[1]]
    )
    
    # Update layout for better appearance
    fig.update_layout(
        plot_bgcolor='white',
        margin=dict(l=40, r=40, t=40, b=40),
        hovermode='closest',
        xaxis_title='',
        yaxis_title=y_axis_title,
        height=400
    )
    
    # Add hover information
    fig.update_traces(
        hovertemplate='Year: %{x}<br>'+y_axis_title+': %{y:.2f}',
    )
    
    return fig

def create_commission_pie_chart(exchange_data):
    """Create a pie chart showing commission distribution by exchange"""
    exchanges = list(exchange_data.keys())
    values = [sum(exchange_data[exchange]['monthly_commission']) for exchange in exchanges]
    
    # Create a DataFrame for the chart
    df = pd.DataFrame({
        'Exchange': exchanges,
        'Commissions': values
    })
    
    # Create the pie chart
    fig = px.pie(
        df,
        names='Exchange',
        values='Commissions',
        title='Monthly Commissions Distribution',
        color_discrete_sequence=px.colors.qualitative.Set2
    )
    
    # Update layout for better appearance
    fig.update_layout(
        margin=dict(l=20, r=20, t=40, b=20),
        height=400
    )
    
    # Add hover information
    fig.update_traces(
        textinfo='percent+label',
        hovertemplate='Exchange: %{label}<br>Commission: %{value:.2f}<br>Percentage: %{percent}'
    )
    
    return fig

def create_volume_pie_chart(exchange_data):
    """Create a pie chart showing volume distribution by exchange"""
    exchanges = list(exchange_data.keys())
    values = [sum(exchange_data[exchange]['monthly_volume']) for exchange in exchanges]
    
    # Create a DataFrame for the chart
    df = pd.DataFrame({
        'Exchange': exchanges,
        'Volume': values
    })
    
    # Create the pie chart
    fig = px.pie(
        df,
        names='Exchange',
        values='Volume',
        title='Monthly Volume Distribution',
        color_discrete_sequence=px.colors.qualitative.Pastel
    )
    
    # Update layout for better appearance
    fig.update_layout(
        margin=dict(l=20, r=20, t=40, b=20),
        height=400
    )
    
    # Add hover information
    fig.update_traces(
        textinfo='percent+label',
        hovertemplate='Exchange: %{label}<br>Volume: %{value:.2f}<br>Percentage: %{percent}'
    )
    
    return fig

def create_fees_table(vip_tiers, maker_fees, taker_fees):
    """Create a table showing VIP tiers and fees"""
    # Create a DataFrame for the table
    df = pd.DataFrame({
        'VIP Tier': vip_tiers,
        'Maker Fee %': [f"{fee:.3f}" for fee in maker_fees],
        'Taker Fee %': [f"{fee:.3f}" for fee in taker_fees]
    })
    
    return df

def create_fee_comparison_chart(exchange_data):
    """Create a bar chart comparing maker/taker fees across exchanges"""
    exchanges = list(exchange_data.keys())
    maker_fees = [exchange_data[exchange]['maker_fees'][0] for exchange in exchanges]  # Regular tier
    taker_fees = [exchange_data[exchange]['taker_fees'][0] for exchange in exchanges]  # Regular tier
    
    # Create DataFrame for the chart
    df = pd.DataFrame({
        'Exchange': exchanges + exchanges,
        'Fee Type': ['Maker Fee'] * len(exchanges) + ['Taker Fee'] * len(exchanges),
        'Fee Percentage': maker_fees + taker_fees
    })
    
    # Create the bar chart
    fig = px.bar(
        df,
        x='Exchange',
        y='Fee Percentage',
        color='Fee Type',
        title='Percentage Commissions Charged by Exchange',
        barmode='group',
        color_discrete_sequence=['#1E88E5', '#FFC107']
    )
    
    # Update layout for better appearance
    fig.update_layout(
        plot_bgcolor='white',
        margin=dict(l=40, r=40, t=40, b=40),
        hovermode='closest',
        xaxis_title='',
        yaxis_title='Fee Percentage',
        height=400,
        yaxis=dict(tickformat='.3f')
    )
    
    # Add hover information
    fig.update_traces(
        hovertemplate='Exchange: %{x}<br>Fee Type: %{customdata}<br>Percentage: %{y:.3f}%',
        customdata=[fee_type for fee_type in df['Fee Type']]
    )
    
    return fig
