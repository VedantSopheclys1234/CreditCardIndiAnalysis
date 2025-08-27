import pandas as pd
import plotly.graph_objects as go
import json

# Load the data
data = [
    {"Year": 2019, "Category": "Grocery & Food", "Spending_Millions_INR": 82.78},
    {"Year": 2019, "Category": "Shopping & Retail", "Spending_Millions_INR": 66.22},
    {"Year": 2019, "Category": "Bills & Utilities", "Spending_Millions_INR": 49.95},
    {"Year": 2019, "Category": "Entertainment", "Spending_Millions_INR": 40.05},
    {"Year": 2019, "Category": "Travel", "Spending_Millions_INR": 33.28},
    {"Year": 2019, "Category": "Fuel", "Spending_Millions_INR": 26.61},
    {"Year": 2020, "Category": "Grocery & Food", "Spending_Millions_INR": 108.93},
    {"Year": 2020, "Category": "Shopping & Retail", "Spending_Millions_INR": 87.13},
    {"Year": 2020, "Category": "Bills & Utilities", "Spending_Millions_INR": 65.15},
    {"Year": 2020, "Category": "Entertainment", "Spending_Millions_INR": 52.28},
    {"Year": 2020, "Category": "Travel", "Spending_Millions_INR": 43.57},
    {"Year": 2020, "Category": "Fuel", "Spending_Millions_INR": 34.83},
    {"Year": 2021, "Category": "Grocery & Food", "Spending_Millions_INR": 140.52},
    {"Year": 2021, "Category": "Shopping & Retail", "Spending_Millions_INR": 112.41},
    {"Year": 2021, "Category": "Bills & Utilities", "Spending_Millions_INR": 84.31},
    {"Year": 2021, "Category": "Entertainment", "Spending_Millions_INR": 67.45},
    {"Year": 2021, "Category": "Travel", "Spending_Millions_INR": 56.21},
    {"Year": 2021, "Category": "Fuel", "Spending_Millions_INR": 44.97},
    {"Year": 2022, "Category": "Grocery & Food", "Spending_Millions_INR": 162.85},
    {"Year": 2022, "Category": "Shopping & Retail", "Spending_Millions_INR": 130.28},
    {"Year": 2022, "Category": "Bills & Utilities", "Spending_Millions_INR": 97.71},
    {"Year": 2022, "Category": "Entertainment", "Spending_Millions_INR": 78.17},
    {"Year": 2022, "Category": "Travel", "Spending_Millions_INR": 65.14},
    {"Year": 2022, "Category": "Fuel", "Spending_Millions_INR": 52.11},
    {"Year": 2023, "Category": "Grocery & Food", "Spending_Millions_INR": 185.42},
    {"Year": 2023, "Category": "Shopping & Retail", "Spending_Millions_INR": 148.34},
    {"Year": 2023, "Category": "Bills & Utilities", "Spending_Millions_INR": 111.25},
    {"Year": 2023, "Category": "Entertainment", "Spending_Millions_INR": 89.00},
    {"Year": 2023, "Category": "Travel", "Spending_Millions_INR": 74.17},
    {"Year": 2023, "Category": "Fuel", "Spending_Millions_INR": 59.34},
    {"Year": 2024, "Category": "Grocery & Food", "Spending_Millions_INR": 207.12},
    {"Year": 2024, "Category": "Shopping & Retail", "Spending_Millions_INR": 165.70},
    {"Year": 2024, "Category": "Bills & Utilities", "Spending_Millions_INR": 124.27},
    {"Year": 2024, "Category": "Entertainment", "Spending_Millions_INR": 99.42},
    {"Year": 2024, "Category": "Travel", "Spending_Millions_INR": 82.85},
    {"Year": 2024, "Category": "Fuel", "Spending_Millions_INR": 66.28},
    {"Year": 2025, "Category": "Grocery & Food", "Spending_Millions_INR": 155.93},
    {"Year": 2025, "Category": "Shopping & Retail", "Spending_Millions_INR": 124.75},
    {"Year": 2025, "Category": "Bills & Utilities", "Spending_Millions_INR": 93.56},
    {"Year": 2025, "Category": "Entertainment", "Spending_Millions_INR": 74.85},
    {"Year": 2025, "Category": "Travel", "Spending_Millions_INR": 62.37},
    {"Year": 2025, "Category": "Fuel", "Spending_Millions_INR": 49.90}
]

# Convert to DataFrame
df = pd.DataFrame(data)

# Pivot the data to have years as index and categories as columns
pivot_df = df.pivot(index='Year', columns='Category', values='Spending_Millions_INR')

# Define the categories in the order specified and colors
categories = ['Grocery & Food', 'Shopping & Retail', 'Bills & Utilities', 'Entertainment', 'Travel', 'Fuel']
colors = ['#1FB8CD', '#DB4545', '#2E8B57', '#5D878F', '#D2BA4C', '#B4413C']

# Create the figure
fig = go.Figure()

# Add each category as a stacked area
for i, category in enumerate(categories):
    # Abbreviate category names for legend (15 char limit)
    if category == 'Grocery & Food':
        category_abbrev = 'Grocery'
    elif category == 'Shopping & Retail':
        category_abbrev = 'Shopping'
    elif category == 'Bills & Utilities':
        category_abbrev = 'Bills'
    else:
        category_abbrev = category
    
    fig.add_trace(go.Scatter(
        x=pivot_df.index,
        y=pivot_df[category],
        fill='tonexty' if i > 0 else 'tozeroy',
        mode='none',
        name=category_abbrev,
        fillcolor=colors[i],
        line_color=colors[i],
        stackgroup='one',
        cliponaxis=False,
        hovertemplate='%{fullData.name}<br>Year: %{x}<br>Spending: ₹%{y:.0f}m<extra></extra>'
    ))

# Update layout
fig.update_layout(
    title='Spending Trends by Category 2019-2025',
    xaxis_title='Year',
    yaxis_title='Spending (₹m)',
    showlegend=True
)

# Save the chart
fig.write_image('spending_trends_stacked_area.png')