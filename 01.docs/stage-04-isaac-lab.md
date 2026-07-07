# 4단계: Isaac Lab

## 목적

Isaac Lab을 사용해 로봇 학습용 환경을 구성하는 단계입니다. Isaac Sim이 시뮬레이터라면, Isaac Lab은 observation, action, reward, reset, randomization을 학습용 구조로 묶는 프레임워크입니다.

## 공부할 내용

### 1. Isaac Lab 환경 구조

공부할 내용:

- direct workflow
- manager-based workflow
- scene config
- robot config
- environment config
- simulation config

테스트:

- Isaac Lab 예제 task 실행
- task config 파일 위치 찾기
- 환경 개수 num_envs 바꾸기
- simulation timestep 바꾸기

### 2. Manager 구조

공부할 내용:

- observation manager
- action manager
- reward manager
- termination manager
- event manager
- curriculum manager

테스트:

- observation term 하나 추가
- reward term weight 바꾸기
- termination 조건 추가
- reset randomization 추가

### 3. Vectorized Simulation

공부할 내용:

- 병렬 환경
- environment spacing
- GPU simulation
- batch tensor observation

테스트:

- 16개 환경 실행
- 256개 환경 실행
- 1024개 환경 실행
- GPU 사용량과 step 속도 확인

### 4. 학습 연동

공부할 내용:

- PPO 학습 스크립트
- checkpoint
- policy export
- rollout evaluation

테스트:

- 기본 PPO 학습 실행
- 학습된 checkpoint로 play 실행
- reward curve 확인
- success rate 측정

## 실습 목표

이 단계의 최소 결과물은 아래입니다.

```text
Isaac Lab 예제 task를 하나 선택해 observation, reward, reset randomization을 직접 수정한다.
```

## 완료 체크리스트

- [ ] Isaac Lab task config 구조를 찾을 수 있다.
- [ ] observation/action/reward/termination의 위치를 설명할 수 있다.
- [ ] num_envs를 바꿔 병렬 환경을 실행할 수 있다.
- [ ] PPO 학습과 checkpoint play를 실행할 수 있다.
- [ ] reward를 수정했을 때 행동이 어떻게 바뀌는지 설명할 수 있다.

## 다음 단계와 연결

이후 모바일 매니퓰레이터 task를 만들 때 Isaac Lab의 manager 구조를 사용하면 randomization, reward, evaluation을 체계적으로 관리할 수 있습니다.
