from __future__ import annotations

import argparse
import sys

parser = argparse.ArgumentParser()
parser.add_argument("--headless", action="store_true")
parser.add_argument("--test", action="store_true")
args, _ = parser.parse_known_args()

from isaacsim import SimulationApp

# Isaac Sim extension/runtime을 먼저 띄워야 isaacsim.* 모듈을 import할 수 있다.
simulation_app = SimulationApp({"headless": args.headless})

import carb
import isaacsim.core.experimental.utils.app as app_utils
import isaacsim.core.experimental.utils.stage as stage_utils
from isaacsim.core.experimental.objects import DistantLight, GroundPlane
from isaacsim.core.experimental.prims import Articulation, XformPrim
from isaacsim.core.utils.viewports import set_camera_view
from isaacsim.storage.native import get_assets_root_path


def main() -> None:
    # Isaac Sim이 제공하는 기본 asset root 경로를 찾는다.
    assets_root_path = get_assets_root_path()
    if assets_root_path is None:
        carb.log_error("Could not find Isaac Sim assets folder")
        sys.exit(1)

    # 빈 USD stage를 새로 만들고, meter 단위로 scene scale을 맞춘다.
    stage_utils.create_new_stage()
    stage_utils.set_stage_units(meters_per_unit=1.0)

    # 로봇이 서 있을 바닥을 만든다.
    GroundPlane("/World/GroundPlane", positions=[0.0, 0.0, 0.0])

    # viewport에서 로봇이 잘 보이도록 조명을 추가한다.
    light = DistantLight("/World/DistantLight")
    light.set_intensities(500)

    # Isaac Sim 내장 Franka Panda USD asset을 stage에 reference로 불러온다.
    franka_usd = assets_root_path + "/Isaac/Robots/FrankaRobotics/FrankaPanda/franka.usd"
    stage_utils.add_reference_to_stage(usd_path=franka_usd, path="/World/Franka")

    # Articulation을 만들기 전에 root prim의 초기 위치를 잡는다.
    franka_xform = XformPrim("/World/Franka")
    franka_xform.set_world_poses(positions=[0.0, 0.0, 0.0])

    # Articulation은 여러 joint로 이루어진 로봇을 제어하는 wrapper다.
    robot = Articulation("/World/Franka")

    # GUI 실행 시 Franka가 바로 보이도록 viewport 카메라 위치를 잡는다.
    set_camera_view(
        eye=[2.8, -3.2, 2.0],
        target=[0.0, 0.0, 0.8],
        camera_prim_path="/OmniverseKit_Persp",
    )

    # timeline을 재생 상태로 바꿔야 PhysX articulation이 움직인다.
    app_utils.play()
    # 첫 update에서 physics backend와 articulation view가 초기화된다.
    simulation_app.update()

    # DOF는 degree of freedom이다. Franka는 팔 7개 + gripper finger 2개로 보통 9개가 나온다.
    print("DOF names:")
    for index, name in enumerate(robot.dof_names):
        print(f"  {index}: {name}")

    # 각 리스트는 robot.dof_names 순서에 맞춘 joint position target이다.
    # 단위는 revolute joint는 rad, prismatic/finger joint는 meter 계열로 보면 된다.
    home = [0.0, -0.4, 0.0, -2.2, 0.0, 2.0, 0.8, 0.04, 0.04]
    reach_left = [0.4, -0.7, 0.2, -2.0, 0.0, 1.6, 1.0, 0.04, 0.04]
    reach_right = [-0.4, -0.7, -0.2, -2.0, 0.0, 1.6, 1.0, 0.02, 0.02]

    targets = [home, reach_left, reach_right, home]
    hold_steps = 120 if not args.test else 20

    for cycle, target in enumerate(targets):
        print(f"target cycle: {cycle}")
        # joint drive의 목표 위치를 보낸다. 한 번 보낸 target을 향해 PhysX가 계속 따라간다.
        robot.set_dof_position_targets(target)

        for step in range(hold_steps):
            # 한 프레임 진행한다. GUI 모드에서는 렌더링도 함께 업데이트된다.
            simulation_app.update()

            if step % 40 == 0:
                # 현재 joint position을 읽어 target으로 수렴하는지 확인한다.
                print("  joint positions:", robot.get_dof_positions())


if __name__ == "__main__":
    try:
        main()
    finally:
        # 예외가 나도 timeline과 SimulationApp을 정리해서 다음 실행이 꼬이지 않게 한다.
        app_utils.stop()
        simulation_app.close()
