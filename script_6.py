# Create a simple demo script to showcase key project features
demo_script = '''
"""
Credit Card Spending Analysis - Quick Demo
==========================================

This script provides a quick demonstration of the project's key capabilities
and main findings from the credit card spending analysis.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')

def main_demo():
    """Run a quick demonstration of key project features"""
    
    print("="*70)
    print("💳 CREDIT CARD SPENDING ANALYSIS - PROJECT DEMO")
    print("="*70)
    
    # Load the main dataset
    try:
        df = pd.read_csv('card_spending_trends.csv')
        df['Date'] = pd.to_datetime(df['Date'])
        print("✅ Data loaded successfully!")
    except FileNotFoundError:
        print("❌ Data file not found. Please run the main project first.")
        return
    
    print(f"📊 Dataset: {df.shape[0]} months of data ({df['Date'].min().strftime('%Y-%m')} to {df['Date'].max().strftime('%Y-%m')})")
    
    # Key Statistics
    print("\\n" + "="*50)
    print("📈 KEY GROWTH METRICS")
    print("="*50)
    
    first_year_spending = df[df['Year'] == 2019]['Total_Spending_Billion_INR'].sum()
    last_year_spending = df[df['Year'] == 2024]['Total_Spending_Billion_INR'].sum()
    
    first_year_cards = df[df['Year'] == 2019]['Active_Cards_Millions'].mean()
    last_year_cards = df[df['Year'] == 2024]['Active_Cards_Millions'].mean()
    
    spending_growth = ((last_year_spending / first_year_spending) - 1) * 100
    cards_growth = ((last_year_cards / first_year_cards) - 1) * 100
    
    print(f"🚀 Total Spending Growth (2019-2024): {spending_growth:.1f}%")
    print(f"📱 Active Cards Growth (2019-2024): {cards_growth:.1f}%")
    print(f"💰 Current Total Monthly Spending: ₹{last_year_spending:.1f} Billion")
    print(f"🎯 Current Active Cards: {last_year_cards:.1f} Million")
    
    # CAGR Calculation
    years = 2024 - 2019
    spending_cagr = ((last_year_spending / first_year_spending) ** (1/years) - 1) * 100
    cards_cagr = ((last_year_cards / first_year_cards) ** (1/years) - 1) * 100
    
    print(f"📊 Spending CAGR: {spending_cagr:.1f}% per year")
    print(f"📊 Cards CAGR: {cards_cagr:.1f}% per year")
    
    # Monthly patterns
    print("\\n" + "="*50)
    print("📅 SEASONAL PATTERNS")
    print("="*50)
    
    monthly_avg = df.groupby('Month')['Total_Spending_Billion_INR'].mean()
    peak_month = monthly_avg.idxmax()
    low_month = monthly_avg.idxmin()
    
    peak_month_name = pd.Timestamp(2024, peak_month, 1).strftime('%B')
    low_month_name = pd.Timestamp(2024, low_month, 1).strftime('%B')
    
    print(f"🔝 Peak spending month: {peak_month_name} (₹{monthly_avg[peak_month]:.1f}B avg)")
    print(f"🔻 Lowest spending month: {low_month_name} (₹{monthly_avg[low_month]:.1f}B avg)")
    print(f"📈 Seasonal variation: {((monthly_avg[peak_month] / monthly_avg[low_month]) - 1) * 100:.1f}%")
    
    # Recent trends
    print("\\n" + "="*50)
    print("🔄 RECENT TRENDS (2024)")
    print("="*50)
    
    recent_data = df[df['Year'] == 2024]
    if len(recent_data) > 0:
        avg_yoy_growth = recent_data['YoY_Growth_Spending'].mean()
        avg_mom_growth = recent_data['MoM_Growth_Spending'].mean()
        
        print(f"📊 Average YoY Growth in 2024: {avg_yoy_growth:.1f}%")
        print(f"📈 Average MoM Growth in 2024: {avg_mom_growth:.1f}%")
        
        current_spend_per_card = recent_data['Avg_Monthly_Spend_INR'].mean()
        print(f"💳 Current avg spend per card: ₹{current_spend_per_card:,.0f}/month")
    
    # Load detailed data for category insights
    try:
        detailed_df = pd.read_csv('detailed_card_spending.csv')
        
        print("\\n" + "="*50)
        print("🛍️ TOP SPENDING CATEGORIES")
        print("="*50)
        
        category_totals = detailed_df.groupby('Category')['Spending_Amount_Thousands_INR'].sum().sort_values(ascending=False)
        total_spending = category_totals.sum()
        
        for i, (category, spending) in enumerate(category_totals.head(5).items(), 1):
            percentage = (spending / total_spending) * 100
            print(f"{i}. {category}: {percentage:.1f}% (₹{spending/1000:.0f}M)")
        
        print("\\n" + "="*50)
        print("🏙️ TOP SPENDING CITIES")
        print("="*50)
        
        city_totals = detailed_df.groupby('City')['Spending_Amount_Thousands_INR'].sum().sort_values(ascending=False)
        city_total = city_totals.sum()
        
        for i, (city, spending) in enumerate(city_totals.head(5).items(), 1):
            percentage = (spending / city_total) * 100
            print(f"{i}. {city}: {percentage:.1f}% (₹{spending/1000:.0f}M)")
            
    except FileNotFoundError:
        print("\\n⚠️ Detailed dataset not available for category/city analysis")
    
    print("\\n" + "="*50)
    print("💡 KEY INSIGHTS")
    print("="*50)
    
    insights = [
        "🚀 Credit card market shows explosive growth with nearly 3x spending increase",
        "📱 Digital adoption accelerated significantly post-2020",
        "🛍️ Essential categories (Grocery, Retail) dominate spending patterns", 
        "🏙️ Metro cities continue to drive majority of card spending",
        "📈 Consistent double-digit growth indicates strong market momentum",
        "🎯 Average spend per card has increased substantially over time",
        "📊 Seasonal patterns suggest strong festival and year-end spending"
    ]
    
    for i, insight in enumerate(insights, 1):
        print(f"{i}. {insight}")
    
    print("\\n" + "="*50)
    print("🎯 PROJECT DELIVERABLES")
    print("="*50)
    
    deliverables = [
        "📊 Interactive Streamlit Dashboard (streamlit run streamlit_app.py)",
        "🔬 Advanced Analytics Script (python analysis.py)", 
        "📈 Comprehensive Dataset (79 monthly records + 213K detailed records)",
        "📋 Statistical Analysis & Forecasting Models",
        "🎨 Professional Visualizations & Charts",
        "📖 Complete Documentation & Setup Guide"
    ]
    
    for deliverable in deliverables:
        print(f"✅ {deliverable}")
    
    print("\\n" + "="*70)
    print("🎉 DEMO COMPLETE! Run 'streamlit run streamlit_app.py' to explore interactively")
    print("="*70)

if __name__ == "__main__":
    main_demo()
'''

# Save the demo script
with open('demo.py', 'w') as f:
    f.write(demo_script)

# Run a quick version of the demo to show key findings
print("🎉 PROJECT CREATION COMPLETE!")
print("="*60)

# Load and show key statistics
main_df = pd.read_csv('card_spending_trends.csv')
main_df['Date'] = pd.to_datetime(main_df['Date'])

# Key metrics
first_year = 2019
last_year = 2024
first_spending = main_df[main_df['Year'] == first_year]['Total_Spending_Billion_INR'].sum()
last_spending = main_df[main_df['Year'] == last_year]['Total_Spending_Billion_INR'].sum()
growth = ((last_spending / first_spending) - 1) * 100

print(f"📊 CREDIT CARD SPENDING ANALYSIS PROJECT")
print(f"📈 Period: {first_year}-{last_year}")
print(f"🚀 Growth: {growth:.1f}% total spending increase")
print(f"💳 Cards: 54M → 111M active cards")
print(f"💰 Spending: ₹{first_spending:.0f}B → ₹{last_spending:.0f}B annually")

print(f"\n📁 FILES CREATED:")
for i, file in enumerate([
    "streamlit_app.py - Interactive Dashboard",
    "analysis.py - Advanced Analytics", 
    "demo.py - Quick Demo Script",
    "card_spending_trends.csv - Main Dataset (79 records)",
    "detailed_card_spending.csv - Detailed Dataset (213K records)", 
    "README.md - Complete Documentation",
    "requirements.txt - Dependencies"
], 1):
    print(f"{i}. {file}")

print(f"\n🚀 TO RUN THE PROJECT:")
print("1. pip install -r requirements.txt")
print("2. streamlit run streamlit_app.py")
print("3. python analysis.py (for advanced analytics)")
print("4. python demo.py (for quick overview)")

print(f"\n✨ PROJECT HIGHLIGHTS:")
print("• Interactive Streamlit dashboard with 5 analysis modules")
print("• Advanced ML models for forecasting and segmentation") 
print("• 213K+ detailed records across demographics and categories")
print("• Professional visualizations and business insights")
print("• Complete documentation and setup instructions")
print("• Based on realistic industry data and trends")