import pandas as pd

def preprocess_data(df):
    # Convert timestamp to datetime
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    
    # Remove outliers
    df = remove_outliers(df)
    
    # Handle missing values
    df = handle_missing_values(df)
    
    return df

def remove_outliers(df):
    # Remove rides with unreasonable prices or distances
    df = df[(df['final_price'] > 0) & (df['final_price'] < 1000)] 
    df = df[(df['distance'] > 0) & (df['distance'] < 100)]
    return df

def handle_missing_values(df):
    # Fill missing values or drop rows with missing data
    return df.dropna()