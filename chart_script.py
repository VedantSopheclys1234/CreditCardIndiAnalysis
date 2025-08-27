import pandas as pd
import plotly.graph_objects as go
from datetime import datetime

# Create the dataset
data = [
    {"Date": "2019-01-31", "Total_Spending_Billion_INR": 664.09, "Active_Cards_Millions": 54.0, "Year": 2019, "YoY_Growth_Spending": None},
    {"Date": "2019-02-28", "Total_Spending_Billion_INR": 649.48, "Active_Cards_Millions": 54.5, "Year": 2019, "YoY_Growth_Spending": None},
    {"Date": "2019-03-31", "Total_Spending_Billion_INR": 783.58, "Active_Cards_Millions": 55.0, "Year": 2019, "YoY_Growth_Spending": None},
    {"Date": "2019-04-30", "Total_Spending_Billion_INR": 824.22, "Active_Cards_Millions": 55.5, "Year": 2019, "YoY_Growth_Spending": None},
    {"Date": "2019-05-31", "Total_Spending_Billion_INR": 664.13, "Active_Cards_Millions": 56.0, "Year": 2019, "YoY_Growth_Spending": None},
    {"Date": "2020-01-31", "Total_Spending_Billion_INR": 496.48, "Active_Cards_Millions": 60.0, "Year": 2020, "YoY_Growth_Spending": -25.24},
    {"Date": "2020-06-30", "Total_Spending_Billion_INR": 594.69, "Active_Cards_Millions": 65.0, "Year": 2020, "YoY_Growth_Spending": -14.37},
    {"Date": "2020-12-31", "Total_Spending_Billion_INR": 1208.83, "Active_Cards_Millions": 70.0, "Year": 2020, "YoY_Growth_Spending": 29.85},
    {"Date": "2021-06-30", "Total_Spending_Billion_INR": 1164.95, "Active_Cards_Millions": 78.0, "Year": 2021, "YoY_Growth_Spending": 95.92},
    {"Date": "2021-12-31", "Total_Spending_Billion_INR": 1779.96, "Active_Cards_Millions": 85.5, "Year": 2021, "YoY_Growth_Spending": 47.25},
    {"Date": "2022-06-30", "Total_Spending_Billion_INR": 1593.31, "Active_Cards_Millions": 93.8, "Year": 2022, "YoY_Growth_Spending": 36.76},
    {"Date": "2022-12-31", "Total_Spending_Billion_INR": 1980.42, "Active_Cards_Millions": 101.5, "Year": 2022, "YoY_Growth_Spending": 11.26},
    {"Date": "2023-06-30", "Total_Spending_Billion_INR": 1860.64, "Active_Cards_Millions": 107.0, "Year": 2023, "YoY_Growth_Spending": 16.78},
    {"Date": "2023-12-31", "Total_Spending_Billion_INR": 2663.97, "Active_Cards_Millions": 108.8, "Year": 2023, "YoY_Growth_Spending": 34.52},
    {"Date": "2024-06-30", "Total_Spending_Billion_INR": 2068.96, "Active_Cards_Millions": 110.2, "Year": 2024, "YoY_Growth_Spending": 11.19},
    {"Date": "2024-12-31", "Total_Spending_Billion_INR": 2532.95, "Active_Cards_Millions": 111.0, "Year": 2024, "YoY_Growth_Spending": -4.92},
    {"Date": "2025-06-30", "Total_Spending_Billion_INR": 2223.43, "Active_Cards_Millions": 116.5, "Year": 2025, "YoY_Growth_Spending": 7.47}
]

# Convert to DataFrame and sort by date
df = pd.DataFrame(data)
df['Date'] = pd.to_datetime(df['Date'])
df = df.sort_values('Date')

# Create figure with secondary y-axis
fig = go.Figure()

# Add spending line (primary y-axis)
fig.add_trace(go.Scatter(
    x=df['Date'],
    y=df['Total_Spending_Billion_INR'],
    mode='lines+markers',
    name='Spending',
    line=dict(color='#1FB8CD', width=3),
    marker=dict(size=6, color='#1FB8CD'),
    hovertemplate='Date: %{x}<br>Spending: %{y:.1f}B INR<extra></extra>',
    yaxis='y1'
))

# Add active cards line (secondary y-axis)
fig.add_trace(go.Scatter(
    x=df['Date'],
    y=df['Active_Cards_Millions'],
    mode='lines+markers',
    name='Active Cards',
    line=dict(color='#DB4545', width=3, dash='dash'),
    marker=dict(size=6, color='#DB4545'),
    hovertemplate='Date: %{x}<br>Cards: %{y:.1f}M<extra></extra>',
    yaxis='y2'
))

# Add COVID-19 impact marker
fig.add_trace(go.Scatter(
    x=['2020-01-31'],
    y=[496.48],
    mode='markers',
    name='COVID Impact',
    marker=dict(size=12, color='#2E8B57', symbol='star'),
    hovertemplate='COVID Impact<br>Jan 2020<extra></extra>',
    yaxis='y1'
))

# Add recovery marker
fig.add_trace(go.Scatter(
    x=['2021-12-31'],
    y=[1779.96],
    mode='markers',
    name='Recovery',
    marker=dict(size=12, color='#D2BA4C', symbol='diamond'),
    hovertemplate='Recovery Phase<br>Dec 2021<extra></extra>',
    yaxis='y1'
))

# Update layout with secondary y-axis
fig.update_layout(
    title='Credit Card Growth 2019-2025',
    xaxis_title='Date',
    yaxis=dict(
        title='Spending (B)',
        side='left'
    ),
    yaxis2=dict(
        title='Cards (M)',
        overlaying='y',
        side='right'
    ),
    legend=dict(orientation='h', yanchor='bottom', y=1.05, xanchor='center', x=0.5),
    hovermode='x unified'
)

# Save the chart
fig.write_image('credit_card_spending_chart.png')