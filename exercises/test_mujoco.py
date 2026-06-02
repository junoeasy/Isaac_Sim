import gymnasium as gym
import time
import numpy as np
env = gym.make("InvertedPendulum-v5", render_mode="human")

obs, info = env.reset()
print("obs:", obs)
print("obs shape:", obs.shape)
print("action space:", env.action_space)

for step in range(10000):
    cart_pos, pole_angle, cart_vel, pole_ang_vel = obs
    action_value = (
        10.0 * pole_angle
        + 1.0 * pole_ang_vel
        + 0.5 * cart_pos
        + 0.2 * cart_vel
    )
    action_value = np.clip(action_value, -3.0, 3.0)

    action = np.array([action_value], dtype=np.float32)

    obs, reward, terminated, truncated, info = env.step(action)

    print(step, reward, terminated, truncated,obs[0],obs[1],obs[2],obs[3])
    time.sleep(0.1)
    if terminated or truncated:
        obs, info = env.reset()
        break

env.close()