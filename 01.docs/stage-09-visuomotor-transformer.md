# 9단계: Visuomotor Transformer 정책

## 목적

카메라 이미지와 로봇 상태를 입력으로 받아 action을 출력하는 visuomotor policy를 설계하는 단계입니다. 단일 task에서 시작해 multi-task, language-conditioned policy로 확장합니다.

## 공부할 내용

### 1. 입력 Observation 설계

공부할 내용:

- RGB image
- depth image
- proprioception
- end-effector pose
- previous action
- task id
- language instruction

테스트:

- image-only policy와 state-only policy 비교
- image + proprioception policy 구성
- 입력 normalization 적용

### 2. Image Encoder

공부할 내용:

- CNN encoder
- ResNet
- ViT
- feature map
- spatial token

테스트:

- 작은 CNN으로 image feature 추출
- pretrained encoder 사용
- encoder freeze와 fine-tuning 비교

### 3. Transformer Policy

공부할 내용:

- token
- positional encoding
- self-attention
- cross-attention
- action head

테스트:

- image token과 proprioception token 결합
- task token 추가
- action sequence 예측

### 4. Action 표현

공부할 내용:

- joint position target
- joint velocity
- end-effector delta pose
- gripper command
- action normalization

테스트:

- joint action과 end-effector action 비교
- gripper action 분리
- action scale을 잘못 잡았을 때 정책이 망가지는지 확인

## 실습 목표

```text
RGB 이미지와 robot proprioception을 입력으로 받아
end-effector delta action과 gripper command를 출력하는 정책을 만든다.
```

## 완료 체크리스트

- [ ] image encoder의 역할을 설명할 수 있다.
- [ ] proprioception을 image feature와 결합할 수 있다.
- [ ] action 표현 방식을 선택하고 이유를 설명할 수 있다.
- [ ] 단일 task policy를 학습하고 rollout 평가할 수 있다.
- [ ] unseen object pose 또는 lighting에서 성능을 측정할 수 있다.

## 다음 단계와 연결

강화학습 단계에서는 이 정책을 초기 policy로 사용하거나, imitation policy를 fine-tuning하는 방식으로 활용할 수 있습니다.
