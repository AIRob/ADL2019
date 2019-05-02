import numpy as np
np.random.seed(9487)
import torch
torch.cuda.manual_seed_all(9487)
import torch.nn as nn
import torch.nn.functional as F
from torch.autograd import Variable

from agent_dir.agent import Agent
from environment import Environment

class PolicyNet(nn.Module):
    def __init__(self, state_dim, action_num, hidden_dim):
        super(PolicyNet, self).__init__()
        self.fc1 = nn.Linear(state_dim, hidden_dim)
        self.fc2 = nn.Linear(hidden_dim, action_num)

    def forward(self, x):
        x = F.relu(self.fc1(x))
        x = self.fc2(x)
        action_prob = F.softmax(x, dim=-1)
        return action_prob

class AgentPG(Agent):
    def __init__(self, env, args):
        self.env = env
        self.model = PolicyNet(state_dim = self.env.observation_space.shape[0],
                               action_num= self.env.action_space.n,
                               hidden_dim=64)
        self.model_name = 'pg'
        if args.test_pg:
            self.load('./checkpoints/' + self.model_name + '.cpt')

        # discounted reward
        self.gamma = 0.99 
        
        # training hyperparameters
        self.num_episodes = 100000 # total training episodes (actually too large...)
        self.display_freq = 10 # frequency to display training progress
        
        # optimizer
        self.optimizer = torch.optim.Adam(self.model.parameters(), lr=3e-3)
        
        # saved rewards and actions
        self.rewards, self.saved_actions = [], []
        self.saved_log_probs = []
    
    def save(self, save_path):
        print('save model to', save_path)
        torch.save(self.model.state_dict(), save_path)
    
    def load(self, load_path):
        print('load model from', load_path)
        self.model.load_state_dict(torch.load(load_path))

    def init_game_setting(self):
        self.rewards, self.saved_actions = [], []
        self.saved_log_probs = []

    def make_action(self, state, test=False):
        # Use your model to output distribution over actions and sample from it.
        # HINT: google torch.distributions.Categorical
        state = torch.from_numpy(state).float().unsqueeze(0)
        action_prob = self.model(state)
        m = torch.distributions.Categorical(action_prob)
        action = m.sample()
        self.saved_log_probs.append(m.log_prob(action))
        return action.item()

    def update(self):
        # discount your saved reward
        R = 0
        policy_loss = []
        rewards = []
        # Discount future rewards back to the present using gamma
        for r in self.rewards[::-1]:
            R = r + self.gamma * R
            rewards.insert(0, R)
        
        # turn rewards to pytorch tensor and standardize
        rewards = torch.Tensor(rewards)
        rewards = (rewards - rewards.mean()) / (rewards.std() + np.finfo(np.float32).eps)
        
        # compute loss
        for log_prob, reward in zip(self.saved_log_probs, rewards):
            policy_loss.append(-log_prob * reward)
        
        # Update network weights
        self.optimizer.zero_grad()
        policy_loss = torch.cat(policy_loss).sum()
        policy_loss.backward()
        self.optimizer.step()

    def train(self):
        avg_reward = None # moving average of reward
        episode_rewards = []
        for epoch in range(self.num_episodes):
            state = self.env.reset()
            self.init_game_setting()
            episode_reward = 0
            done = False
            while(not done):
                action = self.make_action(state)
                state, reward, done, _ = self.env.step(action)
                
                self.saved_actions.append(action)
                self.rewards.append(reward)
                episode_reward += reward

            # for logging 
            last_reward = np.sum(self.rewards)
            avg_reward = last_reward if not avg_reward else avg_reward * 0.9 + last_reward * 0.1
            episode_rewards.append(episode_reward)
            
            # update model
            self.update()

            if epoch % self.display_freq == 0:
                print('Epochs: %d/%d | Avg reward: %f '%
                       (epoch, self.num_episodes, avg_reward))
                np.save('./results/' + self.model_name + '_episode_rewards.npy', np.array(episode_rewards))
            
            if avg_reward > 50: # to pass baseline, avg. reward > 50 is enough.
                print('Epochs: %d/%d | Avg reward: %f '%
                       (epoch, self.num_episodes, avg_reward))
                self.save('./checkpoints/' + self.model_name + '.cpt')
                break