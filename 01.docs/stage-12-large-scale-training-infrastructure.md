# 12단계: 대규모 학습 인프라

## 목적

단일 실험을 넘어서, 여러 task와 많은 데이터를 반복 가능하게 생성/학습/평가하는 파이프라인을 만드는 단계입니다. 개인 학습 단계보다는 연구팀 또는 프로젝트 운영 단계에 가깝습니다.

## 공부할 내용

### 1. 실험 관리

공부할 내용:

- config management
- random seed
- experiment name
- checkpoint
- metric logging
- artifact logging

테스트:

- config 파일로 실험 조건 관리
- seed별 결과 비교
- checkpoint 자동 저장
- train/eval metric 저장

### 2. 데이터 버전 관리

공부할 내용:

- dataset version
- metadata
- train/validation/test split
- data lineage
- failed episode mining

테스트:

- dataset manifest 생성
- episode별 success/failure label 저장
- 데이터 버전별 학습 결과 비교
- 실패 episode만 추출

### 3. 병렬 시뮬레이션과 Job 관리

공부할 내용:

- multi-GPU
- distributed rollout
- job scheduler
- batch data generation
- resource monitoring

테스트:

- 여러 random seed job 실행
- 여러 task dataset 동시 생성
- GPU memory와 step/sec 기록
- 실패한 job 재시도

### 4. 학습 파이프라인 자동화

공부할 내용:

- train script
- eval script
- report generation
- model registry
- reproducibility

테스트:

- dataset 생성 -> 학습 -> 평가를 하나의 pipeline으로 연결
- 결과 table 자동 생성
- best checkpoint 선택
- config와 metric을 함께 저장

## 실습 목표

```text
하나의 명령으로 dataset 생성, policy 학습, rollout 평가, 결과 저장까지 실행되는 작은 파이프라인을 만든다.
```

## 완료 체크리스트

- [ ] config로 실험 조건을 재현할 수 있다.
- [ ] dataset version과 model checkpoint를 연결해 기록할 수 있다.
- [ ] 여러 seed 실험을 자동 실행할 수 있다.
- [ ] 실패 episode를 찾아 재학습 데이터로 사용할 수 있다.
- [ ] 실험 결과를 표로 비교할 수 있다.

## 다음 단계와 연결

VLA/RFM 평가 벤치마크는 많은 task와 policy를 같은 기준으로 평가해야 하므로, 실험 관리와 데이터 관리가 없으면 결과를 신뢰하기 어렵습니다.
