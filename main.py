# main.py
import pandas as pd
import numpy as np
from utils.data_preprocessing import preprocess_data
from utils.feature_engineering import engineer_features
from models.price_predictor import PricePredictor
from models.q_learning import QLearningPricing
from api.google_maps_api import get_traffic_data

def calculate_reward(predicted_price, actual_price):
    # Simple reward function based on the difference between predicted and actual price
    return -abs(predicted_price - actual_price)

def main():
    # Load and preprocess data
    df = pd.read_csv("data/synthetic_ride_data.csv")
    preprocessed_data = preprocess_data(df)
    feature_data = engineer_features(preprocessed_data)
    
    # Initialize and train price predictor
    predictor = PricePredictor()
    predictor.train(feature_data)
    
    # Initialize Q-learning
    n_states = 100  # Number of discretized states
    n_actions = 20  # Number of possible price adjustments
    q_learning = QLearningPricing(n_states, n_actions)
    
    # Simulation loop
    n_episodes = 1000
    for episode in range(n_episodes):
        # Get a random sample from our feature_data for this episode
        sample = feature_data.sample(1).iloc[0]
        
        # Simulate getting traffic data
        traffic_data = get_traffic_data(None, None)  # We're not using specific locations
        
        # Create state representation
        state = [
            sample['distance'],  # Use the distance from our sample instead of traffic data
            traffic_data['traffic_duration'],
            traffic_data['demand'],
            traffic_data['weather_factor'],
            traffic_data['current_time'].hour,
            traffic_data['current_time'].weekday()
        ]
        
        # Discretize state
        discretized_state = q_learning.discretize_state(state)
        
        # Get action (price adjustment)
        action = q_learning.get_action(discretized_state)
        
        # Get base price prediction
        base_price = predictor.predict(sample)  # Pass the entire sample
        
        # Apply price adjustment
        price_adjustment = (action - n_actions/2) / (n_actions/2) * 10  # Scale to -10 to +10
        final_price = base_price + price_adjustment
        
        # In a real scenario, we would wait for the actual outcome.
        # Here, we'll use the original price from our dataset as the "actual" price.
        actual_price = sample['final_price']
        
        # Calculate reward
        reward = calculate_reward(final_price, actual_price)
        
        # Update Q-table
        next_state = discretized_state  # In a real scenario, this would be the next state
        q_learning.update(discretized_state, action, reward, next_state)
        
        if episode % 100 == 0:
            print(f"Episode {episode}, Price: ${final_price:.2f}, Actual: ${actual_price:.2f}, Reward: {reward:.2f}")
    
    # Final test
    sample = feature_data.sample(1).iloc[0]
    traffic_data = get_traffic_data(None, None)
    print("Traffic Data:", traffic_data)
    
    base_price = predictor.predict(sample)
    
    state = [
        sample['distance'],
        traffic_data['traffic_duration'],
        traffic_data['demand'],
        traffic_data['weather_factor'],
        traffic_data['current_time'].hour,
        traffic_data['current_time'].weekday()
    ]
    discretized_state = q_learning.discretize_state(state)
    action = q_learning.get_action(discretized_state)
    price_adjustment = (action - n_actions/2) / (n_actions/2) * 10
    final_price = base_price + price_adjustment
    
    print(f"Base price: ${base_price:.2f}")
    print(f"Q-learning adjusted price: ${final_price:.2f}")

if __name__ == "__main__":
    main()