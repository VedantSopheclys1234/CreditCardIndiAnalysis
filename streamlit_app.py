
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import seaborn as sns
import matplotlib.pyplot as plt 
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

# Page configuration
st.set_page_config(
    page_title="Credit Card Spending Analysis Dashboard",
    page_icon="💳",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
.main {
    padding-top: 2rem;
}
.stMetric {
    background-color: #f0f2f6;
    border: 1px solid #e0e0e0;
    padding: 1rem;
    border-radius: 0.5rem;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}
/* Add this for black font color in metrics */
[data-testid="stMetric"] div {
    color: black !important;
}
.chart-container {
    background-color: white;
    padding: 1rem;
    border-radius: 0.5rem;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    margin: 1rem 0;
}
</style>
""", unsafe_allow_html=True)

# Load data
@st.cache_data
def load_data():
    try:
        main_df = pd.read_csv('card_spending_trends.csv')
        main_df['Date'] = pd.to_datetime(main_df['Date'])

        detailed_df = pd.read_csv('detailed_card_spending.csv') 
        detailed_df['Date'] = pd.to_datetime(detailed_df['Date'])

        return main_df, detailed_df
    except FileNotFoundError:
        st.error("Data files not found. Please ensure card_spending_trends.csv and detailed_card_spending.csv are in the same directory.")
        return None, None

# Main title and description
st.title("💳 Credit Card Spending Analysis Dashboard")
st.markdown("### Interactive Analysis of Credit Card Spending Trends in India (2019-2025)")

# Load data
main_df, detailed_df = load_data()

if main_df is not None and detailed_df is not None:
    # Sidebar filters
    st.sidebar.header("📊 Dashboard Controls")

    # Date range selector
    min_date = main_df['Date'].min().date()
    max_date = main_df['Date'].max().date()

    date_range = st.sidebar.date_input(
        "Select Date Range:",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date
    )

    # Filter main data
    if len(date_range) == 2:
        filtered_main = main_df[
            (main_df['Date'].dt.date >= date_range[0]) & 
            (main_df['Date'].dt.date <= date_range[1])
        ]
        filtered_detailed = detailed_df[
            (detailed_df['Date'].dt.date >= date_range[0]) & 
            (detailed_df['Date'].dt.date <= date_range[1])
        ]
    else:
        filtered_main = main_df
        filtered_detailed = detailed_df

    # Analysis type selector
    analysis_type = st.sidebar.selectbox(
        "Select Analysis Type:",
        ["Overview", "Time Series Analysis", "Category Analysis", "Geographic Analysis", "Demographic Analysis"]
    )

    if analysis_type == "Overview":
        # Key metrics row
        st.header("📈 Key Performance Indicators")

        col1, col2, col3, col4 = st.columns(4)

        latest_data = filtered_main.iloc[-1]
        first_data = filtered_main.iloc[0] if len(filtered_main) > 1 else latest_data

        with col1:
            st.metric(
                "Total Spending (Billion INR)", 
                f"₹{latest_data['Total_Spending_Billion_INR']:.1f}B",
                f"{((latest_data['Total_Spending_Billion_INR'] / first_data['Total_Spending_Billion_INR']) - 1) * 100:.1f}%"
            )

        with col2:
            st.metric(
                "Active Cards (Millions)", 
                f"{latest_data['Active_Cards_Millions']:.1f}M",
                f"{((latest_data['Active_Cards_Millions'] / first_data['Active_Cards_Millions']) - 1) * 100:.1f}%"
            )

        with col3:
            st.metric(
                "Average Monthly Spend", 
                f"₹{latest_data['Avg_Monthly_Spend_INR']:,.0f}",
                f"{latest_data['Spend_Per_Card_Growth_YoY']:.1f}% YoY"
            )

        with col4:
            yoy_growth = latest_data['YoY_Growth_Spending']
            if pd.notna(yoy_growth):
                st.metric(
                    "YoY Growth Rate", 
                    f"{yoy_growth:.1f}%",
                    f"{'📈' if yoy_growth > 0 else '📉'}"
                )
            else:
                st.metric("YoY Growth Rate", "N/A")

        # Main trend chart
        st.header("📊 Spending and Cards Growth Trend")

        fig = make_subplots(
            specs=[[{"secondary_y": True}]],
            subplot_titles=["Credit Card Spending & Active Cards Growth"]
        )

        # Add spending trend
        fig.add_trace(
            go.Scatter(
                x=filtered_main['Date'],
                y=filtered_main['Total_Spending_Billion_INR'],
                mode='lines+markers',
                name='Total Spending (Billion INR)',
                line=dict(color='#1f77b4', width=3),
                hovertemplate='<b>%{x}</b><br>Spending: ₹%{y:.1f}B<extra></extra>'
            ),
            secondary_y=False,
        )

        # Add cards trend on secondary y-axis
        fig.add_trace(
            go.Scatter(
                x=filtered_main['Date'],
                y=filtered_main['Active_Cards_Millions'],
                mode='lines+markers',
                name='Active Cards (Millions)',
                line=dict(color='#ff7f0e', width=3),
                hovertemplate='<b>%{x}</b><br>Cards: %{y:.1f}M<extra></extra>'
            ),
            secondary_y=True,
        )

        # Update layout
        fig.update_xaxes(title_text="Date")
        fig.update_yaxes(title_text="Total Spending (Billion INR)", secondary_y=False)
        fig.update_yaxes(title_text="Active Cards (Millions)", secondary_y=True)
        fig.update_layout(
            title="Credit Card Market Growth Trajectory",
            hovermode='x unified',
            height=500,
            showlegend=True
        )

        st.plotly_chart(fig, use_container_width=True)

        # Summary insights
        st.header("🔍 Key Insights")

        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Growth Metrics")
            total_growth = ((latest_data['Total_Spending_Billion_INR'] / first_data['Total_Spending_Billion_INR']) - 1) * 100
            cards_growth = ((latest_data['Active_Cards_Millions'] / first_data['Active_Cards_Millions']) - 1) * 100

            st.write(f"• **Total spending growth**: {total_growth:.1f}% over the period")
            st.write(f"• **Active cards growth**: {cards_growth:.1f}% over the period") 
            st.write(f"• **Current average spend per card**: ₹{latest_data['Avg_Monthly_Spend_INR']:,}/month")

        with col2:
            st.subheader("Market Trends")
            st.write("• **Consistent upward trajectory** in both spending and card adoption")
            st.write("• **Significant acceleration post-2020** due to digital adoption")
            st.write("• **Seasonal patterns** visible with festival and year-end spikes")

    elif analysis_type == "Time Series Analysis":
        st.header("📈 Time Series Deep Dive")

        # Time series options
        metric_choice = st.selectbox(
            "Select Metric for Analysis:",
            ["Total_Spending_Billion_INR", "Active_Cards_Millions", "Avg_Monthly_Spend_INR", "YoY_Growth_Spending"]
        )

        # Create time series plot
        fig = px.line(
            filtered_main, 
            x='Date', 
            y=metric_choice,
            title=f"{metric_choice.replace('_', ' ').title()} Over Time",
            markers=True
        )

        fig.update_layout(
            height=500,
            hovermode='x unified'
        )

        st.plotly_chart(fig, use_container_width=True)

        # Seasonal analysis
        if len(filtered_main) > 12:
            st.subheader("📅 Seasonal Analysis")

            # Create month-wise analysis
            monthly_avg = filtered_main.groupby(filtered_main['Date'].dt.month)[metric_choice].mean().reset_index()
            monthly_avg['Month_Name'] = monthly_avg['Date'].apply(lambda x: pd.Timestamp(2024, x, 1).strftime('%B'))

            fig2 = px.bar(
                monthly_avg,
                x='Month_Name',
                y=metric_choice,
                title=f"Average {metric_choice.replace('_', ' ').title()} by Month"
            )

            st.plotly_chart(fig2, use_container_width=True)

    elif analysis_type == "Category Analysis":
        st.header("🛍️ Category-wise Spending Analysis")

        # Category filters
        categories = st.multiselect(
            "Select Categories:",
            filtered_detailed['Category'].unique(),
            default=filtered_detailed['Category'].unique()[:6]
        )

        if categories:
            category_data = filtered_detailed[filtered_detailed['Category'].isin(categories)]

            # Category spending over time
            category_trends = category_data.groupby(['Date', 'Category'])['Spending_Amount_Thousands_INR'].sum().reset_index()

            fig = px.area(
                category_trends,
                x='Date',
                y='Spending_Amount_Thousands_INR',
                color='Category',
                title="Category-wise Spending Trends"
            )

            fig.update_layout(height=500)
            st.plotly_chart(fig, use_container_width=True)

            # Category distribution
            col1, col2 = st.columns(2)

            with col1:
                total_by_category = category_data.groupby('Category')['Spending_Amount_Thousands_INR'].sum().sort_values(ascending=True)

                fig2 = px.bar(
                    x=total_by_category.values,
                    y=total_by_category.index,
                    orientation='h',
                    title="Total Spending by Category"
                )
                st.plotly_chart(fig2, use_container_width=True)

            with col2:
                fig3 = px.pie(
                    values=total_by_category.values,
                    names=total_by_category.index,
                    title="Category Distribution"
                )
                st.plotly_chart(fig3, use_container_width=True)

    elif analysis_type == "Geographic Analysis":
        st.header("🌍 Geographic Spending Analysis")

        # City analysis
        city_data = filtered_detailed.groupby(['City', 'Date'])['Spending_Amount_Thousands_INR'].sum().reset_index()

        # Top cities
        top_cities = filtered_detailed.groupby('City')['Spending_Amount_Thousands_INR'].sum().sort_values(ascending=False)

        col1, col2 = st.columns(2)

        with col1:
            fig = px.bar(
                x=top_cities.values,
                y=top_cities.index,
                orientation='h',
                title="Total Spending by City"
            )
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            # City trends over time
            city_choice = st.selectbox("Select City for Trend Analysis:", top_cities.index[:5])
            city_trend = city_data[city_data['City'] == city_choice]

            fig2 = px.line(
                city_trend,
                x='Date',
                y='Spending_Amount_Thousands_INR',
                title=f"Spending Trend for {city_choice}",
                markers=True
            )
            st.plotly_chart(fig2, use_container_width=True)

    elif analysis_type == "Demographic Analysis":
        st.header("👥 Demographic Spending Analysis")

        # Age group analysis
        st.subheader("Age Group Analysis")
        age_data = filtered_detailed.groupby(['Age_Group', 'Date'])['Spending_Amount_Thousands_INR'].sum().reset_index()

        fig = px.box(
            filtered_detailed,
            x='Age_Group',
            y='Spending_Amount_Thousands_INR',
            title="Spending Distribution by Age Group"
        )
        st.plotly_chart(fig, use_container_width=True)

        # Gender and Card Type analysis
        col1, col2 = st.columns(2)

        with col1:
            gender_data = filtered_detailed.groupby('Gender')['Spending_Amount_Thousands_INR'].sum()
            fig2 = px.pie(
                values=gender_data.values,
                names=gender_data.index,
                title="Spending by Gender"
            )
            st.plotly_chart(fig2, use_container_width=True)

        with col2:
            card_data = filtered_detailed.groupby('Card_Type')['Spending_Amount_Thousands_INR'].sum()
            fig3 = px.bar(
                x=card_data.index,
                y=card_data.values,
                title="Spending by Card Type"
            )
            st.plotly_chart(fig3, use_container_width=True)

    # Data export section
    st.sidebar.header("📥 Data Export")
    if st.sidebar.button("Download Main Dataset"):
        csv = filtered_main.to_csv(index=False)
        st.sidebar.download_button(
            label="Download CSV",
            data=csv,
            file_name="card_spending_main.csv",
            mime="text/csv"
        )

    if st.sidebar.button("Download Detailed Dataset"):
        csv = filtered_detailed.to_csv(index=False) 
        st.sidebar.download_button(
            label="Download Detailed CSV",
            data=csv,
            file_name="card_spending_detailed.csv",
            mime="text/csv"
        )

    # Footer
    st.markdown("---")
    st.markdown(
        """
        **Data Science Project: Credit Card Spending Analysis**  
        📊 Built with Streamlit | 💳 Data covers 2019-2025 period  
        🔍 Interactive dashboard for comprehensive spending pattern analysis
        """
    )

else:
    st.error("Failed to load data. Please check if the data files exist.")
