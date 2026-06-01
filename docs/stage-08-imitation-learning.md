# 8단계: 모방학습

## 목적

scripted expert 또는 사람 demonstration 데이터를 사용해 로봇 정책을 학습하는 단계입니다. 처음에는 Behavior Cloning으로 시작하고, 이후 ACT와 Diffusion Policy로 확장합니다.

## 공부할 내용

### 1. Behavior Cloning

공부할 내용:

- supervised learning
- observation to action mapping
- MSE loss
- action normalization
- train/validation split

테스트:

- state-only BC 학습
- image + proprioception BC 학습
- validation loss 확인
- rollout success rate 측정

### 2. Sequence Modeling

공부할 내용:

- action chunk
- temporal context
- recurrent model
- Transformer
- compounding error

테스트:

- 단일 action 예측과 action chunk 예측 비교
- history length를 바꿔 성능 비교
- rollout 중 오차가 누적되는 case 관찰

### 3. ACT

공부할 내용:

- Action Chunking Transformer
- query token
- chunked action prediction
- temporal ensembling

테스트:

- 같은 dataset으로 BC와 ACT 비교
- chunk size 바꾸기
- temporal ensemble on/off 비교

### 4. Diffusion Policy

공부할 내용:

- denoising diffusion
- action trajectory generation
- noise schedule
- receding horizon control

테스트:

- action trajectory를 diffusion으로 예측
- inference step 수에 따른 속도/성능 비교
- BC/ACT/Diffusion Policy success rate 비교

## 실습 목표

```text
합성 demonstration dataset으로 최소 1개 task에서 BC baseline을 학습하고,
이후 ACT 또는 Diffusion Policy와 비교한다.
```

## 완료 체크리스트

- [ ] demonstration dataset을 학습 코드에서 읽을 수 있다.
- [ ] observation과 action normalization을 적용할 수 있다.
- [ ] BC baseline을 학습하고 rollout 평가할 수 있다.
- [ ] train loss와 실제 success rate가 다를 수 있음을 설명할 수 있다.
- [ ] ACT 또는 Diffusion Policy가 왜 필요한지 설명할 수 있다.

## 다음 단계와 연결

Visuomotor Transformer는 이미지와 robot state를 함께 보고 action을 출력하는 정책입니다. 모방학습 구조를 이해해야 Transformer 기반 정책을 안정적으로 설계할 수 있습니다.
