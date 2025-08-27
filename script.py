# Let me start by creating a comprehensive data science project structure
# First, let me create sample data based on the trends I found in my research

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import warnings
warnings.filterwarnings('ignore')

# Set random seed for reproducibility
np.random.seed(42)

# Create a comprehensive dataset based on real trends from research
def create_card_spending_dataset():
    # Date range from 2019 to 2025 based on the trends found
    start_date = datetime(2019, 1, 1)
    end_date = datetime(2025, 8, 1)
    
    # Create monthly date range
    date_range = pd.date_range(start=start_date, end=end_date, freq='M')
    
    # Create base spending data with realistic trends
    base_data = []
    
    # Based on research: India had ~54M cards in 2019, ~108M by Dec 2024
    # Credit card spending grew significantly, especially post-2020
    # Average spend per card was around ₹16,911 in Jan 2025
    
    for i, date in enumerate(date_range):
        year = date.year
        month = date.month
        
        # Base metrics from research
        if year <= 2019:
            active_cards = 54_000_000 + (i * 500_000)  # Growing from 54M
            avg_monthly_spend = 12_000  # Lower initially
        elif year == 2020:
            # COVID impact - spending dipped initially then recovered
            active_cards = 60_000_000 + (i-12) * 1_000_000
            if month <= 6:  # COVID impact
                avg_monthly_spend = 8_000 + (month * 500)
            else:  # Recovery
                avg_monthly_spend = 10_000 + (month * 800)
        elif year == 2021:
            active_cards = 70_000_000 + (i-24) * 1_500_000
            avg_monthly_spend = 13_000 + (month * 200)
        elif year == 2022:
            active_cards = 80_000_000 + (i-36) * 1_800_000
            avg_monthly_spend = 14_500 + (month * 150)
        elif year == 2023:
            active_cards = 95_000_000 + (i-48) * 2_000_000
            avg_monthly_spend = 15_500 + (month * 100)
        elif year == 2024:
            active_cards = 108_000_000 + (i-60) * 200_000
            avg_monthly_spend = 16_000 + (month * 80)
        else:  # 2025
            active_cards = 111_000_000 + (i-72) * 100_000
            avg_monthly_spend = 16_800 + (month * 50)
        
        # Add seasonal patterns
        seasonal_multiplier = 1.0
        if month in [10, 11, 12]:  # Festival season in India
            seasonal_multiplier = 1.3
        elif month in [3, 4]:  # End of financial year
            seasonal_multiplier = 1.15
        elif month in [6, 7, 8]:  # Monsoon/back to school
            seasonal_multiplier = 0.9
        
        # Calculate total spending
        total_spending = active_cards * avg_monthly_spend * seasonal_multiplier
        
        # Add some random variation
        noise = np.random.normal(0, 0.05)  # 5% noise
        total_spending = total_spending * (1 + noise)
        avg_monthly_spend = avg_monthly_spend * (1 + noise)
        
        base_data.append({
            'Date': date,
            'Year': year,
            'Month': month,
            'Quarter': f'Q{(month-1)//3 + 1}',
            'Active_Cards_Millions': round(active_cards / 1_000_000, 2),
            'Avg_Monthly_Spend_INR': round(avg_monthly_spend),
            'Total_Spending_Billion_INR': round(total_spending / 1_000_000_000, 2),
            'Seasonal_Factor': round(seasonal_multiplier, 2)
        })
    
    df = pd.DataFrame(base_data)
    
    # Add more derived metrics
    df['YoY_Growth_Spending'] = df['Total_Spending_Billion_INR'].pct_change(12) * 100
    df['MoM_Growth_Spending'] = df['Total_Spending_Billion_INR'].pct_change() * 100
    df['Cards_Growth_YoY'] = df['Active_Cards_Millions'].pct_change(12) * 100
    df['Spend_Per_Card_Growth_YoY'] = df['Avg_Monthly_Spend_INR'].pct_change(12) * 100
    
    return df

# Create the main dataset
card_spending_df = create_card_spending_dataset()

# Display basic info about the dataset
print("Dataset Overview:")
print("="*50)
print(f"Shape: {card_spending_df.shape}")
print(f"Date Range: {card_spending_df['Date'].min()} to {card_spending_df['Date'].max()}")
print("\nFirst few rows:")
print(card_spending_df.head())

print("\nDataset Info:")
print(card_spending_df.info())

print("\nBasic Statistics:")
print(card_spending_df.describe())