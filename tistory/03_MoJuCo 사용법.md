MoJuCo를 사용하여 기본적인 제어에 대해 알아보기로 한다

## 1. MoJuCo 설치
```
# MuJoCO = 물리 시뮬레이터
pip install mujoco

# Gymnasium = 강화학습 환경 인터페이스 표준
pip install "gymnasium[mujoco]"
```

## 2. 초반 예제
```py
import gymnasium as gym

env = gym.make("InvertedPendulum-v5")

obs, info = env.reset()
print("obs:", obs)
print("obs shape:", obs.shape)
print("action space:", env.action_space)

for step in range(100):
    action = env.action_space.sample()
    obs, reward, terminated, truncated, info = env.step(action)

    print(step, reward, terminated, truncated)

    if terminated or truncated:
        obs, info = env.reset()

env.close()
```