import numpy as np
from sklearn.preprocessing import KBinsDiscretizer

class QLearningPricing:
    def __init__(self, n_states, n_actions, learning_rate=0.1, discount_factor=0.95, epsilon=0.1):
        self.n_states = n_states
        self.n_actions = n_actions
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        self.epsilon = epsilon
        self.q_table = np.zeros((n_states, n_actions))
        
        # State discretization
        self.state_discretizer = KBinsDiscretizer(n_bins=n_states, encode='ordinal', strategy='uniform')
        
    def discretize_state(self, state):
        discretized = self.state_discretizer.fit_transform(np.array(state).reshape(1, -1))
        return int(discretized[0][0])
    
    def get_action(self, state):
        if np.random.random() < self.epsilon:
            return np.random.choice(self.n_actions)
        else:
            return np.argmax(self.q_table[state])
    
    def update(self, state, action, reward, next_state):
        current_q = self.q_table[state, action]
        next_max_q = np.max(self.q_table[next_state])
        new_q = current_q + self.learning_rate * (reward + self.discount_factor * next_max_q - current_q)
        self.q_table[state, action] = new_q