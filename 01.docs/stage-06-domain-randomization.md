# 6단계: 도메인 랜덤화

## 목적

시뮬레이션에서 학습한 정책이 특정 scene에만 과적합되지 않도록 환경 조건을 다양하게 바꾸는 단계입니다. Sim-to-Real 전이의 핵심 준비 작업입니다.

## 공부할 내용

### 1. 시각 랜덤화

공부할 내용:

- texture randomization
- object color randomization
- lighting randomization
- camera pose randomization
- background randomization

테스트:

- 물체 색상을 매 episode마다 바꾸기
- 조명 위치와 밝기 바꾸기
- 카메라 위치에 작은 noise 추가
- 배경과 바닥 texture 바꾸기

### 2. 물리 랜덤화

공부할 내용:

- mass
- friction
- restitution
- damping
- center of mass

테스트:

- 물체 질량 범위 바꾸기
- 마찰 계수 범위 바꾸기
- 같은 grasp policy가 어느 범위까지 성공하는지 측정

### 3. 센서/Actuator 랜덤화

공부할 내용:

- camera noise
- depth noise
- latency
- action delay
- motor gain
- action clipping

테스트:

- RGB noise 추가
- depth noise 추가
- action delay 1~3 step 추가
- joint target에 작은 noise 추가

### 4. 랜덤화 범위 설계

공부할 내용:

- 너무 약한 randomization
- 너무 강한 randomization
- train/eval split
- robustness metric

테스트:

- randomization off 성공률 측정
- 약한 randomization 성공률 측정
- 강한 randomization 성공률 측정
- 실패 원인 분류

## 실습 목표

```text
같은 pick-and-place task를 100개 이상의 다른 scene 조건에서 실행하고 성공률을 기록한다.
```

## 완료 체크리스트

- [ ] 시각 랜덤화와 물리 랜덤화의 차이를 설명할 수 있다.
- [ ] randomization 범위를 config로 관리할 수 있다.
- [ ] random seed를 고정해 재현 가능한 실험을 만들 수 있다.
- [ ] randomization 강도에 따른 성공률을 비교할 수 있다.
- [ ] Sim-to-Real 관점에서 어떤 요소를 랜덤화해야 하는지 설명할 수 있다.

## 다음 단계와 연결

랜덤화된 scene에서 데이터를 생성해야 학습 데이터가 다양해집니다. 7단계 합성 데이터 생성은 이 랜덤화 설정 위에서 진행합니다.
