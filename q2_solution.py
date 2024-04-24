import numpy as np
from stable_baselines3 import DDPG
from stable_baselines3.common.env_util import make_vec_env

from gym import Env
from gym.spaces import Box

class NOCEnvironment(Env):
    def __init__(self):
        super(NOCEnvironment, self).__init__()
        self.action_space = Box(low=-1, high=1, shape=(4,), dtype=np.float32)
        self.observation_space = Box(low=0, high=1, shape=(4,), dtype=np.float32)
        self.buffer_occupancy = 0.5
        self.arbitration_rate_cpu = 0.6
        self.arbitration_rate_io = 0.4
        self.power_consumption = 0.7

    def step(self, action):
        self.buffer_occupancy += action[0]
        self.arbitration_rate_cpu += action[1]
        self.arbitration_rate_io += action[2]
        self.power_consumption += action[3]

        reward = self.calculate_reward()

        new_state = [self.buffer_occupancy, self.arbitration_rate_cpu, self.arbitration_rate_io, self.power_consumption]

        return np.array(new_state), reward, False, {}

    def reset(self):
        self.buffer_occupancy = 0.5
        self.arbitration_rate_cpu = 0.6
        self.arbitration_rate_io = 0.4
        self.power_consumption = 0.7
        return np.array([self.buffer_occupancy, self.arbitration_rate_cpu, self.arbitration_rate_io, self.power_consumption])

    def seed(self, seed=None):
        pass

    def calculate_reward(self):
        reward = 0.5 * (1 - self.buffer_occupancy) + 0.3 * (self.arbitration_rate_cpu + self.arbitration_rate_io) + 0.2 * (1 - self.power_consumption)
        return reward

env = make_vec_env(lambda: NOCEnvironment(), n_envs=1)

model = DDPG("MlpPolicy", env, verbose=1)
model.learn(total_timesteps=10000)

model.save("ddpg_noc_model")
