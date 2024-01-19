# Gym
import gym
import gym_anytrading

# Stable baselines - rl
from stable_baselines.common.vec_env import DummyVecEnv
from stable_baselines import A2C

# Processing libraries
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

df = pd.read_csv('historical_data/1day/SPY.csv')
df.head()

df['Date'] = pd.to_datetime(df['Date'])
df.dtypes

df.sort_values('Date', ascending=True, inplace=True)
df.head()

df.set_index('Date', inplace=True)
df.head()

env = gym.make('stocks-v0', df=df, frame_bound=(5,250), window_size=5)
env.signal_features

env.action_space

state = env.reset()
while True: 
    action = env.action_space.sample()
    n_state, reward, done, info = env.step(action)
    if done: 
        print("info", info)
        break
        
plt.figure(figsize=(15,6))
plt.cla()
env.render_all()
plt.show()

from gym_anytrading.envs import StocksEnv
from finta import TA

df['Volume'] = df['Volume'].apply(lambda x: float(x.replace(",", "")))
df.dtypes

df['SMA'] = TA.SMA(df, 12)
df['RSI'] = TA.RSI(df)
df['OBV'] = TA.OBV(df)
df.fillna(0, inplace=True)
df.head(15)

def add_signals(env):
    start = env.frame_bound[0] - env.window_size
    end = env.frame_bound[1]
    prices = env.df.loc[:, 'Low'].to_numpy()[start:end]
    signal_features = env.df.loc[:, ['Low', 'Volume','SMA', 'RSI', 'OBV']].to_numpy()[start:end]
    return prices, signal_features

class MyCustomEnv(StocksEnv):
    _process_data = add_signals
    
env2 = MyCustomEnv(df=df, window_size=12, frame_bound=(12,50))

env2.signal_features
df.head()

env_maker = lambda: env2
env = DummyVecEnv([env_maker])

model = A2C('MlpLstmPolicy', env, verbose=1) 
model.learn(total_timesteps=1000000)

env = MyCustomEnv(df=df, window_size=12, frame_bound=(80,250))
obs = env.reset()
while True: 
    obs = obs[np.newaxis, ...]
    action, _states = model.predict(obs)
    obs, rewards, done, info = env.step(action)
    if done:
        print("info", info)
        break

plt.figure(figsize=(15,6))
plt.cla()
env.render_all()
plt.show()