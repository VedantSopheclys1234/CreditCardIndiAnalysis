# Create category analysis for visualization
category_analysis = detailed_df.groupby(['Date', 'Category']).agg({
    'Spending_Amount_Thousands_INR': 'sum',
    'Transaction_Count': 'sum'
}).reset_index()

# Get top categories by total spending
top_categories = detailed_df.groupby('Category')['Spending_Amount_Thousands_INR'].sum().sort_values(ascending=False).head(6)
print("Top 6 Categories by Total Spending:")
print(top_categories)

# Prepare data for category trends chart
category_trends = category_analysis[category_analysis['Category'].isin(top_categories.index)]
category_trends['Year'] = category_trends['Date'].dt.year

# Create yearly summary for chart
yearly_category = category_trends.groupby(['Year', 'Category'])['Spending_Amount_Thousands_INR'].sum().reset_index()
yearly_category['Spending_Millions_INR'] = yearly_category['Spending_Amount_Thousands_INR'] / 1000

print("\nYearly Category Trends (Top 6):")
print(yearly_category.head(10))