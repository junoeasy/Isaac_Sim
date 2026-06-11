# 3단계: Isaac Sim 기초

## 목적

Isaac Sim에서 scene을 만들고, 로봇과 물체를 배치하고, 카메라/센서 데이터를 얻는 기본 능력을 만드는 단계입니다. 이 단계에서는 학습보다 시뮬레이터 조작 자체가 목표입니다.

## 공부할 내용

### 1. USD와 Scene 구조

공부할 내용:

- USD stage
- prim
- xform
- mesh
- articulation
- reference
- layer

핵심 개념:

```text
Isaac Sim scene은 USD stage 위에 prim들이 계층적으로 배치된 구조다.
```

테스트:

- 빈 stage 만들기
- cube prim 추가
- cube 위치, 회전, scale 바꾸기
- prim path를 통해 물체 찾기

### 2. 물리 시뮬레이션

공부할 내용:

- PhysX
- collider
- rigid body
- mass
- friction
- restitution
- timestep

테스트:

- cube를 공중에 놓고 떨어뜨리기
- 바닥 friction 바꾸기
- 질량을 바꾸고 움직임 비교
- collision이 켜진 물체와 꺼진 물체 비교

### 3. 로봇 Articulation

공부할 내용:

- articulation root
- joint
- joint drive
- position target
- velocity target
- effort target

테스트:

- 기본 로봇 asset 로드
- joint 이름 출력
- joint position 읽기
- joint target을 보내서 움직이기

### 4. 카메라와 센서

공부할 내용:

- RGB camera
- depth
- semantic segmentation
- instance segmentation
- camera intrinsic/extrinsic

테스트:

- 카메라 추가
- RGB 이미지 저장
- depth 이미지 저장
- segmentation 결과 저장
- 카메라 pose를 바꾸고 이미지 변화 확인

## 실습 목표

이 단계의 최소 결과물은 아래입니다.

```text
테이블 위 물체와 로봇 하나가 있는 scene을 만들고,
카메라 이미지와 로봇 joint 상태를 Python으로 읽는다.
```

## 완료 체크리스트

- [ ] USD stage와 prim의 의미를 설명할 수 있다.
- [ ] 물체의 pose를 코드로 바꿀 수 있다.
- [ ] 로봇 articulation의 joint 상태를 읽을 수 있다.
- [ ] 카메라 RGB/depth 데이터를 저장할 수 있다.
- [ ] scene을 Python script로 재현할 수 있다.

## 실습: Cube rigid body와 pose 제어

실행:

```bash
cd /home/junho/Isaac_Sim
/home/junho/isaacsim/python.sh exercises/isaac_cube_rigid_body.py
```

이 예제에서 하는 일:

- `/World/GroundPlane` 생성
- `/World/DynamicCube` 생성
- `RigidPrim`으로 rigid body 적용
- `GeomPrim(..., apply_collision_apis=True)`로 collider 적용
- `get_world_poses()`로 Cube 위치 읽기
- `set_world_poses()`로 Cube 위치 바꾸기
- `get_velocities()`로 속도 읽기
- `set_velocities()`로 선속도/각속도 바꾸기

핵심 코드:

```python
cube = RigidPrim(paths="/World/DynamicCube", masses=1.0)
GeomPrim(paths="/World/DynamicCube", apply_collision_apis=True)

positions, orientations = cube.get_world_poses()
linear_velocities, angular_velocities = cube.get_velocities()

cube.set_world_poses(
    positions=[[0.0, 0.0, 2.5]],
    orientations=[[1.0, 0.0, 0.0, 0.0]],
)
cube.set_velocities(
    linear_velocities=[[0.0, 1.2, 0.0]],
    angular_velocities=[[0.0, 0.0, 4.0]],
)
```

일반 Python이나 프로젝트 `.venv`로 실행하면 안 됩니다. Isaac Sim extension runtime이 필요하므로 반드시 `~/isaacsim/python.sh`를 사용합니다.

## 실습: Franka robot asset과 joint 제어

실행:

```bash
cd /home/junho/Isaac_Sim
/home/junho/isaacsim/python.sh exercises/isaac_franka_joint_control.py
```

이 예제에서 하는 일:

- Isaac Sim 내장 Franka Panda USD asset 로드
- `/World/Franka`에 reference로 배치
- `Articulation`으로 로봇 제어 객체 생성
- `robot.dof_names`로 joint 이름 출력
- `get_dof_positions()`로 joint position 읽기
- `set_dof_position_targets()`로 joint target 보내기

핵심 코드:

```python
franka_usd = assets_root_path + "/Isaac/Robots/FrankaRobotics/FrankaPanda/franka.usd"
stage_utils.add_reference_to_stage(usd_path=franka_usd, path="/World/Franka")

robot = Articulation("/World/Franka")

print(robot.dof_names)
print(robot.get_dof_positions())

robot.set_dof_position_targets([
    0.0, -0.4, 0.0, -2.2, 0.0, 2.0, 0.8, 0.04, 0.04
])
```

Franka의 앞 7개 DOF는 팔 joint이고, 마지막 2개는 gripper finger joint입니다. 실행 중 콘솔에 joint 이름이 출력되므로, 실제 이름과 순서를 먼저 확인한 뒤 원하는 joint만 골라 제어하면 됩니다.

특정 joint만 움직이고 싶을 때:

```python
joint_index = robot.dof_names.index("panda_joint2")
robot.set_dof_position_targets(-0.8, dof_indices=[joint_index])
```

## 다음 단계와 연결

Isaac Lab은 Isaac Sim 위에서 RL/IL용 환경을 구조화해주는 프레임워크입니다. Isaac Sim의 stage, articulation, sensor 개념을 모르면 Isaac Lab task를 수정할 때 막히므로 이 단계가 중요합니다.
