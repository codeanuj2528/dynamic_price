import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

def generate_synthetic_ride_data(num_rides=10000, start_date='2023-01-01', end_date='2023-12-31'):
    # Generate random datetimes
    start = datetime.strptime(start_date, '%Y-%m-%d')
    end = datetime.strptime(end_date, '%Y-%m-%d')
    dates = [start + timedelta(seconds=random.randint(0, int((end - start).total_seconds())))
             for _ in range(num_rides)]

    # Generate other features
    distances = np.random.uniform(1, 30, num_rides)  # in km
    base_prices = distances * np.random.uniform(1.5, 2.5, num_rides)
    
    # Time-based factors
    time_factors = [1.0 + 0.5 * (date.hour >= 7 and date.hour <= 9) + 
                    0.3 * (date.hour >= 16 and date.hour <= 19) for date in dates]
    
    # Day-based factors
    day_factors = [1.0 + 0.2 * (date.weekday() >= 5) for date in dates]
    
    # Demand simulation (higher in mornings, evenings, and weekends)
    demands = [np.random.poisson(20 if 7 <= date.hour <= 9 or 16 <= date.hour <= 19 or date.weekday() >= 5 else 10) 
               for date in dates]
    
    # Weather factor (random for simplicity)
    weather_factors = np.random.uniform(0.9, 1.2, num_rides)
    
    # Calculate final prices
    prices = base_prices * np.array(time_factors) * np.array(day_factors) * weather_factors * (1 + np.array(demands) / 100)
    
    # Create DataFrame
    df = pd.DataFrame({
        'timestamp': dates,
        'distance': distances,
        'base_price': base_prices,
        'final_price': prices,
        'demand': demands,
        'weather_factor': weather_factors
    })
    
    # Add some random noise to prices
    df['final_price'] += np.random.normal(0, 1, num_rides)
    df['final_price'] = np.round(df['final_price'].clip(lower=0), 2)
    
    return df

# Generate the data
data = generate_synthetic_ride_data()

# Save to CSV
data.to_csv('data/synthetic_ride_data.csv', index=False)
print("Synthetic ride data has been generated and saved to 'data/synthetic_ride_data.csv'")

# Display first few rows and basic statistics
print(data.head())
print(data.describe())