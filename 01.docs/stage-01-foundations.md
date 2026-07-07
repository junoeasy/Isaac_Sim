# 1단계: 기초

## 목적

이 단계는 Isaac Sim을 다루기 전에 필요한 최소한의 수학, Python, 로봇 제어 배경을 만드는 단계입니다. 좌표계, 변환, 기구학, 간단한 제어 루프를 이해하고 Isaac Sim으로 넘어가면 이후 학습 속도가 훨씬 빨라집니다.

## 공부할 내용

### 1. Python과 개발 도구

공부할 내용:

- Python 함수, 클래스, type hint, 가상환경
- NumPy 배열과 행렬곱
- Matplotlib 시각화
- Git 기본 명령: clone, status, diff, commit
- Linux shell 기본 명령: `pwd`, `ls`, `cd`, `mkdir`, `python3`, `pip`

테스트:

- Python script 작성
- 터미널에서 실행
- 숫자 결과 출력
- 로봇팔 자세 plot 생성

### 2. 로보틱스를 위한 선형대수

공부할 내용:

- 벡터
- 행렬
- 내적
- 외적
- 역행렬
- 좌표축
- 동차좌표

아래 표현에 익숙해져야 합니다.

```text
p_world = T_world_robot @ p_robot
```

의미:

robot frame에서 표현된 점 `p_robot`을 world frame 기준의 점 `p_world`로 변환합니다. 이때 사용하는 변환행렬이 `T_world_robot`입니다.

테스트:

- 2D 점을 `[x, y, 1]`로 표현
- 2D 변환행렬 만들기
- 점을 다른 좌표계로 변환하기

### 3. 회전과 pose

공부할 내용:

- 2D 회전행렬
- 3D 회전행렬
- Euler angle
- quaternion
- translation
- pose
- SE(3)

중요한 개념:

```text
Pose = 위치 + 회전
Transform = 한 좌표계의 표현을 다른 좌표계 표현으로 바꾸는 행렬
```

테스트:

- 점을 90도 회전
- `[1, 2]`만큼 평행이동
- 두 transform 합성
- transform 역행렬 계산

### 4. 로봇 기구학

공부할 내용:

- joint
- link
- 순기구학
- 역기구학
- end-effector
- workspace
- singularity
- Jacobian

처음에는 2-link planar arm으로 시작합니다. 구조는 단순하지만, 큰 로봇팔에도 그대로 이어지는 핵심 개념을 담고 있습니다.

테스트:

- joint angle `q1`, `q2`가 주어졌을 때 end-effector 위치 계산
- target `(x, y)`가 주어졌을 때 근사 joint angle 계산
- 로봇팔 자세 plot 생성

### 5. 기본 제어

공부할 내용:

- control loop
- setpoint
- error
- proportional control
- PID control
- velocity limit
- acceleration limit
- trajectory interpolation

테스트:

- simulated point를 현재 위치에서 목표 위치로 이동
- 속도 제한 추가
- 시간에 따른 position error plot 생성

## 실습

첫 번째 실습 코드는 아래 파일에 있습니다.

- [stage01_transforms_and_kinematics.py](../exercises/stage01_transforms_and_kinematics.py)

실행:

```bash
python3 exercises/stage01_transforms_and_kinematics.py
```

예상 결과:

- 좌표 변환 테스트 결과 출력
- 2-link 로봇팔 순기구학 결과 출력
- 간단한 역기구학 target 풀이
- `outputs/stage01_2link_arm.png` 그림 저장

## 완료 체크리스트

- [ ] point와 vector의 차이를 설명할 수 있다.
- [ ] pose와 transform의 차이를 설명할 수 있다.
- [ ] robot frame의 점을 world frame으로 변환할 수 있다.
- [ ] transform을 합성하고 역변환할 수 있다.
- [ ] 2-link 로봇팔의 순기구학을 구현할 수 있다.
- [ ] 간단한 역기구학 문제를 풀 수 있다.
- [ ] 간단한 control loop를 설명할 수 있다.

## 이후 Isaac Sim과의 연결

Isaac Sim에서도 같은 개념을 사용합니다. 다만 계층이 많아질 뿐입니다.

- world frame: USD stage의 전체 좌표계
- robot base frame: 로봇 base prim 또는 articulation root
- end-effector frame: gripper 또는 tool transform
- camera frame: sensor transform
- object frame: cube, cup, door handle, target object의 pose

초보 단계에서 Isaac Sim 문제가 생기는 가장 흔한 원인은 frame 문제입니다. 물체가 이상한 위치에 나타나거나, 로봇팔이 엉뚱한 방향으로 움직이면 원인은 대개 잘못된 transform, 단위 scale, 회전 convention, parent frame입니다.
