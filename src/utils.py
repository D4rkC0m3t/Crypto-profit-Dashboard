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

    # Create enhanced bar chart with 3D effect
    fig = go.Figure()

    # Add simple bar chart with clean styling
    fig.add_trace(go.Bar(
        x=df['Date'],
        y=df['Value'],
        marker=dict(
            color='rgba(30, 136, 229, 0.8)',
            line=dict(color='rgba(30, 136, 229, 1.0)', width=1)
        ),
        hovertemplate='<b>%{x}</b><br>' + y_axis_title + ': $%{y:,.2f}<extra></extra>'
    ))

    # Add a line trace for trend visualization
    fig.add_trace(go.Scatter(
        x=df['Date'],
        y=df['Value'],
        mode='lines',
        line=dict(color='rgba(255, 152, 0, 0.7)', width=2),
        showlegend=False,
        hoverinfo='skip'
    ))

    # Update layout with enhanced styling
    fig.update_layout(
        title={
            'text': title,
            'font': {'size': 18}
        },
        xaxis_title='',
        yaxis_title=y_axis_title,
        plot_bgcolor='rgba(240, 240, 240, 0.8)',  # Light background for contrast
        margin=dict(l=40, r=40, t=60, b=40),
        height=400,
        hovermode='closest'
    )

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

    # Create enhanced bar chart with 3D effect
    fig = go.Figure()

    # Add simple bar chart with clean styling
    fig.add_trace(go.Bar(
        x=df['Year'],
        y=df['Value'],
        marker=dict(
            color='rgba(76, 175, 80, 0.8)',
            line=dict(color='rgba(76, 175, 80, 1.0)', width=1)
        ),
        hovertemplate='<b>%{x}</b><br>' + y_axis_title + ': $%{y:,.2f}<extra></extra>'
    ))

    # Add markers for emphasis
    fig.add_trace(go.Scatter(
        x=df['Year'],
        y=df['Value'],
        mode='markers',
        marker=dict(
            color='rgba(255, 255, 255, 0.9)',
            size=8,
            line=dict(color='rgba(76, 175, 80, 1.0)', width=2)
        ),
        showlegend=False,
        hoverinfo='skip'
    ))

    # Update layout with enhanced styling
    fig.update_layout(
        title={
            'text': title,
            'font': {'size': 18}
        },
        xaxis_title='',
        yaxis_title=y_axis_title,
        plot_bgcolor='rgba(240, 240, 240, 0.8)',  # Light background for contrast
        margin=dict(l=40, r=40, t=60, b=40),
        height=400,
        hovermode='closest'
    )

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

    # Create enhanced pie chart with 3D effect
    fig = px.pie(
        df,
        names='Exchange',
        values='Commissions',
        title='Monthly Commissions Distribution',
        color_discrete_sequence=px.colors.qualitative.Bold,
        hole=0.4  # Donut chart for 3D effect
    )

    # Add simple styling
    fig.update_traces(
        textposition='inside',
        textinfo='percent+label',
        textfont=dict(size=12),
        marker=dict(
            line=dict(color='#FFFFFF', width=1)
        ),
        hoverinfo='label+percent+value',
        hovertemplate='<b>%{label}</b><br>Commission: $%{value:,.2f}<br>Share: %{percent}<extra></extra>'
    )

    # Simple layout
    fig.update_layout(
        title_font=dict(size=16),
        margin=dict(l=20, r=20, t=40, b=20),
        height=400,
        showlegend=True
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

    # Create enhanced pie chart with 3D effect
    fig = px.pie(
        df,
        names='Exchange',
        values='Volume',
        title='Monthly Volume Distribution',
        color_discrete_sequence=px.colors.qualitative.Vivid,
        hole=0.4  # Donut chart for 3D effect
    )

    # Add simple styling
    fig.update_traces(
        textposition='inside',
        textinfo='percent+label',
        textfont=dict(size=12),
        marker=dict(
            line=dict(color='#FFFFFF', width=1)
        ),
        hoverinfo='label+percent+value',
        hovertemplate='<b>%{label}</b><br>Volume: $%{value:,.2f}<br>Share: %{percent}<extra></extra>'
    )

    # Simple layout
    fig.update_layout(
        title_font=dict(size=16),
        margin=dict(l=20, r=20, t=40, b=20),
        height=400,
        showlegend=True
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

    # Create enhanced bar chart with 3D effect using go.Figure
    fig = go.Figure()

    # Add maker fee bars with simple styling
    maker_data = df[df['Fee Type'] == 'Maker Fee']
    fig.add_trace(go.Bar(
        x=maker_data['Exchange'],
        y=maker_data['Fee Percentage'],
        name='Maker Fee',
        marker=dict(
            color='rgba(58, 71, 80, 0.8)',
            line=dict(color='rgba(58, 71, 80, 1.0)', width=1)
        ),
        hovertemplate='<b>%{x}</b><br>Maker Fee: %{y:.3f}%<extra></extra>'
    ))

    # Add taker fee bars with simple styling
    taker_data = df[df['Fee Type'] == 'Taker Fee']
    fig.add_trace(go.Bar(
        x=taker_data['Exchange'],
        y=taker_data['Fee Percentage'],
        name='Taker Fee',
        marker=dict(
            color='rgba(246, 78, 139, 0.8)',
            line=dict(color='rgba(246, 78, 139, 1.0)', width=1)
        ),
        hovertemplate='<b>%{x}</b><br>Taker Fee: %{y:.3f}%<extra></extra>'
    ))

    # Update layout with enhanced styling
    fig.update_layout(
        title={
            'text': 'Percentage Commissions Charged by Exchange',
            'font': {'size': 18}
        },
        xaxis_title='',
        yaxis_title='Fee Percentage',
        yaxis=dict(tickformat='.3f', ticksuffix='%'),
        barmode='group',
        bargap=0.15,  # Gap between bars of adjacent location coordinates
        bargroupgap=0.1,  # Gap between bars of the same location coordinates
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ),
        plot_bgcolor='rgba(240, 240, 240, 0.8)',  # Light background for contrast
        margin=dict(l=40, r=40, t=60, b=40),
        height=400
    )

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

    return fig
