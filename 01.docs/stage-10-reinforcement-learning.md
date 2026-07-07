# 10단계: 강화학습

## 목적

보상 기반으로 로봇 정책을 개선하는 단계입니다. 처음부터 복잡한 manipulation을 RL로 푸는 것보다 reach, align, lift 같은 작은 subtask부터 시작하고, 모방학습 policy를 fine-tuning하는 방향이 현실적입니다.

## 공부할 내용

### 1. RL 기본 구조

공부할 내용:

- state
- action
- reward
- policy
- value function
- episode
- return

테스트:

- reach task reward 설계
- reward curve 확인
- episode length와 success rate 기록

### 2. PPO

공부할 내용:

- on-policy learning
- advantage
- clipped objective
- entropy bonus
- rollout buffer

테스트:

- PPO로 reach task 학습
- learning rate 변경
- reward scale 변경
- entropy coefficient 변경

### 3. SAC

공부할 내용:

- off-policy learning
- replay buffer
- Q function
- entropy regularization
- sample efficiency

테스트:

- SAC로 간단한 continuous control task 학습
- replay buffer 크기 변경
- exploration 차이 확인

### 4. Manipulation Reward 설계

공부할 내용:

- dense reward
- sparse reward
- shaped reward
- success bonus
- collision penalty
- action penalty

테스트:

- reach reward
- grasp alignment reward
- lift reward
- place reward
- collision penalty 추가

## 실습 목표

```text
단순 reach task를 PPO로 학습하고,
이후 grasp alignment 또는 lift subtask로 확장한다.
```

## 완료 체크리스트

- [ ] PPO와 SAC의 차이를 설명할 수 있다.
- [ ] reward shaping이 왜 필요한지 설명할 수 있다.
- [ ] success rate와 reward curve를 함께 볼 수 있다.
- [ ] random seed별 성능 차이를 확인할 수 있다.
- [ ] imitation policy를 RL로 fine-tuning하는 구조를 설명할 수 있다.

## 다음 단계와 연결

Sim-to-Real 전이에서는 RL policy가 시뮬레이션의 물리 조건에 과적합될 수 있습니다. 그래서 domain randomization, actuator modeling, safety constraint가 반드시 함께 필요합니다.
