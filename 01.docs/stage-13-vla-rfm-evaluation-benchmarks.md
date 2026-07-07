# 13단계: VLA/RFM 평가 벤치마크

## 목적

Vision-Language-Action 또는 Robot Foundation Model 스타일 정책을 시뮬레이션에서 공정하게 평가하는 벤치마크를 만드는 단계입니다. 단일 task 성공률이 아니라 다양한 instruction, object, scene, embodiment에서의 일반화 능력을 봅니다.

## 공부할 내용

### 1. Task Suite 설계

공부할 내용:

- pick
- place
- push
- open
- close
- navigate
- long-horizon task

테스트:

- 3개 이상의 기본 task 정의
- 각 task의 success condition 작성
- easy/medium/hard 난이도 분리

### 2. Instruction 설계

공부할 내용:

- language instruction
- task template
- object attribute
- spatial relation
- ambiguity

테스트:

- 같은 task에 여러 instruction 작성
- 색상/형상/위치 조건 포함
- 애매한 instruction을 제거하거나 별도 분류

### 3. 평가 Split

공부할 내용:

- seen object
- unseen object
- seen scene
- unseen scene
- seen task
- unseen task
- multi-embodiment

테스트:

- train/eval object 분리
- train/eval scene 분리
- task별 난이도 균형 맞추기

### 4. Metric

공부할 내용:

- success rate
- completion time
- collision rate
- path efficiency
- recovery rate
- instruction following accuracy

테스트:

- task별 success rate 계산
- 실패 원인 자동 태깅
- policy별 결과 table 생성
- 동일 seed에서 여러 policy 비교

## 실습 목표

```text
pick, place, push 같은 작은 task suite를 만들고,
두 개 이상의 policy를 같은 조건에서 평가하는 benchmark report를 만든다.
```

## 완료 체크리스트

- [ ] task별 success condition을 명확히 정의할 수 있다.
- [ ] instruction template을 설계할 수 있다.
- [ ] seen/unseen split을 만들 수 있다.
- [ ] 여러 policy를 같은 조건에서 평가할 수 있다.
- [ ] success rate 외의 failure metric도 기록할 수 있다.

## 최종 연결

이 단계까지 오면 처음 이미지에 있던 업무 대부분을 하나의 연구 파이프라인으로 연결할 수 있습니다.

```text
시뮬레이션 환경 구축
-> 도메인 랜덤화
-> 합성 데이터 생성
-> 모방학습/RL 학습
-> Sim-to-Real 준비
-> 대규모 실험 관리
-> VLA/RFM 평가
```
