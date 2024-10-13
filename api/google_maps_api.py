from datetime import datetime
import random

def get_traffic_data(start_location, end_location):
    """
    Advanced mock function to simulate getting traffic data from Google Maps API.
    This function creates a response structure similar to the real Google Maps API.
    """
    # Simulate distance (in km)
    distance = random.uniform(5, 50)
    
    # Simulate duration (in minutes)
    base_duration = distance * 2  # Assume 30 km/h average speed
    traffic_factor = random.uniform(1, 1.5)  # Random traffic factor
    duration = base_duration * traffic_factor
    
    # Simulate demand (placeholder)
    demand = random.randint(1, 20)
    
    # Simulate weather factor
    weather_factor = random.uniform(0.9, 1.1)
    
    # Create a mock response similar to Google Maps API
    mock_response = {
        "routes": [{
            "legs": [{
                "distance": {
                    "text": f"{distance:.1f} km",
                    "value": int(distance * 1000)  # Convert to meters
                },
                "duration": {
                    "text": f"{int(base_duration)} mins",
                    "value": int(base_duration * 60)  # Convert to seconds
                },
                "duration_in_traffic": {
                    "text": f"{int(duration)} mins",
                    "value": int(duration * 60)  # Convert to seconds
                },
                "end_address": end_location,
                "start_address": start_location,
            }]
        }]
    }
    
    # Extract relevant information from the mock response
    leg = mock_response['routes'][0]['legs'][0]
    
    return {
        "distance": leg['distance']['value'] / 1000,  # Convert meters to kilometers
        "duration": leg['duration']['value'] / 60,  # Convert seconds to minutes
        "traffic_duration": leg['duration_in_traffic']['value'] / 60,  # Convert seconds to minutes
        "current_time": datetime.now(),
        "demand": demand,
        "weather_factor": weather_factor
    }
