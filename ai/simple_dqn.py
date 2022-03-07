# RL Package
import torch
import torch.nn as nn
import torch.nn.functional as F
from tqdm import tqdm
import tensorflow as tf
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pandas import read_csv, set_option
import datetime
import math
from numpy.random import choice
import random
from collections import deque

data = pd.read_csv("BTC_1hr_train.csv")
data = data.drop(columns={"Open_time", 'Symbol'})

train_size = int(data.shape[0] * 0.8)

train_data = data.iloc[:train_size,3].values
val_data = data.iloc[train_size:,3].values


class DenseNet(nn.Module):
    def __init__(self, state_size, action_size = 3):
        super(DenseNet, self).__init__()
        self.state_size = state_size
        self.action_size = action_size
        self.dense1 = nn.Linear(self.state_size, 64)
        self.activation1 = nn.ReLU()
        self.dense2 = nn.Linear(64, 32)
        self.activation2 = nn.ReLU()
        self.dense3 = nn.Linear(32, 8)
        self.activation3 = nn.ReLU()
        self.out = nn.Linear(8, self.action_size)

    def forward(self, x):
        x = self.dense1(x)
        x = self.activation1(x)
        x = self.dense2(x)
        x = self.activation2(x)
        x = self.dense3(x)
        x = self.activation3(x)
        x = self.out(x)
        return x


class Agent:
    def __init__(self, state_size, is_eval=False, model_name=""):
        self.state_size = state_size # normalized previous days
        self.action_size = 3 # sit, buy, sell
        self.memory = deque(maxlen=1000)
        self.inventory = []
        self.model_name = model_name
        self.is_eval = is_eval
        self.gamma = 0.95
        self.epsilon = 1.0
        self.epsilon_min = 0.01
        self.epsilon_decay = 0.995
        self.model = load_model(model_name) if is_eval else self._model()
        self.criterion = nn.MSELoss()
        self.optimizer = torch.optim.Adam(self.model.parameters(), 1.0)

    def _model(self):
        model = DenseNet(self.state_size, self.action_size)
        return model

    def act(self, state):
        if not self.is_eval and random.random() <= self.epsilon:
            return random.randrange(self.action_size) # select according to epsilon-greedy
        # select according to Q function
        self.model.eval()
        with torch.no_grad():
            options = self.model(state)
        return torch.argmax(options[0])

    def expReplay(self, batch_size):
        mini_batch = []
        l = len(self.memory)
        for i in range(l - batch_size + 1, l):
            mini_batch.append(self.memory[i])
        for state, action, reward, next_state, done in mini_batch:
            self.model.eval()
            target = reward
            if not done:
                with torch.no_grad():
                    target = reward + self.gamma * torch.amax(self.model(next_state)[0])

            with torch.no_grad():
                target_f = self.model(state)
            target_f[0][action] = target
            # fit model
            self.model.train()
            optimizer.zero_grad()
            output = model(state)
            loss = criterion(output, target_f)
            loss.backward()
            self.model.eval()
            # self.model.fit(state, target_f, epochs=1, verbose=0)
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay


def formatPrice(n):
    return("-Rs." if n<0 else "Rs.")+"{0:.2f}".format(abs(n))

def sigmoid(x):
    if x < 0:
        return 1 - 1/(1 + math.exp(x))
    else:
        return 1/(1 + math.exp(-x))

def getState(data, t, n):
    d = t - n + 1
    if d >= 0:
        block = data[d:t+1]
    else:
        block = np.concatenate([-d*[data[0]], data[0:t+1]])
    res = []
    for i in range(n - 1):
        res.append(sigmoid(block[i + 1] - block[i]))
    return torch.tensor([res], dtype=torch.float32)


import sys
window_size = 10
agent = Agent(window_size)
l = train_data.shape[0] - 1
batch_size = 32
states_sell = []
states_buy = []
episode_count = 3

for e in range(episode_count + 1):
    print("Episode " + str(e) + "/" + str(episode_count))
    state = getState(train_data, 0, window_size + 1)
    total_profit = 0
    agent.inventory = []
    for t in tqdm(range(l), position=0, leave=True):
        action = agent.act(state)
        # sit
        next_state = getState(train_data, t + 1, window_size + 1)
        reward = 0
        if action == 1: # buy
            agent.inventory.append(train_data[t])
            # print("Buy: " + formatPrice(train_data[t]))
        elif action == 2 and len(agent.inventory) > 0: # sell
            bought_price = window_size_price = agent.inventory.pop(0)
            reward = max(train_data[t] - bought_price, 0)
            total_profit += train_data[t] - bought_price
            # print("Sell: " + formatPrice(train_data[t]) + " | Profit: " + formatPrice(train_data[t] - bought_price))
        done = True if t == l - 1 else False
        agent.memory.append((state, action, reward, next_state, done))
        state = next_state
        if done:
            print("--------------------------------")
            print("Total Profit: " + formatPrice(total_profit))
            print("--------------------------------")
        if len(agent.memory) > batch_size:
            agent.expReplay(batch_size)
    if e % 10 == 0:
        agent.model.save("RL_example.h5")
