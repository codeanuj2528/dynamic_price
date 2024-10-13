import numpy as np
import pandas as pd
from geopy.distance import geodesic

# Simulated traffic conditions (can be replaced with real-time data from an API)
traffic_conditions = {
    'low': 1.0,   # Normal traffic multiplier
    'medium': 1.2,  # Medium traffic multiplier
    'high': 1.5   # Heavy traffic multiplier
}

class TaxiPricingSystem:
    def __init__(self, demand_data):
        self.data = demand_data

    def get_user_input(self):
        # Get start and destination input from the user
        start_point = input("Enter the pick-up location as latitude,longitude (e.g., 28.6139,77.2090): ")
        destination = input("Enter the destination location as latitude,longitude (e.g., 19.0760,72.8777): ")

        # Convert input to latitude, longitude pairs
        start_coords = tuple(map(float, start_point.split(',')))
        destination_coords = tuple(map(float, destination.split(',')))
        return start_coords, destination_coords

    def calculate_distance_and_time(self, start_coords, destination_coords):
        # Use the geodesic function to calculate the distance between points
        distance_km = geodesic(start_coords, destination_coords).km
        
        # Assume an average speed of 40 km/h, calculate travel time in minutes
        avg_speed_kmh = 40  # You can adjust this based on real data
        time_minutes = (distance_km / avg_speed_kmh) * 60
        return distance_km, time_minutes

    def get_traffic_condition(self):
        # Simulate getting traffic condition from the user (or from an API)
        traffic = input("Enter current traffic condition (low/medium/high): ").lower()
        return traffic_conditions.get(traffic, 1.0)  # Default to low traffic if input is invalid

    def calculate_dynamic_price(self, distance_km, traffic_multiplier, demand, supply):
        base_price_per_km = 10  # Assume base price is $10 per km
        base_price = distance_km * base_price_per_km
        
        # Surge pricing based on demand and supply ratio
        surge_multiplier = max(1.0, demand / supply)  # Ensure minimum multiplier of 1.0 (no surge)
        final_price = base_price * surge_multiplier * traffic_multiplier
        
        return final_price

    def run_pricing_model(self):
        # Get user input for start and destination locations
        start_coords, destination_coords = self.get_user_input()
        
        # Calculate the distance and estimated time
        distance_km, time_minutes = self.calculate_distance_and_time(start_coords, destination_coords)
        
        # Get the current traffic condition multiplier
        traffic_multiplier = self.get_traffic_condition()
        
        # Use mock data for demand and supply (could be from a real-time source)
        demand = np.random.randint(50, 500)  # Random demand between 50 and 500
        supply = np.random.randint(20, 200)  # Random supply between 20 and 200
        
        # Calculate the final dynamic price
        final_price = self.calculate_dynamic_price(distance_km, traffic_multiplier, demand, supply)
        
        # Display results
        print(f"\nEstimated trip distance: {distance_km:.2f} km")
        print(f"Estimated travel time: {time_minutes:.2f} minutes")
        print(f"Traffic condition: {traffic_multiplier:.1f}x multiplier")
        print(f"Final dynamic price: ${final_price:.2f}")

# Simulated demand data (could be real data in a deployed system)
mock_data = pd.DataFrame({
    'demand': np.random.randint(50, 500, size=100),
    'supply': np.random.randint(20, 200, size=100),
    'weather': np.random.choice([1, 2, 3], size=100)  # 1=Sunny, 2=Rainy, 3=Snowy
})

# Initialize the pricing system with mock data
pricing_system = TaxiPricingSystem(mock_data)

# Run the pricing model to simulate a user session
pricing_system.run_pricing_model()
