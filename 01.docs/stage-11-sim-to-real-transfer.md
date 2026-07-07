# 11단계: Sim-to-Real 전이

## 목적

시뮬레이션에서 만든 policy와 controller를 실제 로봇 또는 실제 시스템에 옮길 때 필요한 차이를 줄이는 단계입니다. 이 단계는 성능보다 안전과 검증 절차가 중요합니다.

## 공부할 내용

### 1. Calibration

공부할 내용:

- camera intrinsic
- camera extrinsic
- hand-eye calibration
- robot base alignment
- object frame alignment

테스트:

- checkerboard 또는 marker 기반 카메라 보정
- camera frame에서 본 물체 위치를 robot frame으로 변환
- sim camera pose와 real camera pose 비교

### 2. Actuator와 Sensor 차이

공부할 내용:

- motor delay
- joint limit
- velocity limit
- torque limit
- encoder noise
- camera latency

테스트:

- 실제 joint command 응답 시간 측정
- action delay를 sim에 반영
- velocity limit을 sim과 real에 동일하게 맞추기

### 3. ROS 2 연동

공부할 내용:

- topic
- service
- action
- TF tree
- joint_states
- image topic

테스트:

- Isaac Sim ROS 2 bridge 실행
- joint_states publish/subscribe
- camera image topic 확인
- TF tree 확인

### 4. Safety Layer

공부할 내용:

- workspace limit
- speed limit
- emergency stop
- collision check
- command filtering

테스트:

- action clipping 적용
- workspace 밖 명령 차단
- 속도 제한 적용
- low-speed rollout만 허용

## 실습 목표

```text
시뮬레이션 policy 또는 trajectory를 실제/가상 ROS 2 interface에 연결하고,
저속 안전 조건에서 replay할 수 있는 구조를 만든다.
```

## 완료 체크리스트

- [ ] sim과 real의 frame 차이를 설명할 수 있다.
- [ ] camera calibration이 왜 필요한지 설명할 수 있다.
- [ ] ROS 2 TF tree를 확인할 수 있다.
- [ ] action command에 safety filter를 적용할 수 있다.
- [ ] 실제 실행 전에 필요한 검증 절차를 문서화할 수 있다.

## 다음 단계와 연결

대규모 학습 인프라는 Sim-to-Real 실패 데이터를 다시 시뮬레이션으로 가져와 randomization과 dataset을 개선하는 루프까지 포함합니다.
