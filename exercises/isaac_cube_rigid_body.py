from __future__ import annotations

import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--headless", action="store_true")
parser.add_argument("--test", action="store_true")
args, _ = parser.parse_known_args()

from isaacsim import SimulationApp

# Isaac Sim의 extension/runtime을 먼저 띄워야 아래 isaacsim.* API를 import할 수 있다.
simulation_app = SimulationApp({"headless": args.headless})

import isaacsim.core.experimental.utils.app as app_utils
import isaacsim.core.experimental.utils.stage as stage_utils
from isaacsim.core.experimental.materials import PreviewSurfaceMaterial
from isaacsim.core.experimental.objects import Cube, DistantLight, GroundPlane
from isaacsim.core.experimental.prims import GeomPrim, RigidPrim
from isaacsim.core.utils.viewports import set_camera_view


def main() -> None:
    # 빈 USD stage를 새로 만든다. GUI에서 File > New를 누르는 것과 비슷하다.
    stage_utils.create_new_stage()

    # 물체가 떨어져 충돌할 바닥을 만든다.
    GroundPlane("/World/GroundPlane", positions=[0.0, 0.0, 0.0])

    # 조명이 없으면 물체가 어둡게 보이므로 기본 directional light를 추가한다.
    light = DistantLight("/World/DistantLight")
    light.set_intensities(500)

    # Cube에 입힐 간단한 파란색 preview material을 만든다.
    material = PreviewSurfaceMaterial("/World/Looks/blue")
    material.set_input_values("diffuseColor", [0.1, 0.45, 1.0])

    # 시각적으로 보이는 Cube prim을 만든다. 아직 물리 body는 아니다.
    cube_shape = Cube(
        paths="/World/DynamicCube",
        positions=[0.0, 0.0, 2.0],
        sizes=1.0,
        scales=[0.4, 0.4, 0.4],
    )
    cube_shape.apply_visual_materials(material)

    # 같은 prim path를 RigidPrim으로 감싸면 rigid body API가 적용된다.
    cube = RigidPrim(paths="/World/DynamicCube", masses=1.0)
    # collider가 있어야 바닥과 충돌한다. Rigid body만 있으면 물리 충돌이 빠질 수 있다.
    GeomPrim(paths="/World/DynamicCube", apply_collision_apis=True)

    # GUI 실행 시 Cube와 바닥이 바로 보이도록 viewport 카메라 위치를 잡는다.
    set_camera_view(
        eye=[3.0, -4.0, 2.5],
        target=[0.0, 0.0, 0.7],
        camera_prim_path="/OmniverseKit_Persp",
    )

    # timeline을 재생 상태로 바꿔야 PhysX simulation이 진행된다.
    app_utils.play()
    # 첫 update에서 physics backend와 prim view들이 초기화된다.
    simulation_app.update()

    # 초기 속도를 준다. linear는 m/s, angular는 rad/s로 생각하면 된다.
    cube.set_velocities(linear_velocities=[0.8, 0.0, 0.0], angular_velocities=[0.0, 0.0, 2.0])

    max_steps = 180 if not args.test else 20
    for step in range(max_steps):
        if step == 60:
            # 60 step 뒤 Cube를 다시 공중으로 옮기고 회전/이동 속도를 바꾼다.
            cube.set_world_poses(
                positions=[[0.0, 0.0, 2.5]],
                orientations=[[1.0, 0.0, 0.0, 0.0]],
            )
            cube.set_velocities(linear_velocities=[[0.0, 1.2, 0.0]], angular_velocities=[[0.0, 0.0, 4.0]])

        # 한 프레임 진행한다. GUI 모드에서는 렌더링도 함께 업데이트된다.
        simulation_app.update()

        if step % 30 == 0:
            # pose와 velocity를 읽어서 콘솔에 출력한다.
            positions, orientations = cube.get_world_poses()
            linear_velocities, angular_velocities = cube.get_velocities()
            print(f"step: {step}")
            print(f"  position: {positions}")
            print(f"  orientation: {orientations}")
            print(f"  linear velocity: {linear_velocities}")
            print(f"  angular velocity: {angular_velocities}")


if __name__ == "__main__":
    try:
        main()
    finally:
        # 예외가 나도 timeline과 SimulationApp을 정리해서 다음 실행이 꼬이지 않게 한다.
        app_utils.stop()
        simulation_app.close()
