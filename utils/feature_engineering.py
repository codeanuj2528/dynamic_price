def engineer_features(df):
    # Extract time-based features
    df['hour'] = df['timestamp'].dt.hour
    df['day_of_week'] = df['timestamp'].dt.dayofweek
    df['is_weekend'] = df['day_of_week'].isin([5, 6]).astype(int)
    
    # Create demand indicator (already present in our synthetic data)
    # df['demand'] is already available
    
    # Calculate price per mile
    df['price_per_mile'] = df['final_price'] / df['distance']  # Changed 'price' to 'final_price'
    
    return df