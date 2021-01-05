from gym.envs.registration import register

register(
    id='find-target-v0',
    entry_point='find_target.envs:FindTarget',
)