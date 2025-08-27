# Save the main dataset and create additional detailed datasets
card_spending_df.to_csv('card_spending_trends.csv', index=False)

# Create a more detailed transactional dataset by category and demographics
def create_detailed_spending_dataset():
    # Categories based on research
    categories = ['Grocery & Food', 'Entertainment', 'Shopping & Retail', 'Travel', 
                 'Bills & Utilities', 'Fuel', 'Healthcare', 'Education', 'Others']
    
    # Cities based on research - top spending cities in India
    cities = ['Mumbai', 'Delhi NCR', 'Bangalore', 'Chennai', 'Hyderabad', 'Pune', 
             'Kolkata', 'Ahmedabad', 'Surat', 'Nashik']
    
    # Demographics
    age_groups = ['18-25', '26-35', '36-45', '46-55', '55+']
    genders = ['Male', 'Female']
    card_types = ['Gold', 'Silver', 'Platinum']
    
    # Create detailed transactional data
    detailed_data = []
    
    # Generate data for each month in our main dataset
    for _, row in card_spending_df.iterrows():
        date = row['Date']
        total_spending = row['Total_Spending_Billion_INR'] * 1000  # Convert to millions for distribution
        
        # Distribute spending across categories (based on typical patterns)
        category_splits = {
            'Grocery & Food': 0.25,
            'Shopping & Retail': 0.20,
            'Bills & Utilities': 0.15,
            'Entertainment': 0.12,
            'Travel': 0.10,
            'Fuel': 0.08,
            'Healthcare': 0.05,
            'Education': 0.03,
            'Others': 0.02
        }
        
        # City distribution (metros get more share)
        city_splits = {
            'Mumbai': 0.20,
            'Delhi NCR': 0.18,
            'Bangalore': 0.15,
            'Chennai': 0.10,
            'Hyderabad': 0.08,
            'Pune': 0.07,
            'Kolkata': 0.06,
            'Ahmedabad': 0.05,
            'Surat': 0.06,
            'Nashik': 0.05
        }
        
        for category in categories:
            for city in cities:
                for age_group in age_groups:
                    for gender in genders:
                        for card_type in card_types:
                            # Calculate spending for this combination
                            base_amount = total_spending * category_splits[category] * city_splits[city]
                            
                            # Age group adjustments
                            age_multiplier = {'18-25': 0.6, '26-35': 1.3, '36-45': 1.2, '46-55': 1.0, '55+': 0.8}
                            base_amount *= age_multiplier[age_group]
                            
                            # Gender adjustments (slight differences)
                            gender_multiplier = {'Male': 1.05, 'Female': 0.95}
                            base_amount *= gender_multiplier[gender]
                            
                            # Card type adjustments
                            card_multiplier = {'Platinum': 2.0, 'Gold': 1.2, 'Silver': 0.6}
                            base_amount *= card_multiplier[card_type]
                            
                            # Add some randomness
                            noise = np.random.normal(1, 0.1)
                            final_amount = max(0, base_amount * noise / 1000)  # Convert back to reasonable scale
                            
                            # Generate transaction count
                            avg_transaction_amount = np.random.normal(3500, 1000)  # Average ~3500 INR per transaction
                            transaction_count = max(1, int(final_amount * 1000 / avg_transaction_amount))
                            
                            if final_amount > 0.01:  # Only include meaningful amounts
                                detailed_data.append({
                                    'Date': date,
                                    'Year': date.year,
                                    'Month': date.month,
                                    'Category': category,
                                    'City': city,
                                    'Age_Group': age_group,
                                    'Gender': gender,
                                    'Card_Type': card_type,
                                    'Spending_Amount_Thousands_INR': round(final_amount, 2),
                                    'Transaction_Count': transaction_count,
                                    'Avg_Transaction_Amount_INR': round(final_amount * 1000 / transaction_count if transaction_count > 0 else 0, 2)
                                })
    
    return pd.DataFrame(detailed_data)

# Create the detailed dataset
detailed_df = create_detailed_spending_dataset()

print(f"Detailed Dataset Shape: {detailed_df.shape}")
print("\nSample data:")
print(detailed_df.head(10))

# Save detailed dataset
detailed_df.to_csv('detailed_card_spending.csv', index=False)

# Create summary statistics
summary_stats = {
    'Total_Records': len(detailed_df),
    'Date_Range': f"{detailed_df['Date'].min()} to {detailed_df['Date'].max()}",
    'Categories': detailed_df['Category'].nunique(),
    'Cities': detailed_df['City'].nunique(),
    'Age_Groups': detailed_df['Age_Group'].nunique(),
    'Card_Types': detailed_df['Card_Type'].nunique(),
    'Total_Spending_Millions_INR': detailed_df['Spending_Amount_Thousands_INR'].sum(),
    'Total_Transactions': detailed_df['Transaction_Count'].sum()
}

print("\nSummary Statistics:")
print("="*50)
for key, value in summary_stats.items():
    print(f"{key}: {value}")