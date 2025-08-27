
"""
Credit Card Spending Analysis - Advanced Analytics Script
=========================================================

This script performs comprehensive analysis of credit card spending trends
including statistical analysis, forecasting, and pattern recognition.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Statistical and ML libraries
from scipy import stats
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import warnings
warnings.filterwarnings('ignore')

class CreditCardAnalyzer:
    """
    Comprehensive analyzer for credit card spending data
    """

    def __init__(self, main_data_path, detailed_data_path):
        """Initialize the analyzer with data paths"""
        self.main_df = pd.read_csv(main_data_path)
        self.detailed_df = pd.read_csv(detailed_data_path)

        # Convert date columns
        self.main_df['Date'] = pd.to_datetime(self.main_df['Date'])
        self.detailed_df['Date'] = pd.to_datetime(self.detailed_df['Date'])

        print("✅ Data loaded successfully!")
        print(f"Main dataset: {self.main_df.shape}")
        print(f"Detailed dataset: {self.detailed_df.shape}")

    def statistical_summary(self):
        """Generate comprehensive statistical summary"""
        print("\n" + "="*60)
        print("📊 STATISTICAL SUMMARY")
        print("="*60)

        # Basic statistics
        print("\n🔍 Main Dataset Statistics:")
        print(self.main_df[['Total_Spending_Billion_INR', 'Active_Cards_Millions', 'Avg_Monthly_Spend_INR']].describe())

        # Growth analysis
        latest_year = self.main_df['Year'].max()
        earliest_year = self.main_df['Year'].min()

        latest_spending = self.main_df[self.main_df['Year'] == latest_year]['Total_Spending_Billion_INR'].sum()
        earliest_spending = self.main_df[self.main_df['Year'] == earliest_year]['Total_Spending_Billion_INR'].sum()
        total_growth = ((latest_spending / earliest_spending) - 1) * 100

        print(f"\n📈 Overall Growth Analysis ({earliest_year}-{latest_year}):")
        print(f"Total spending growth: {total_growth:.1f}%")
        print(f"CAGR: {((latest_spending/earliest_spending)**(1/(latest_year-earliest_year)) - 1) * 100:.1f}%")

        return {
            'total_growth': total_growth,
            'earliest_year': earliest_year,
            'latest_year': latest_year
        }

    def trend_analysis(self):
        """Analyze spending trends and seasonality"""
        print("\n" + "="*60)
        print("📈 TREND ANALYSIS")
        print("="*60)

        # Monthly seasonality
        self.main_df['Month_Name'] = self.main_df['Date'].dt.strftime('%B')
        monthly_avg = self.main_df.groupby('Month')['Total_Spending_Billion_INR'].mean()

        print("\n🗓️ Monthly Seasonality (Average Spending by Month):")
        for month, spending in monthly_avg.items():
            month_name = pd.Timestamp(2024, month, 1).strftime('%B')
            print(f"{month_name}: ₹{spending:.1f}B")

        # Year-over-year growth analysis
        yearly_growth = self.main_df.groupby('Year').agg({
            'Total_Spending_Billion_INR': 'sum',
            'Active_Cards_Millions': 'mean'
        })

        yearly_growth['Spending_Growth'] = yearly_growth['Total_Spending_Billion_INR'].pct_change() * 100
        yearly_growth['Cards_Growth'] = yearly_growth['Active_Cards_Millions'].pct_change() * 100

        print("\n📊 Year-over-Year Growth:")
        for year, row in yearly_growth.iterrows():
            if not np.isnan(row['Spending_Growth']):
                print(f"{year}: Spending {row['Spending_Growth']:.1f}%, Cards {row['Cards_Growth']:.1f}%")

        return yearly_growth

    def category_analysis(self):
        """Analyze spending patterns by category"""
        print("\n" + "="*60)  
        print("🛍️ CATEGORY ANALYSIS")
        print("="*60)

        # Top categories
        category_totals = self.detailed_df.groupby('Category')['Spending_Amount_Thousands_INR'].sum().sort_values(ascending=False)
        total_spending = category_totals.sum()

        print("\n🏆 Top Categories by Total Spending:")
        for i, (category, spending) in enumerate(category_totals.head(8).items(), 1):
            percentage = (spending / total_spending) * 100
            print(f"{i}. {category}: ₹{spending/1000:.1f}M ({percentage:.1f}%)")

        # Category growth trends
        category_yearly = self.detailed_df.groupby(['Year', 'Category'])['Spending_Amount_Thousands_INR'].sum().unstack(fill_value=0)
        category_growth = category_yearly.pct_change() * 100

        print("\n📈 Category Growth (2024 vs 2023):")
        if 2024 in category_growth.index and 2023 in category_growth.index:
            growth_2024 = category_growth.loc[2024].sort_values(ascending=False)
            for category, growth in growth_2024.head(5).items():
                if not np.isnan(growth):
                    print(f"{category}: {growth:.1f}%")

        return category_totals

    def demographic_analysis(self):
        """Analyze spending by demographics"""
        print("\n" + "="*60)
        print("👥 DEMOGRAPHIC ANALYSIS") 
        print("="*60)

        # Age group analysis
        age_spending = self.detailed_df.groupby('Age_Group')['Spending_Amount_Thousands_INR'].agg(['mean', 'sum'])
        age_spending['percentage'] = (age_spending['sum'] / age_spending['sum'].sum()) * 100

        print("\n🎂 Spending by Age Group:")
        for age_group, row in age_spending.iterrows():
            print(f"{age_group}: Avg ₹{row['mean']:.1f}K, Total Share {row['percentage']:.1f}%")

        # Gender analysis
        gender_spending = self.detailed_df.groupby('Gender')['Spending_Amount_Thousands_INR'].agg(['mean', 'sum'])
        gender_spending['percentage'] = (gender_spending['sum'] / gender_spending['sum'].sum()) * 100

        print("\n⚥ Spending by Gender:")
        for gender, row in gender_spending.iterrows():
            print(f"{gender}: Avg ₹{row['mean']:.1f}K, Total Share {row['percentage']:.1f}%")

        # Card type analysis
        card_spending = self.detailed_df.groupby('Card_Type')['Spending_Amount_Thousands_INR'].agg(['mean', 'sum'])
        card_spending['percentage'] = (card_spending['sum'] / card_spending['sum'].sum()) * 100

        print("\n💳 Spending by Card Type:")
        for card_type, row in card_spending.iterrows():
            print(f"{card_type}: Avg ₹{row['mean']:.1f}K, Total Share {row['percentage']:.1f}%")

    def geographic_analysis(self):
        """Analyze spending by geography"""
        print("\n" + "="*60)
        print("🌍 GEOGRAPHIC ANALYSIS")
        print("="*60)

        # City-wise analysis
        city_spending = self.detailed_df.groupby('City')['Spending_Amount_Thousands_INR'].agg(['mean', 'sum', 'count'])
        city_spending['percentage'] = (city_spending['sum'] / city_spending['sum'].sum()) * 100
        city_spending = city_spending.sort_values('sum', ascending=False)

        print("\n🏙️ Top Cities by Total Spending:")
        for i, (city, row) in enumerate(city_spending.head(8).iterrows(), 1):
            print(f"{i}. {city}: ₹{row['sum']/1000:.1f}M ({row['percentage']:.1f}%), Avg: ₹{row['mean']:.1f}K")

    def customer_segmentation(self):
        """Perform customer segmentation using clustering"""
        print("\n" + "="*60)
        print("🎯 CUSTOMER SEGMENTATION")
        print("="*60)

        # Prepare data for clustering
        segment_data = self.detailed_df.groupby(['Age_Group', 'Gender', 'Card_Type']).agg({
            'Spending_Amount_Thousands_INR': ['mean', 'sum', 'count'],
            'Transaction_Count': 'mean',
            'Avg_Transaction_Amount_INR': 'mean'
        }).round(2)

        # Flatten column names
        segment_data.columns = ['_'.join(col) for col in segment_data.columns]
        segment_data = segment_data.reset_index()

        # Select features for clustering
        features = ['Spending_Amount_Thousands_INR_mean', 'Spending_Amount_Thousands_INR_sum', 
                   'Transaction_Count_mean', 'Avg_Transaction_Amount_INR_mean']

        X = segment_data[features].fillna(0)

        # Standardize features
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)

        # Perform K-means clustering
        kmeans = KMeans(n_clusters=4, random_state=42)
        segment_data['Cluster'] = kmeans.fit_predict(X_scaled)

        print("\n🔍 Customer Segments Identified:")
        for cluster in range(4):
            cluster_data = segment_data[segment_data['Cluster'] == cluster]
            avg_spending = cluster_data['Spending_Amount_Thousands_INR_mean'].mean()
            avg_transactions = cluster_data['Transaction_Count_mean'].mean()

            print(f"\nCluster {cluster + 1}: {len(cluster_data)} segments")
            print(f"  - Average spending: ₹{avg_spending:.1f}K")
            print(f"  - Average transactions: {avg_transactions:.0f}")

            # Show top demographics in this cluster
            top_demo = cluster_data.nlargest(3, 'Spending_Amount_Thousands_INR_sum')
            for _, row in top_demo.iterrows():
                print(f"    • {row['Age_Group']} {row['Gender']} {row['Card_Type']}: ₹{row['Spending_Amount_Thousands_INR_mean']:.1f}K")

    def spending_forecasting(self):
        """Build a simple forecasting model"""
        print("\n" + "="*60)
        print("🔮 SPENDING FORECAST")
        print("="*60)

        # Prepare time series features
        self.main_df = self.main_df.sort_values('Date')
        self.main_df['Days_Since_Start'] = (self.main_df['Date'] - self.main_df['Date'].min()).dt.days
        self.main_df['Month_Sin'] = np.sin(2 * np.pi * self.main_df['Month'] / 12)
        self.main_df['Month_Cos'] = np.cos(2 * np.pi * self.main_df['Month'] / 12)

        # Features for prediction
        features = ['Days_Since_Start', 'Month_Sin', 'Month_Cos', 'Active_Cards_Millions', 'Seasonal_Factor']
        target = 'Total_Spending_Billion_INR'

        # Prepare data
        X = self.main_df[features].fillna(method='bfill')
        y = self.main_df[target]

        # Train-test split (use last 12 months as test)
        split_idx = len(X) - 12
        X_train, X_test = X[:split_idx], X[split_idx:]
        y_train, y_test = y[:split_idx], y[split_idx:]

        # Train Random Forest model
        model = RandomForestRegressor(n_estimators=100, random_state=42)
        model.fit(X_train, y_train)

        # Make predictions
        y_pred = model.predict(X_test)

        # Evaluate model
        mae = mean_absolute_error(y_test, y_pred)
        rmse = np.sqrt(mean_squared_error(y_test, y_pred))
        r2 = r2_score(y_test, y_pred)

        print(f"\n📊 Model Performance:")
        print(f"Mean Absolute Error: ₹{mae:.1f}B")
        print(f"Root Mean Square Error: ₹{rmse:.1f}B") 
        print(f"R² Score: {r2:.3f}")

        # Feature importance
        feature_importance = pd.DataFrame({
            'feature': features,
            'importance': model.feature_importances_
        }).sort_values('importance', ascending=False)

        print(f"\n🎯 Feature Importance:")
        for _, row in feature_importance.iterrows():
            print(f"{row['feature']}: {row['importance']:.3f}")

        # Generate future predictions (next 6 months)
        print(f"\n🔮 Next 6 Months Forecast:")
        last_date = self.main_df['Date'].max()

        for i in range(1, 7):
            future_date = last_date + pd.DateOffset(months=i)
            future_features = {
                'Days_Since_Start': (future_date - self.main_df['Date'].min()).days,
                'Month_Sin': np.sin(2 * np.pi * future_date.month / 12),
                'Month_Cos': np.cos(2 * np.pi * future_date.month / 12),
                'Active_Cards_Millions': self.main_df['Active_Cards_Millions'].iloc[-1] * (1 + 0.01),  # Assume 1% monthly growth
                'Seasonal_Factor': 1.1 if future_date.month in [10, 11, 12] else 1.0  # Festival season
            }

            future_X = pd.DataFrame([future_features])
            prediction = model.predict(future_X)[0]

            print(f"{future_date.strftime('%B %Y')}: ₹{prediction:.1f}B")

    def generate_insights(self):
        """Generate key business insights"""
        print("\n" + "="*60)
        print("💡 KEY BUSINESS INSIGHTS")
        print("="*60)

        insights = []

        # Growth insights
        latest_growth = self.main_df['YoY_Growth_Spending'].dropna().iloc[-1]
        if latest_growth > 20:
            insights.append("🚀 Experiencing strong double-digit growth in card spending")
        elif latest_growth > 10:
            insights.append("📈 Maintaining healthy growth momentum")
        else:
            insights.append("📊 Growth is stabilizing")

        # Category insights
        top_category = self.detailed_df.groupby('Category')['Spending_Amount_Thousands_INR'].sum().idxmax()
        insights.append(f"🛍️ '{top_category}' dominates spending categories")

        # Demographic insights
        top_age_group = self.detailed_df.groupby('Age_Group')['Spending_Amount_Thousands_INR'].sum().idxmax()
        insights.append(f"👥 '{top_age_group}' age group shows highest spending")

        # Geographic insights
        top_city = self.detailed_df.groupby('City')['Spending_Amount_Thousands_INR'].sum().idxmax()
        insights.append(f"🏙️ '{top_city}' leads in total card spending")

        # Seasonal insights
        peak_month = self.main_df.groupby('Month')['Total_Spending_Billion_INR'].mean().idxmax()
        peak_month_name = pd.Timestamp(2024, peak_month, 1).strftime('%B')
        insights.append(f"🗓️ '{peak_month_name}' shows peak seasonal spending")

        print("\n".join(f"{i+1}. {insight}" for i, insight in enumerate(insights)))

        return insights

    def run_complete_analysis(self):
        """Run the complete analysis pipeline"""
        print("🎉 STARTING COMPREHENSIVE CREDIT CARD SPENDING ANALYSIS")
        print("="*80)

        # Run all analyses
        stats = self.statistical_summary()
        trends = self.trend_analysis()
        categories = self.category_analysis()
        self.demographic_analysis()
        self.geographic_analysis()
        self.customer_segmentation()
        self.spending_forecasting()
        insights = self.generate_insights()

        print("\n" + "="*80)
        print("✅ ANALYSIS COMPLETE!")
        print("="*80)

        return {
            'stats': stats,
            'trends': trends,
            'categories': categories,
            'insights': insights
        }

# Main execution
if __name__ == "__main__":
    # Initialize analyzer
    analyzer = CreditCardAnalyzer('card_spending_trends.csv', 'detailed_card_spending.csv')

    # Run complete analysis
    results = analyzer.run_complete_analysis()
