# Isaac Sim 내장 로봇 팔로 Isaac Lab 강화학습 시작하기

> 작성일: 2026-07-10  
> 이 문서는 현재 PC에 설치된 버전을 기준으로 작성했다.  
> - Isaac Sim: `6.0.0-rc.59` (`~/isaacsim`)  
> - Isaac Lab: `3.0.0`, branch `release/3.0.0-beta2` (`~/isaac/IsaacLab`)  

## 1. 결론부터

지금은 직접 만든 로봇 USD를 사용하지 않아도 된다. Isaac Sim에 포함된 Franka Panda를 Isaac Lab의 학습 task에서 바로 사용할 수 있다.

추천 순서는 다음과 같다.

```text
내장 Franka Reach 실행
        ↓
내장 Franka Lift-Cube 실행
        ↓
PPO 학습 및 checkpoint 재생
        ↓
기존 task 설정을 복사해 내 작업(목표 위치, 물체, reward)으로 수정
        ↓
필요할 때만 내 로봇 USD를 Isaac Lab에 연결
```

Isaac Sim은 물리 시뮬레이터와 USD asset을 제공하고, Isaac Lab은 병렬 환경·관측·행동·보상·리셋·강화학습 라이브러리를 묶어 제공한다. 따라서 강화학습을 할 때 Isaac Sim GUI에서 로봇을 수동 조작하는 것보다 Isaac Lab task를 실행하는 것이 기본 흐름이다.

## 2. 내장 로봇 팔 선택

처음에는 `Franka Panda`를 추천한다.

| 로봇 | 시작 task | 특징 |
|---|---|---|
| Franka Panda | Reach, Lift-Cube, Open-Drawer | Isaac Lab 예제가 가장 잘 갖춰져 있고 학습 확인이 쉽다 |
| UR10 | Reach, 일부 manipulation task | 6축 산업용 팔을 실험하기 좋다 |
| Kuka + Allegro | Lift-Cube 등 | 팔과 다관절 손을 함께 다룰 때 사용 |
| Isaac Sim 내장 기타 팔 | 직접 task 작성 | asset은 있어도 Isaac Lab 학습 task가 자동으로 생기지는 않는다 |

Isaac Sim 5.x 계열 문서 기준 Franka asset 경로는 다음과 같다.

```text
Robots/FrankaRobotics/FrankaPanda/franka.usd
```

Isaac Sim 6.x에서는 Content Browser의 `Isaac Sim/Robots` 아래에서 로봇을 찾는다. 메뉴에서는 대체로 `Create > Robots > Franka Emika Panda Arm`으로 추가할 수 있다. 단, Isaac Lab의 기본 manipulation task는 asset을 직접 드래그하는 대신 task 설정 안에서 필요한 robot configuration을 불러온다.

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

## 4. 첫 실행: Franka Reach

Reach는 로봇 팔의 end-effector가 랜덤으로 주어진 목표 pose로 이동하도록 학습하는 가장 좋은 첫 task다.

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

## 5. 두 번째 실행: Franka Lift-Cube

Lift-Cube는 Franka가 큐브를 집어 목표 높이까지 들어 올리는 task다. Reach보다 grasp와 접촉 물리가 포함되어 있어 강화학습 실습에 더 적합하다.

짧은 학습 확인:

```bash
cd ~/isaac/IsaacLab
./isaaclab.sh train \
  --rl_library rsl_rl \
  --task Isaac-Lift-Cube-Franka-v0 \
  --num_envs 64 \
  --max_iterations 10
```

실제 학습:

```bash
./isaaclab.sh train \
  --rl_library rsl_rl \
  --task Isaac-Lift-Cube-Franka-v0 \
  --num_envs 1024 \
  --max_iterations 2000 \
  --headless
```

학습 결과는 보통 다음 계열의 디렉터리에 저장된다.

```text
~/isaac/IsaacLab/logs/rsl_rl/
```

정확한 experiment 이름은 실행 시 출력되는 로그 경로를 확인한다.

## 6. 학습된 정책 재생하기

학습이 끝나면 checkpoint를 사용해 policy를 재생한다. 현재 Isaac Lab 3.x에서는 통합 wrapper 형식을 우선 사용한다.

```bash
cd ~/isaac/IsaacLab
./isaaclab.sh play \
  --rl_library rsl_rl \
  --task Isaac-Lift-Cube-Franka-v0 \
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
./isaaclab.sh play --rl_library rsl_rl --task Isaac-Lift-Cube-Franka-v0 --help
```

## 7. 행동·관측·보상은 무엇인가

강화학습 task를 이해할 때 아래 네 가지를 먼저 찾으면 된다.

| 구성 | Franka Lift-Cube 예시 |
|---|---|
| Observation | 관절 위치/속도, end-effector와 큐브의 상대 위치, 큐브 높이 |
| Action | 관절 위치 목표 또는 IK 기반 end-effector 이동량 |
| Reward | 큐브에 가까워짐, grasp 성공, 목표 높이까지 들어 올림 |
| Termination/Reset | 성공, 시간 초과, 비정상 상태 발생 후 초기화 |

기본 joint-position task와 IK task는 학습 난이도가 다르다. 처음에는 `Isaac-Lift-Cube-Franka-v0`처럼 joint position control을 사용하고, 이후 다음 계열을 비교한다.

```text
IsaacContrib-Lift-Cube-Franka-IK-Abs-v0
IsaacContrib-Lift-Cube-Franka-IK-Rel-v0
```

현재 저장소에서 실제 등록 이름이 다를 수 있으므로 반드시 목록으로 확인한다.

```bash
./isaaclab.sh -p scripts/environments/list_envs.py --keyword Lift-Cube
```

## 8. 내 task로 바꾸는 방법

처음부터 새 환경을 만들기보다 기존 Franka task를 복사해 수정한다.

### 8.1 Manager-Based workflow를 우선 사용

Lift-Cube는 보통 manager-based 구조로 구성되어 있다. 다음 항목을 설정 클래스에서 바꾼다.

```text
scene       로봇, 테이블, 큐브, 조명, 센서
actions     joint position / IK action의 크기와 스케일
observations 관절 상태, 물체 pose, 목표 pose
rewards     거리 보상, grasp 보상, lift 보상, 패널티
terminations 성공 조건, 시간 제한, 실패 조건
events      reset 시 위치·질량·마찰·목표 랜덤화
```

### 8.2 Direct workflow는 나중에 사용

보상과 관측을 한 파일에서 직접 계산하고 싶거나 custom physics 계산이 많으면 `DirectRLEnv`를 사용한다. Isaac Lab 공식 문서도 manager-based와 direct workflow를 모두 제공하지만, 처음 task를 수정할 때는 기존 manager-based Lift-Cube를 복사하는 편이 빠르다.

### 8.3 커스텀 프로젝트 생성

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
1. Franka를 scene에 배치
2. 큐브와 테이블 배치
3. observation shape 확인
4. action이 실제 관절을 움직이는지 확인
5. reward를 하나씩 추가
6. reset randomization 추가
7. 10 iteration → 100 iteration → 장시간 학습 순으로 검증
```

## 9. Isaac Sim 내장 USD를 직접 바꿔 쓰고 싶을 때

로봇을 Isaac Sim GUI에서 직접 배치하고 제어하는 테스트는 별도로 할 수 있다.

```text
Isaac Sim 실행
→ Create > Robots > Franka Emika Panda Arm
→ Physics/Articulation 설정 확인
→ 관절 이름과 gripper joint 확인
→ 필요하면 별도의 scene.usd로 저장
```

하지만 학습에서는 다음을 구분해야 한다.

- Isaac Sim에서 저장한 `scene.usd`: 시각적 scene 또는 custom asset
- Isaac Lab의 task config: 병렬 복제, observation, action, reward, reset을 정의하는 학습 환경

따라서 GUI에서 만든 USD를 저장했다고 해서 PPO 학습 task가 자동으로 만들어지지는 않는다. custom USD를 Isaac Lab에서 사용하려면 scene configuration에 USD 경로를 연결하고, articulation의 joint/body 이름과 action·observation 설정을 맞춰야 한다.

## 10. 기존에 만든 6-DOF arm USD를 연결하는 시점

지금 바로 기존 USD를 연결하는 것보다 Franka Reach/Lift-Cube가 먼저다. 이유는 학습 실패 원인을 분리하기 위해서다.

```text
Franka task 학습 성공
→ 내 6-DOF USD의 articulation 구조 확인
→ joint 이름/순서 확인
→ drive stiffness, damping, limit 확인
→ end-effector body와 gripper 정의
→ Franka task의 robot config를 내 로봇 config로 교체
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

## 11. 자주 생기는 문제

### `Task not found`

task 이름이나 버전이 맞지 않는 경우다.

```bash
./isaaclab.sh -p scripts/environments/list_envs.py --keyword Franka
```

출력된 정확한 이름을 `--task`에 사용한다. 문서 버전에 따라 예전의 `-v0` 접미사가 없거나 task 이름이 바뀔 수 있다.

### GPU 메모리 부족

```bash
./isaaclab.sh train --rl_library rsl_rl \
  --task Isaac-Lift-Cube-Franka-v0 \
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

## 12. 추천 실습 순서

```text
[ ] Isaac-Reach-Franka 실행
[ ] Isaac-Lift-Cube-Franka 실행
[ ] num_envs=64와 1024의 속도 비교
[ ] PPO checkpoint 저장 위치 확인
[ ] checkpoint play 실행
[ ] observation 항목 하나 출력
[ ] reward weight 하나 변경
[ ] reset 시 큐브 위치 랜덤화
[ ] Open-Drawer 또는 Stack-Cube 실행
[ ] 내 6-DOF USD를 Reach task에 연결
```

## 13. 참고 링크

- [Isaac Lab 공식 Quickstart](https://isaac-sim.github.io/IsaacLab/main/source/setup/quickstart.html)
- [Isaac Lab 사용 가능한 환경](https://isaac-sim.github.io/IsaacLab/release/3.0.0-beta2/source/overview/environments.html)
- [Direct RL environment 작성법](https://isaac-sim.github.io/IsaacLab/develop/source/tutorials/03_envs/create_direct_rl_env.html)
- [Isaac Sim 로봇 asset 목록](https://docs.isaacsim.omniverse.nvidia.com/5.0.0/assets/usd_assets_robots.html)
- [Isaac Sim Manipulator 추가 튜토리얼](https://docs.isaacsim.omniverse.nvidia.com/latest/core_api_tutorials/tutorial_core_adding_manipulator.html)

## 핵심 명령만 다시 보기

```bash
cd ~/isaac/IsaacLab

# Franka task 검색
./isaaclab.sh -p scripts/environments/list_envs.py --keyword Franka

# 짧은 Reach 확인
./isaaclab.sh train --rl_library rsl_rl \
  --task Isaac-Reach-Franka-v0 --num_envs 64 --max_iterations 10

# 짧은 Lift-Cube 확인
./isaaclab.sh train --rl_library rsl_rl \
  --task Isaac-Lift-Cube-Franka-v0 --num_envs 64 --max_iterations 10

# 실제 학습 예시
./isaaclab.sh train --rl_library rsl_rl \
  --task Isaac-Lift-Cube-Franka-v0 --num_envs 1024 \
  --max_iterations 2000 --headless
```

