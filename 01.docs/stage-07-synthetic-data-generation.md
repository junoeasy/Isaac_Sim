# 7단계: 합성 데이터 생성

## 목적

시뮬레이션에서 이미지, depth, segmentation, pose, robot state, action trajectory를 자동으로 저장해 학습 데이터셋을 만드는 단계입니다.

## 공부할 내용

### 1. 데이터 종류

공부할 내용:

- RGB image
- depth image
- semantic segmentation
- instance segmentation
- object pose
- camera pose
- joint position/velocity
- end-effector pose
- action

테스트:

- RGB와 depth 저장
- segmentation mask 저장
- object pose와 camera pose 저장
- robot proprioception 저장

### 2. Dataset Schema

공부할 내용:

- episode
- timestep
- observation
- action
- reward
- done
- language instruction
- task id

예시 구조:

```text
episode_0001/
  obs/rgb
  obs/depth
  obs/joint_pos
  obs/ee_pose
  action
  metadata
```

테스트:

- episode 단위로 파일 저장
- timestep 순서 검증
- image와 action 개수 일치 확인
- metadata에 randomization seed 저장

### 3. 저장 형식

공부할 내용:

- HDF5
- Zarr
- WebDataset
- NPZ
- Parquet metadata

테스트:

- 작은 dataset을 NPZ로 저장
- HDF5 또는 Zarr로 episode 저장
- 저장한 데이터를 다시 load해서 shape 확인

### 4. 데이터 품질 검증

공부할 내용:

- frame alignment
- missing frame
- corrupted image
- action/observation timestamp mismatch
- success label

테스트:

- episode별 길이 확인
- 이미지 샘플 grid 생성
- 성공 episode와 실패 episode 분리
- 데이터 통계 출력

## 실습 목표

```text
scripted expert가 수행한 pick-and-place episode를 100개 이상 저장하고,
나중에 모방학습에 바로 쓸 수 있는 dataset schema를 만든다.
```

## 완료 체크리스트

- [ ] observation과 action을 timestep별로 저장할 수 있다.
- [ ] episode metadata를 남길 수 있다.
- [ ] 저장한 dataset을 다시 불러와 검증할 수 있다.
- [ ] 성공/실패 episode를 구분할 수 있다.
- [ ] 학습 코드가 읽기 쉬운 구조로 dataset을 설계할 수 있다.

## 다음 단계와 연결

모방학습은 demonstration 데이터 품질에 크게 의존합니다. 데이터 저장 구조가 불안정하면 BC, ACT, Diffusion Policy 모두 학습이 흔들립니다.
