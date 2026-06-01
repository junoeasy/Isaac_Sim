# Isaac Sim / 로봇 학습 로드맵

## 최종 목표

최종적으로는 아래 업무를 직접 수행할 수 있는 수준을 목표로 합니다.

- Isaac Sim / MuJoCo 기반 모바일 매니퓰레이터 시뮬레이션 환경 구축
- 시뮬레이션 환경의 도메인 랜덤화
- 모방학습용 합성 데이터 자동 생성
- BC, ACT, Diffusion Policy 기반 모방학습
- Visuomotor Transformer 기반 제어 정책 학습
- PPO, SAC 기반 강화학습
- Sim-to-Real 전이 파이프라인 설계
- 다중 task, 다중 embodiment용 대규모 합성 데이터 생성
- VLA/RFM 정책의 시뮬레이션 기반 평가 벤치마크 구축

이 로드맵은 각 단계마다 “이론 공부 → 작은 테스트 → 다음 단계로 넘어가기 위한 기준”을 갖도록 구성했습니다.

## 1단계: 기초

공부할 내용:

- Linux shell, Git, Python 프로젝트 구조
- NumPy, PyTorch, Matplotlib
- 좌표계, 벡터, 회전행렬, 동차변환
- quaternion, SE(3)
- 로봇 기구학: 순기구학, 역기구학, Jacobian
- 기본 제어: PID, trajectory 보간, 속도 제한

테스트:

- Python으로 2D/3D 좌표 변환 구현
- 2-link 로봇팔 순기구학 구현
- 2-link 로봇팔 역기구학 구현
- 작은 PyTorch 모델 학습 및 저장/불러오기

다음 단계로 넘어가는 기준:

- world frame, robot base frame, camera frame, end-effector frame을 설명할 수 있다.
- 한 좌표계의 점을 다른 좌표계로 변환할 수 있다.
- 시뮬레이터 없이 작은 로봇 기구학 계산을 직접 구현할 수 있다.

상세 문서: [1단계: 기초](stage-01-foundations.md)

## 2단계: MuJoCo 제어 기초

공부할 내용:

- 시뮬레이터 루프: reset, step, observation, action, reward, done
- MJCF/XML 로봇 모델 구조
- 접촉, 마찰, joint limit, actuator control
- Gymnasium 스타일 환경 인터페이스

테스트:

- 간단한 MuJoCo reach task 실행
- 직접 reach 환경 만들기
- position control과 velocity control 비교
- 작은 task에서 PPO 또는 SAC baseline 학습

다음 단계로 넘어가는 기준:

- Isaac Sim 없이도 로봇 제어 루프를 이해한다.
- observation, action, reward, success metric을 직접 정의할 수 있다.

## 3단계: Isaac Sim 기초

공부할 내용:

- USD stage, prim, xform, articulation
- PhysX 시뮬레이션 설정
- 재질, 조명, 카메라, depth, segmentation
- Isaac Sim Python scripting
- asset 로딩과 scene 구성

테스트:

- 기본 로봇 asset 로드
- 테이블, 물체, 카메라, 조명 추가
- Python으로 로봇 joint 제어
- RGB, depth, segmentation 결과 저장

다음 단계로 넘어가는 기준:

- 간단한 manipulation scene을 코드로 만들 수 있다.
- 시뮬레이터에서 기본 sensor 데이터를 수집할 수 있다.

## 4단계: Isaac Lab

공부할 내용:

- Isaac Lab 환경 구조
- manager-based environment
- observation, action, reward, termination, randomization manager
- vectorized simulation
- RL 라이브러리 연동

테스트:

- Isaac Lab 예제 실행
- reward term 수정
- observation term 추가
- 수백~수천 개 환경 병렬 실행

다음 단계로 넘어가는 기준:

- Isaac Lab task를 수정하고 정책을 학습시킬 수 있다.

## 5단계: 모바일 매니퓰레이터 환경 구축

공부할 내용:

- 모바일 베이스와 로봇팔의 기구학
- base navigation과 arm manipulation의 결합
- gripper 모델링
- task state machine
- scripted expert policy

테스트:

- mobile base + arm scene 구성
- base를 pre-grasp pose로 이동
- scripted controller로 pick-and-place 수행
- 성공/실패 case 로그 저장

다음 단계로 넘어가는 기준:

- 시뮬레이션에서 end-to-end scripted mobile manipulation task 하나를 완성한다.

## 6단계: 도메인 랜덤화

공부할 내용:

- 시각 랜덤화: texture, 색상, 조명, 카메라 위치
- 물리 랜덤화: 질량, 마찰, 반발계수, damping
- 센서 랜덤화: noise, latency, dropped frame
- actuator 랜덤화: delay, gain, saturation

테스트:

- 수백 개 randomized scene 생성
- 랜덤화 환경에서 task 성공률 측정
- task를 망가뜨리는 랜덤화 범위 확인

다음 단계로 넘어가는 기준:

- 시각/물리 랜덤화가 들어가도 task가 완전히 무너지지 않는다.

## 7단계: 합성 데이터 생성

공부할 내용:

- Isaac Sim Replicator
- dataset schema 설계
- RGB, depth, segmentation, pose, proprioception, action logging
- HDF5, Zarr, WebDataset 같은 저장 형식

테스트:

- perception dataset 생성
- imitation learning trajectory dataset 생성
- 데이터 shape, timestamp, frame alignment 검증

다음 단계로 넘어가는 기준:

- 시뮬레이션에서 재사용 가능한 학습 데이터를 자동 생성할 수 있다.

## 8단계: 모방학습

공부할 내용:

- Behavior Cloning
- 로봇 action sequence modeling
- ACT
- Diffusion Policy
- rollout evaluation

테스트:

- scripted expert 데이터로 BC 학습
- chunked action으로 ACT 학습
- action trajectory로 Diffusion Policy 학습
- 시뮬레이션 success rate 비교

다음 단계로 넘어가는 기준:

- demonstration 데이터에서 정책을 학습하고 시뮬레이션에서 평가할 수 있다.

## 9단계: Visuomotor Transformer 정책

공부할 내용:

- image encoder: CNN, ViT
- proprioception fusion
- Transformer sequence modeling
- language-conditioned action
- action 표현: joint target, velocity, end-effector delta pose

테스트:

- 단일 task image-conditioned policy 학습
- proprioception 추가
- language 또는 task ID 추가
- unseen object pose와 lighting에서 평가

다음 단계로 넘어가는 기준:

- 시각 observation을 robot action으로 변환하는 정책을 만들 수 있다.

## 10단계: 강화학습

공부할 내용:

- PPO, SAC
- reward shaping
- curriculum learning
- imitation-initialized RL
- off-policy replay와 on-policy rollout

테스트:

- PPO로 reach 학습
- PPO 또는 SAC로 grasp alignment 학습
- imitation policy를 RL로 fine-tuning
- training curve와 success rate 비교

다음 단계로 넘어가는 기준:

- RL이 필요한 상황을 판단하고 안정적인 학습 세팅을 설계할 수 있다.

## 11단계: Sim-to-Real 전이

공부할 내용:

- calibration: camera intrinsic, extrinsic, robot base alignment
- 실제 actuator limit과 latency
- ROS 2 bridge
- safety controller
- real-world evaluation protocol

테스트:

- Isaac Sim과 ROS 2 연결
- 시뮬레이션 trajectory를 실제 또는 mock robot interface로 replay
- simulated observation과 real observation 비교
- 저속 real-world validation 수행

다음 단계로 넘어가는 기준:

- 시뮬레이션과 실제 시스템 사이에서 무엇을 맞춰야 하는지 설명할 수 있다.

## 12단계: 대규모 학습 인프라

공부할 내용:

- multi-GPU training
- distributed simulation job
- experiment tracking
- dataset versioning
- failure mining과 자동 데이터 재생성

테스트:

- 대규모 vectorized simulation 실행
- W&B, MLflow 또는 유사 도구로 실험 추적
- dataset과 config 버전 관리
- batch dataset generation 자동화

다음 단계로 넘어가는 기준:

- 단일 실험을 반복 가능한 학습 파이프라인으로 확장할 수 있다.

## 13단계: VLA/RFM 평가 벤치마크

공부할 내용:

- task suite 구성
- instruction-conditioned evaluation
- multi-task, multi-embodiment 구성
- seen/unseen split
- metric: success rate, completion time, collision rate, recovery rate

테스트:

- benchmark suite 정의
- task instruction 작성
- 여러 policy를 같은 suite에서 평가
- metric을 재현 가능하게 보고

다음 단계로 넘어가는 기준:

- 시뮬레이션을 robot foundation model 스타일 정책의 평가 벤치마크로 사용할 수 있다.

## 진행 원칙

튜토리얼이 한 번 실행됐다고 다음 단계로 넘어가지 않습니다. 예제를 수정할 수 있고, 중요한 변수를 설명할 수 있고, 결과가 깨졌을 때 확인할 작은 테스트를 만들 수 있으면 다음 단계로 넘어갑니다.
