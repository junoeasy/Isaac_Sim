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
	#env.step에 해당 액션 넣고 값 불러오기
	
    print(step, reward, terminated, truncated)
	# 해당 값 출력
	# terminated : (규칙에 의한 종료)막대가 기준치 이상으로 기울어졌을 때 (현재는 |angle|<0.2)
	# truncated : (시간에 의한 종료) 외부 제약 조건으로 인한 종료(step에 의해 종료)
	
    if terminated or truncated:
        obs, info = env.reset()
        //초기화

env.close()
```

해당 파이썬 파일을 실행하면 값이 쭉 나온다.
![[Pasted image 20260602102740.png]]
처음에 초기 값과 설정 값들이 나오고
이후에 각 step별로 reward와 terminated,truncated 가 출력되고 있다.
5번 step을 보면 현재 reward가 0이고 terminated가 True인 것을 확인할 수 있다.
즉, 5번 step에서 |막대 기둥의 각도|>=0.2 가 됐다는 것을 알 수 있다.
좀 더 자세히 알고 싶으면 추가로 obs 값을 매 step출력하면 된다.

```

    # print(step, reward, terminated, truncated)
    
    print(step, reward, terminated, truncated, obs[0], obs[1], obs[2], obs[3])
```
다음과 같이 수정하고 실행하면 이렇게 나온다.
![[Pasted image 20260602103107.png|637]]
4번 step을 보면 obs[1] 의 값이 -0.2286... 이고 이 값의 절대값이 0.2보다 크기 때문에  terminated가 True가 되고 reward가 0이 된다.

reward를 같이 출력하면 
![[Pasted image 20260602103326.png]]
이런식으로 나온다.

## 3.예제 수정 및 개선 및 GUI표시

### GUI추가하기
처음에 있는 env를
```
env = gym.make("InvertedPendulum-v5", render_mode="human")
```
다음과 같이 수정해주면 이미지가 나오게 된다.
![[Mojuco6.gif]]
시뮬 속도가 빠르기 때문에 코드 안에 import time과 for문 안에 time.sleep(0.1)정도를 추가해준다.
![[Mojuco7.gif]]

### action 직접 제어
현재 action은 -3.0에서 3.0중에 random값인데 이것을 1.0으로 고정해보자.
action은 1차원 배열 1개이므로 action=[1.0] 으로 수정해준다.
![[Mojuco8.gif]]
다음과 같이 오른쪽 방향으로만 카트가 이동하는 것을 볼 수 있다.

### 수동 policy
Policy란 observation을 보고 action을 정하는 규칙이다.
기존 action은 random으로 지정하거나, 직접 제어했다. 
이번에는 policy를 직접 정해서 진행해보자
기존 observation 4개를 각각 cart_pos, pole_angle, cart_vel, pole_ang_vel 이런식으로 설정한다.
이후 PD 제어와 같이 cart_pos와 pole_angle에는 비례제어이득값, cart_vel과 pole_ang_vel에는 미분제어이득값을 곱해준다.
``` python
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
		print(step, reward, terminated,truncated,obs[0],obs[1],obs[2],obs[3])
	time.sleep(0.1)
	if terminated or truncated:
		obs, info = env.reset()
		break
```
이 정도 이득값을 배치하면 1000번 step까지는 

## 4. PPO
### PPO란
Proximal Policy Optimization으로 현재 policy를 조금씩만 안전하게 개선하는 강화학습 방법이다.
이전 학습에서는 수동  policy를 직접 만들어 이득값을 직접 설정했었는데, PPO는 사람이 설정하는 것이 아니라 신경망이 스스로 배우게 하는 방법

### PPO 구조
```
obs
-> neural network policy
-> action
-> MuJoCo step
-> reward
-> PPO가 policy 업데이트
```

### PPO가 학습하는 것
- policy network
	- obs를 보고 action을 정하는 모델
- value network
	- 혅