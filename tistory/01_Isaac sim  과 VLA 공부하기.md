![](https://blog.kakaocdn.net/dna/lGYHM/dJMcafGPwPF/AAAAAAAAAAAAAAAAAAAAAEgB5ufjfkvxBr1P7BMhz996EbPV8hz-7Bbr6IT3Rwtm/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1782831599&allow_ip=&allow_referer=&signature=dVaZk06mTaGXL8dIQUZ7dFgjNXc%3D)

로보티즈에서 다음과 같은 업무를 하는 직원을 모집하고 있다.

나도 로봇에 관심이 많고 이러한 VLA와 시뮬레이션에 대해 관심이 많았기 때문에 Isaac Sim을 사용하며 공부하기로 한다.

  

공부순서는 다음과 같다. LLM을 이용해서 학습 순서를 정했기 때문에 현재는 모르는 내용이 많다.
앞으로 학습을 할 예정이다.

1. 기초 준비
	1. 기본적인 python을 이용하여 정기구학, 역기구학 공부
	2. pytorch로 CNN/Trancsformer 학습하기
	3. 이론 정리
2. MuJoCo로 제어 감각 잡기
	1. Isaac Sim은 무겁고 복잡 -> MuJoCo를 이용하여 pick,reach, push 같은 작은 Task 먼저 해보기
	2. Mujoco에서 arm reach task실행
	3. observeation/action/reward 구조 이해
	4. PPO 또는 SAC로 간단한 policy 학습
	5. 이론 정리
3. Isaac Sim 기본 학습
	1. Isaac Sim 기반 모바일 매니퓰레이터 시뮬레이션 환경 구축하기
	2. USD stage, prim. articulation, physics material, joint drive, camera, lidar, depth sensor, RTX rendering을 학습
	3. Franka, UR5, mobile base 같은 기본 로봇 로드
	4. 카메라/depth/segmentation 이미지 저장
	5. 바닥,조명, 물체, collision 설정
	6. python script로 로봇 joint position 제어
4. Isaac Lab
	1. 강화학습/병렬환경/로봇학습을 하기 위해 Isaac Lab을 학습
	2. Isaac Laqb 예제 실행
	3. manager-based environment 구조 이해
	4. 수십-수천 개 병렬 환경 실행
	5. observation,action, reward, termination 커스터마이즈
5. 모바일 매니퓰레이터 환경 구축
	1. base 이동 + arm reach
	2. base navigation + pick pose 도달
	3. grasp 후보 pose 생성
	4. pick-and-place scripted policy 작성
	5. 실패 케이스 로그 수집
6. Domain Randomization
	1. texture, lighting, camera pose, object pose, mass, friction, joint noise, latency, sensor noise를 랜덤화
	2. 같은 pick task를 1000개 scene variation으로 생성
	3. RGB/depth/segmentation/action log 저장
	4. randomization 범위가 task를 망치지 않는지 성공률 측정
7. Synthetic Data Generation
	1. Isaac Sim Replicator 를 사용해서 합성 데이터를 자동 생성 -> 모방학습/ACT/Diffusion Policy용 시뮬레이션 사전학습 및 합성 데이터 자동생성의 기반
	2. RGB, Depth, semantic segmentation, instance segmentation 저장
	3. robot proprioception, end-effector pose, action trajectory 저장
	4. dataset schema 정하기: obs, action, reward, done, language, task_id
	5. HDFS/Zarr/WebDataset 중 하나로 저장
8. 모방학습
	1. 먼저 Behavior Cloning으로 시작하고 다음 ACT, Diffusion Policy로 진행.
	2. scripted expert로 1만 episode 생성
	3. BS baseline 학습
	4. ACT 학습
	5. Diffusion Policy 학습
	6. sim rollout success rate 비교
9. Visumotor Transformer
	1. CNN/Vit encoder + proprioception MLP + Transfomer policy
	2. single-task pick 학습
	3. multi-object pick 학습
	4. unseen object/lighting/camera에서 평가
10. 강화학습: PPO,SAC
	1. reach task PPO
	2. grasp alignment PPO
	3. pick lift reward 설계
	4. imitation initialized policy를 RL로 fine-tuning
	5. domain randomization 포함 학습
11. Sim-to-Real 전이
	1. 카메라 intrinsic/extrinsic calibration
	2. real robot joint limit/ velocity/torque limit 반영
	3. ROS 2 bridge 연결
	4. sim policy를 real robot에 low-speed로 실행
	5. failure log를 다시 sim randomization에 반영
12. 대규모 병렬 학습 인프라
	1. 단일 GPU에서 1024env
	2. multi-GPU 학습 
	3. Weights & Biases/MLflow 로깅
	4. dataset registry
	5. 실패 episode 자동 재수집
13. RFM/VLA 평가 벤치마크
	1. task suite 구성 : pick, place, push, open, close, navigate
	2. instruction template 작성
	3. seen/unseen object split
	4. seen/unseen scene split
	5. success rate, SPL, collision, completion time, recovery rate 측정


이 많은 양의 task순서를 최대한 빠르게 구현 및 정리를 해 볼 예정이다.