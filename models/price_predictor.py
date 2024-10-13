# models/price_predictor.py
from sklearn.ensemble import RandomForestRegressor

class PricePredictor:
    def __init__(self):
        self.model = RandomForestRegressor()
    
    def train(self, data):
        features = ['distance', 'hour', 'day_of_week', 'is_weekend', 'demand', 'weather_factor']
        X = data[features]
        y = data['final_price']
        self.model.fit(X, y)
    
    def predict(self, sample):
        features = [
            sample['distance'],
            sample['hour'],
            sample['day_of_week'],
            sample['is_weekend'],
            sample['demand'],
            sample['weather_factor']
        ]
        return self.model.predict([features])[0]