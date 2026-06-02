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

# env에 gymnasium 새로 만들기 만든 버전은 InvertedPendulum 
# 해당문서 https://gymnasium.farama.org/v1.1.1/environments/mujoco/inverted_pendulum/
env = gym.make("InvertedPendulum-v5")


# obs = observation 관찰 값
# info = obs값 외 추가 정보
obs, info = env.reset()

print("obs:", obs)
# obs: [-0.0068138  -0.00394543 -0.0099438  -0.00846145]
# obs[0] = 카트 위치(m)
# obs[1] = 카트 위에 있는 막대의 각도(rad)
# obs[2] = 카트의 선속도(m/s)
# obs[3] = 막대의 각속도(rad/s)

print("obs shape:", obs.shape)
# obs shape: (4,) 
# 4, 인 이유 : 1차원 배열이라는 표현(numpy에서)
# 1차원 배열에 4개의 값이 있다.

print("action space:", env.action_space)
# action space: Box(-3.0, 3.0, (1,), float32)
# action은 -3에서 3사이의 값이고 float32의 형식이다. 값은 1차원 배열 1개만 들어갈 수있다.

#100번 반복하면서
for step in range(100):
    action = env.action_space.sample()
    # action값을 범위 내에서 random으로 하기
    
    obs, reward, terminated, truncated, info = env.step(action)
	env.step에 해당 액션 넣고 값 불러오기
	
    print(step, reward, terminated, truncated)
	# 해당 값 출력
    if terminated or truncated:
        obs, info = env.reset()

env.close()
```