# 2단계: MuJoCo 제어 기초

## 목적

Isaac Sim으로 바로 들어가기 전에 시뮬레이터의 기본 루프와 로봇 제어 구조를 가볍게 익히는 단계입니다. MuJoCo는 Isaac Sim보다 빠르고 단순해서 observation, action, reward, done 구조를 이해하기 좋습니다.

## 공부할 내용

### 1. 시뮬레이터 루프

공부할 내용:

- reset
- step
- observation
- action
- reward
- done 또는 terminated/truncated
- simulation timestep
- control frequency

핵심 개념:

```text
초기화 -> 관측 -> 행동 입력 -> 시뮬레이션 한 스텝 진행 -> 보상/종료 확인
```

테스트:

- MuJoCo 예제 환경 하나 실행
- 매 step마다 observation shape 출력
- action을 0으로 넣었을 때 로봇이 어떻게 되는지 확인
- random action을 넣었을 때 상태가 어떻게 바뀌는지 확인

### 2. 로봇 모델 구조

공부할 내용:

- MJCF/XML
- body
- joint
- geom
- actuator
- sensor
- site

테스트:

- XML에서 link 길이 바꾸기
- joint limit 바꾸기
- actuator strength 바꾸기
- site 위치를 바꾸고 end-effector 위치 확인

### 3. 제어 방식

공부할 내용:

- position control
- velocity control
- torque control
- joint limit
- actuator saturation

테스트:

- 같은 목표 위치를 position control과 velocity control로 보내보기
- 너무 큰 action을 넣었을 때 clipping되는지 확인
- joint limit 근처에서 로봇이 어떻게 움직이는지 확인

### 4. 강화학습 환경 구조

공부할 내용:

- Gymnasium environment
- observation space
- action space
- reward function
- success metric

테스트:

- reach task의 observation/action/reward를 직접 출력
- reward를 바꿔보고 학습 난이도가 어떻게 바뀌는지 비교

## 실습 목표

이 단계의 최소 결과물은 아래입니다.

```text
2-link 또는 간단한 arm reach 환경에서
목표점까지 end-effector를 이동시키는 제어 루프를 이해한다.
```

## 완료 체크리스트

- [ ] reset과 step의 역할을 설명할 수 있다.
- [ ] observation, action, reward가 무엇인지 설명할 수 있다.
- [ ] MuJoCo XML에서 joint, body, actuator를 찾을 수 있다.
- [ ] position control과 velocity control의 차이를 설명할 수 있다.
- [ ] 간단한 reach task의 success metric을 정의할 수 있다.

## 다음 단계와 연결

Isaac Sim에서도 기본 구조는 같습니다. 차이는 Isaac Sim이 USD, PhysX, sensor, renderer, articulation 같은 계층을 더 많이 가진다는 점입니다. MuJoCo에서 제어 루프를 먼저 이해하면 Isaac Sim의 복잡한 인터페이스를 볼 때 핵심을 놓치지 않습니다.
