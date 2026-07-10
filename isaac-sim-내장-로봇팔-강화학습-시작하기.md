# ROBOTIS OpenMANIPULATOR-X로 Isaac Lab 강화학습 시작하기

> 작성일: 2026-07-10  
> 이 문서는 현재 PC에 설치된 버전과 ROBOTIS `OpenMANIPULATOR-X`를 기준으로 작성했다.  
> - Isaac Sim: `6.0.0-rc.59` (`~/isaacsim`)  
> - Isaac Lab: `3.0.0`, branch `release/3.0.0-beta2` (`~/isaac/IsaacLab`)  

## 1. 결론부터

Franka Panda는 Isaac Lab 구조를 배우기 위한 참고용 로봇이고, 최종 목표는 ROBOTIS `OpenMANIPULATOR-X`로 둔다. OpenMANIPULATOR-X는 Franka처럼 Isaac Lab에 기본 등록된 완성 task가 아닐 수 있으므로, 로봇 모델을 준비한 뒤 ROBOTIS용 task를 직접 연결해야 한다.

추천 순서는 다음과 같다.

```text
Franka Reach 예제로 Isaac Lab 구조 확인
        ↓
OpenMANIPULATOR-X 모델을 Isaac Sim에서 검증
        ↓
ROBOTIS용 Reach 환경 작성
        ↓
ROBOTIS용 Lift/Pick-and-Place 환경 작성
        ↓
PPO 학습·checkpoint 재생·Sim-to-Real 준비
```

Isaac Sim은 물리 시뮬레이터와 USD asset을 제공하고, Isaac Lab은 병렬 환경·관측·행동·보상·리셋·강화학습 라이브러리를 묶어 제공한다. 따라서 강화학습을 할 때 Isaac Sim GUI에서 로봇을 수동 조작하는 것보다 Isaac Lab task를 실행하는 것이 기본 흐름이다.

## 2. ROBOTIS 모델과 준비물

이 문서에서는 `OpenMANIPULATOR-X`를 사용한다. ROBOTIS의 OMY, OMX, AI Worker를 사용하는 경우에도 전체 원리는 같지만 관절 수, joint 이름, gripper, USD 경로가 달라진다.

| 로봇 | 시작 task | 특징 |
|---|---|---|
| 모델 | 용도 | 이 문서에서의 역할 |
|---|---|---|
| OpenMANIPULATOR-X | 교육·연구용 소형 로봇팔 | 최종 학습·실제 로봇 배포 대상 |
| OMY / OMX | ROBOTIS AI Manipulator | 공식 USD/ROS 2 모델을 사용할 수 있는 대안 |
| Franka Panda | Isaac Lab 기본 manipulation 예제 | task 구조를 먼저 확인하는 참고용 |

OpenMANIPULATOR-X는 ROBOTIS 공식 ROS 2 저장소에서 URDF/Xacro와 joint 정보를 확인한다. Isaac Sim에서 사용할 수 있는 USD가 이미 있다면 그 USD를 우선 사용하고, 없다면 URDF를 Isaac Sim에서 import한 뒤 articulation을 검증한다.

```text
open_manipulator/open_manipulator_x_description/urdf/open_manipulator_x.urdf.xacro
```

ROBOTIS는 공식 open-source 페이지에서 OMY/OMX/AI Worker의 URDF, MJCF, USD simulation model을 제공한다. OpenMANIPULATOR-X는 공식 ROS 2 패키지와 URDF를 기준으로 모델을 준비한다. 모델을 Isaac Sim에서 열었다고 해서 Isaac Lab task가 자동 생성되는 것은 아니다.

필요한 준비물:

- OpenMANIPULATOR-X의 URDF/Xacro 또는 USD
- 관절 이름·순서·limit·방향 정보
- end-effector와 gripper joint 이름
- 실제 로봇을 사용할 경우 DYNAMIXEL/ROS 2 제어 인터페이스
- 물리용 collision mesh와 질량·관성 정보

## 3. Isaac Lab 디렉터리와 실행 전 확인

현재 작업 디렉터리는 다음처럼 사용한다.

```bash
cd ~/isaac/IsaacLab
```

설치 상태를 확인한다.

```bash
cat ~/isaacsim/VERSION
cat ~/isaac/IsaacLab/VERSION
git -C ~/isaac/IsaacLab branch --show-current
```

Isaac Lab이 인식하는 task 목록은 다음 명령으로 확인한다.

```bash
cd ~/isaac/IsaacLab
./isaaclab.sh -p scripts/environments/list_envs.py --keyword Franka
```

이 명령이 실패하면 먼저 설치 환경을 확인한다.

```bash
ls -l ~/isaac/IsaacLab/_isaac_sim
ls -l ~/isaac/IsaacLab/isaaclab.sh
```

현재 저장소는 `~/isaacsim`을 `~/isaac/IsaacLab/_isaac_sim`으로 연결해 둔 상태다. 일반적으로 Isaac Lab은 이 wrapper를 통해 Isaac Sim을 실행하므로 별도로 `python`을 골라 실행하지 않는 것이 안전하다.

## 4. 첫 실행: Franka Reach로 Isaac Lab 구조 확인

ROBOTIS용 task를 만들기 전에 Franka Reach를 10 iteration 정도 실행한다. 이 단계의 목적은 Franka를 최종 사용하려는 것이 아니라, 학습 스크립트·로그·checkpoint·manager 구조가 정상인지 확인하는 것이다.

먼저 GUI가 보이는 짧은 실행으로 환경이 정상인지 확인한다.

```bash
cd ~/isaac/IsaacLab
./isaaclab.sh train \
  --rl_library rsl_rl \
  --task Isaac-Reach-Franka-v0 \
  --num_envs 64 \
  --max_iterations 10
```

학습을 빠르게 돌릴 때는 화면을 끄고 환경 수를 늘린다.

```bash
./isaaclab.sh train \
  --rl_library rsl_rl \
  --task Isaac-Reach-Franka-v0 \
  --num_envs 1024 \
  --max_iterations 1000 \
  --headless
```

`num_envs`는 동시에 실행하는 복제 환경의 수다. GPU 메모리가 부족하면 `1024`를 `256` 또는 `64`로 낮춘다.

## 5. ROBOTIS 모델을 Isaac Sim에서 먼저 검증

Isaac Lab에 연결하기 전에 Isaac Sim에서 OpenMANIPULATOR-X의 articulation이 정상인지 확인한다. 처음부터 PPO를 실행하지 말고 관절 하나씩 움직이는 테스트를 한다.

확인할 항목:

- articulation root가 하나인가
- 모든 link/joint가 하나의 chain으로 연결되는가
- joint 수와 이름이 예상과 같은가
- 각 joint의 lower/upper limit과 회전 방향이 맞는가
- base가 고정되어 있는가
- gripper가 별도 joint로 움직이는가
- collision mesh와 inertial property가 존재하는가

OpenMANIPULATOR-X의 실제 joint 목록은 모델 파일에서 확인하고, Isaac Lab 코드에는 그 순서를 명시적으로 고정한다. `joint_1`, `joint_2`처럼 이름을 추측하지 말고 USD/URDF에서 실제 이름을 복사한다.

## 6. ROBOTIS용 Reach task 만들기

Isaac Lab 기본 Franka Reach task를 복사해 ROBOTIS용 task로 바꾼다. 처음에는 큐브나 카메라를 넣지 말고 end-effector 위치 제어만 성공시키는 것이 좋다.

```text
Franka Reach 설정 복사
        ↓
ROBOTIS USD 경로로 robot asset 교체
        ↓
ROBOTIS joint 이름·순서·limit 반영
        ↓
end-effector body 이름 반영
        ↓
action 차원을 ROBOTIS 관절 수에 맞춤
        ↓
observation과 reward에서 ROBOTIS body 참조
```

ROBOTIS용 Reach의 최소 구성은 다음과 같다.

| 구성 | OpenMANIPULATOR-X 예시 |
|---|---|
| Observation | 모든 관절 position/velocity, end-effector pose, 목표 위치, 이전 action |
| Action | 관절 position target 또는 end-effector IK target |
| Reward | end-effector와 목표 위치의 거리 감소, 최종 도달 보상 |
| Reset | 관절 초기 pose와 목표 위치 랜덤화 |

처음에는 joint-position action을 추천한다. IK action은 로봇의 실제 end-effector body와 좌표계가 정확히 확인된 뒤 사용한다.

예시 실행 명령은 새 task 이름에 맞춰 바꾼다.

```bash
cd ~/isaac/IsaacLab
./isaaclab.sh train \
  --rl_library rsl_rl \
  --task Isaac-Reach-OpenManipulatorX-v0 \
  --num_envs 64 \
  --max_iterations 10
```

위 task 이름은 새로 등록할 이름의 예시다. 아직 task를 등록하지 않았다면 `Task not found`가 정상이며, 먼저 custom environment를 만들고 Gymnasium task registry에 등록해야 한다.

## 7. ROBOTIS용 Lift-Cube/Pick-and-Place

Reach가 성공한 뒤 큐브와 테이블을 추가한다. Lift-Cube는 Franka용 task를 참고하되, ROBOTIS의 gripper joint와 end-effector body를 반드시 새로 지정한다.

```text
1. 큐브를 ROBOTIS gripper 앞에 배치
2. Approach reward 추가
3. gripper close action 추가
4. 큐브와 손가락의 접촉 확인
5. grasp 유지 reward 추가
6. 큐브 높이 상승 reward 추가
7. 성공 시 reset
```

```bash
./isaaclab.sh train \
  --rl_library rsl_rl \
  --task Isaac-Lift-Cube-OpenManipulatorX-v0 \
  --num_envs 64 \
  --max_iterations 10
```

이 명령도 custom task 등록 이후 사용하는 예시다. 처음에는 `num_envs=1` 또는 `16`으로 gripper 접촉과 action 방향부터 확인한다.

학습 결과는 보통 다음 계열의 디렉터리에 저장된다.

```text
~/isaac/IsaacLab/logs/rsl_rl/
```

정확한 experiment 이름은 실행 시 출력되는 로그 경로를 확인한다.

## 8. 학습된 정책 재생하기

학습이 끝나면 checkpoint를 사용해 policy를 재생한다. 현재 Isaac Lab 3.x에서는 통합 wrapper 형식을 우선 사용한다.

```bash
cd ~/isaac/IsaacLab
./isaaclab.sh play \
  --rl_library rsl_rl \
  --task Isaac-Lift-Cube-OpenManipulatorX-v0 \
  --num_envs 16 \
  --checkpoint /절대경로/모델.pt
```

`/절대경로/모델.pt`는 학습 로그 아래에서 찾는다.

```bash
find ~/isaac/IsaacLab/logs/rsl_rl -type f \( -name '*.pt' -o -name '*.pth' \) | sort | tail -20
```

현재 branch에서 `play` 옵션이 task별로 다르게 보이면 도움말을 확인한다.

```bash
./isaaclab.sh play --help
./isaaclab.sh play --rl_library rsl_rl --task Isaac-Lift-Cube-OpenManipulatorX-v0 --help
```

## 9. 행동·관측·보상은 무엇인가

강화학습 task를 이해할 때 아래 네 가지를 먼저 찾으면 된다.

| 구성 | OpenMANIPULATOR-X Lift-Cube 예시 |
|---|---|
| Observation | 관절 위치/속도, end-effector와 큐브의 상대 위치, 큐브 높이 |
| Action | 관절 위치 목표 또는 IK 기반 end-effector 이동량 |
| Reward | 큐브에 가까워짐, grasp 성공, 목표 높이까지 들어 올림 |
| Termination/Reset | 성공, 시간 초과, 비정상 상태 발생 후 초기화 |

기본 joint-position task와 IK task는 학습 난이도가 다르다. 처음에는 OpenMANIPULATOR-X용 joint position control을 사용하고, 이후 IK control을 비교한다.

```text
Isaac-Lift-Cube-OpenManipulatorX-IK-Abs-v0
Isaac-Lift-Cube-OpenManipulatorX-IK-Rel-v0
```

현재 저장소에서 실제 등록 이름이 다를 수 있으므로 반드시 목록으로 확인한다.

```bash
./isaaclab.sh -p scripts/environments/list_envs.py --keyword Lift-Cube
```

## 10. 내 task로 바꾸는 방법

처음부터 새 환경을 만들기보다 Isaac Lab의 Franka Reach/Lift task 구조를 참고해 OpenMANIPULATOR-X용 task를 만든다. Franka의 관절 수·joint 이름·gripper 이름을 그대로 복사하면 안 된다.

### 10.1 Manager-Based workflow를 우선 사용

Lift-Cube는 보통 manager-based 구조로 구성되어 있다. 다음 항목을 설정 클래스에서 바꾼다.

```text
scene       로봇, 테이블, 큐브, 조명, 센서
actions     joint position / IK action의 크기와 스케일
observations 관절 상태, 물체 pose, 목표 pose
rewards     거리 보상, grasp 보상, lift 보상, 패널티
terminations 성공 조건, 시간 제한, 실패 조건
events      reset 시 위치·질량·마찰·목표 랜덤화
```

### 10.2 Direct workflow는 나중에 사용

보상과 관측을 한 파일에서 직접 계산하고 싶거나 custom physics 계산이 많으면 `DirectRLEnv`를 사용한다. Isaac Lab 공식 문서도 manager-based와 direct workflow를 모두 제공하지만, 처음 task를 수정할 때는 기존 manager-based Lift-Cube를 복사하는 편이 빠르다.

### 10.3 커스텀 프로젝트 생성

현재 branch에서 제공하는 scaffold 명령을 확인한다.

```bash
./isaaclab.sh --help
```

지원되는 경우 다음 명령으로 새 프로젝트 뼈대를 만든다.

```bash
./isaaclab.sh --new
```

그 후 새 프로젝트에서 다음 순서로 개발한다.

```text
1. OpenMANIPULATOR-X USD를 scene에 배치
2. 큐브와 테이블 배치
3. observation shape 확인
4. action이 실제 관절을 움직이는지 확인
5. reward를 하나씩 추가
6. reset randomization 추가
7. 10 iteration → 100 iteration → 장시간 학습 순으로 검증
```

## 11. Isaac Sim에서 ROBOTIS 모델 검증하기

로봇을 Isaac Sim GUI에서 직접 배치하고 제어하는 테스트는 별도로 할 수 있다.

```text
Isaac Sim 실행
→ OpenMANIPULATOR-X USD 또는 URDF import
→ Physics/Articulation 설정 확인
→ 관절 이름과 gripper joint 확인
→ 필요하면 별도의 scene.usd로 저장
```

하지만 학습에서는 다음을 구분해야 한다.

- Isaac Sim에서 저장한 `scene.usd`: 시각적 scene 또는 custom asset
- Isaac Lab의 task config: 병렬 복제, observation, action, reward, reset을 정의하는 학습 환경

따라서 GUI에서 만든 USD를 저장했다고 해서 PPO 학습 task가 자동으로 만들어지지는 않는다. custom USD를 Isaac Lab에서 사용하려면 scene configuration에 USD 경로를 연결하고, articulation의 joint/body 이름과 action·observation 설정을 맞춰야 한다.

## 12. 기존에 만든 6-DOF arm USD를 연결하는 시점

OpenMANIPULATOR-X Reach가 먼저다. 그 다음 기존에 만든 6-DOF USD를 같은 custom Reach task에 연결한다. 두 로봇을 비교하면 학습 실패가 task 문제인지 모델 문제인지 분리하기 쉽다.

```text
OpenMANIPULATOR-X Reach task 학습 성공
→ 내 6-DOF USD의 articulation 구조 확인
→ joint 이름/순서 확인
→ drive stiffness, damping, limit 확인
→ end-effector body와 gripper 정의
→ OpenMANIPULATOR-X robot config를 내 로봇 config로 교체
→ 동일한 Reach task로 동작 확인
→ 그 다음 Lift/Grasp reward 추가
```

내 USD에서 특히 확인할 것:

- 하나의 articulation root 아래에 모든 link와 joint가 연결되어 있는가
- joint가 올바른 parent-to-child 방향으로 연결되어 있는가
- 각 joint에 drive와 limit이 있는가
- 로봇의 base가 고정되어 있는가
- end-effector body prim 이름을 코드에서 찾을 수 있는가
- gripper가 실제로 닫히고 물체와 충돌하는가
- collision mesh와 visual mesh가 분리되어 있는가

## 13. 자주 생기는 문제

### `Task not found`

task 이름이나 버전이 맞지 않는 경우다.

```bash
./isaaclab.sh -p scripts/environments/list_envs.py --keyword OpenManipulator
```

출력된 정확한 이름을 `--task`에 사용한다. 문서 버전에 따라 예전의 `-v0` 접미사가 없거나 task 이름이 바뀔 수 있다.

### GPU 메모리 부족

```bash
./isaaclab.sh train --rl_library rsl_rl \
  --task Isaac-Lift-Cube-OpenManipulatorX-v0 \
  --num_envs 64 \
  --max_iterations 10 \
  --headless
```

먼저 `num_envs`와 camera 사용 여부를 줄인다.

### Isaac Sim 창은 뜨지만 로봇이 이상하게 움직임

학습 전에 `num_envs=1` 또는 `16`으로 실행하고 다음을 확인한다.

- action scale이 너무 크지 않은가
- joint limit 순서가 맞는가
- drive stiffness/damping이 설정됐는가
- 초기 관절 pose가 충돌 상태가 아닌가
- end-effector body 이름이 정확한가

### 학습 reward가 올라가지 않음

처음부터 grasp와 lift를 동시에 해결하려 하지 않는다.

```text
1. Reach: end-effector를 목표 위치로 이동
2. Approach: 큐브 위로 이동
3. Grasp: 손가락을 닫고 접촉 유지
4. Lift: 큐브 높이를 올림
5. Place: 목표 위치에 놓음
```

## 14. 추천 실습 순서

```text
[ ] Isaac-Reach-Franka로 Isaac Lab 구조 확인
[ ] OpenMANIPULATOR-X articulation 검증
[ ] Isaac-Reach-OpenManipulatorX custom task 실행
[ ] Isaac-Lift-Cube-OpenManipulatorX custom task 실행
[ ] num_envs=64와 1024의 속도 비교
[ ] PPO checkpoint 저장 위치 확인
[ ] checkpoint play 실행
[ ] observation 항목 하나 출력
[ ] reward weight 하나 변경
[ ] reset 시 큐브 위치 랜덤화
[ ] Open-Drawer 또는 Stack-Cube 실행
[ ] 기존 6-DOF USD를 OpenMANIPULATOR-X Reach task에 연결
```

## 15. 참고 링크

- [Isaac Lab 공식 Quickstart](https://isaac-sim.github.io/IsaacLab/main/source/setup/quickstart.html)
- [Isaac Lab 사용 가능한 환경](https://isaac-sim.github.io/IsaacLab/release/3.0.0-beta2/source/overview/environments.html)
- [Direct RL environment 작성법](https://isaac-sim.github.io/IsaacLab/develop/source/tutorials/03_envs/create_direct_rl_env.html)
- [Isaac Sim 로봇 asset 목록](https://docs.isaacsim.omniverse.nvidia.com/5.0.0/assets/usd_assets_robots.html)
- [Isaac Sim Manipulator 추가 튜토리얼](https://docs.isaacsim.omniverse.nvidia.com/latest/core_api_tutorials/tutorial_core_adding_manipulator.html)
- [ROBOTIS Open Source / Isaac Sim Models](https://ai.robotis.com/opensource.html)
- [ROBOTIS OpenMANIPULATOR 공식 ROS 2 저장소](https://github.com/ROBOTIS-GIT/open_manipulator)
- [OpenMANIPULATOR-X 공식 문서](https://emanual.robotis.com/docs/en/platform/openmanipulator_x/)

## 핵심 명령만 다시 보기

```bash
cd ~/isaac/IsaacLab

# Franka 참고 task 검색
./isaaclab.sh -p scripts/environments/list_envs.py --keyword Franka

# 짧은 Reach 확인
./isaaclab.sh train --rl_library rsl_rl \
  --task Isaac-Reach-Franka-v0 --num_envs 64 --max_iterations 10

# ROBOTIS custom Reach 예시
./isaaclab.sh train --rl_library rsl_rl \
  --task Isaac-Reach-OpenManipulatorX-v0 --num_envs 64 --max_iterations 10

# ROBOTIS custom Lift-Cube 예시
./isaaclab.sh train --rl_library rsl_rl \
  --task Isaac-Lift-Cube-OpenManipulatorX-v0 --num_envs 1024 \
  --max_iterations 2000 --headless
```
