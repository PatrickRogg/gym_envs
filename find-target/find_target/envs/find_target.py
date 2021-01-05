import gym
import numpy as np
from gym import spaces

MAX_TIME = 1000

DIRECTIONS = ['LEFT', 'TOP', 'RIGHT', 'BOTTOM']


class FindTarget(gym.Env):
    metadata = {'render.modes': ['human']}

    def __init__(self):
        super(FindTarget, self).__init__()
        self.action_space = spaces.Discrete(4)
        self.observation_space = spaces.Box(low=0,
                                            high=4,
                                            shape=(6, 6),
                                            dtype=np.int32)
        self.world = self._create_world()
        self.time = 0

    def step(self, action:int):
        if not self.time % 2:
            current_player = 1
        else:
            current_player = 2

        self.time += 1
        reward = self._move(current_player, DIRECTIONS[action])
        done = reward != -1 or time > MAX_TIME
        obs = self.world

        return obs, reward, done, {}

    def reset(self):
        self.world = self._create_world()
        self.time = 0
        return self.world

    def render(self, mode='human', close=False):
        print(self.world)

    def _create_world(self):
        world = np.array([
            [1, 0, 0, 0, 0, 2],
            [0, 0, 0, 3, 3, 3],
            [0, 0, 3, 0, 0, 0],
            [3, 0, 0, 0, 0, 3],
            [0, 0, 0, 3, 0, 4],
            [0, 0, 0, 3, 3, 3],
        ])
        return world

    def _move(self, current_player, action):
        current_pos = np.where(self.world == current_player)

        if action == 'LEFT':
            next_pos = (current_pos[0], current_pos[1] - 1)
        elif action == 'TOP':
            next_pos = (current_pos[0] - 1, current_pos[1])
        elif action == 'RIGHT':
            next_pos = (current_pos[0], current_pos[1] + 1)
        else:
            next_pos = (current_pos[0] + 1, current_pos[1])

        reward = -1

        if self._valid_pos(next_pos):
            self.world[current_pos] = 0

            if self.world[next_pos] == 4:
                reward = 1000
            elif self.world[next_pos] == 3:
                reward = -1000

            self.world[next_pos] = current_player

        return reward

    def _valid_pos(self, pos):
        return 0 <= pos[0] < 6 and 0 <= pos[1] < 6 and self.world[pos] == 0
