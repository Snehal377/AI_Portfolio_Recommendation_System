import gym
import numpy as np
import pandas as pd
from stable_baselines3 import PPO

class PortfolioEnv(gym.Env):

    def __init__(self, returns):

        super(PortfolioEnv, self).__init__()

        self.returns = returns.values
        self.n_assets = returns.shape[1]
        self.current_step = 0

        self.action_space = gym.spaces.Box(
            low=0,
            high=1,
            shape=(self.n_assets,),
            dtype=np.float32
        )

        self.observation_space = gym.spaces.Box(
            low=-np.inf,
            high=np.inf,
            shape=(self.n_assets,),
            dtype=np.float32
        )

    def reset(self):

        self.current_step = 0
        
        return np.nan_to_num(self.returns[self.current_step])

    def step(self, action):

        weights = action / (np.sum(action) + 1e-8)

        portfolio_return = np.dot(weights, self.returns[self.current_step])

        reward = portfolio_return

        self.current_step += 1

        done = self.current_step >= len(self.returns) - 1

        next_state = np.nan_to_num(self.returns[self.current_step])

        return next_state, reward, done, {}


# -------- RL TRAINING FUNCTION --------

def train_rl_agent(returns):

    env = PortfolioEnv(returns)

    model = PPO("MlpPolicy", env, verbose=0)

    model.learn(total_timesteps=10000)

    return model


# -------- GET PORTFOLIO WEIGHTS --------

def get_rl_portfolio_weights(model, returns):

    env = PortfolioEnv(returns)

    obs = env.reset()

    action, _ = model.predict(obs)

    weights = action / np.sum(action)

    return weights