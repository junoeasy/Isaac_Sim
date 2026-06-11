from __future__ import annotations

import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--headless", action="store_true")
parser.add_argument("--test", action="store_true")
args, _ = parser.parse_known_args()

from isaacsim import SimulationApp

simulation_app = SimulationApp({"headless": args.headless})

import isaacsim.core.experimental.utils.app as app_utils
import isaacsim.core.experimental.utils.stage as stage_utils
from isaacsim.core.experimental.materials import PreviewSurfaceMaterial
from isaacsim.core.experimental.objects import Cube, DistantLight, GroundPlane
from isaacsim.core.experimental.prims import GeomPrim, RigidPrim
from isaacsim.core.utils.viewports import set_camera_view


def main() -> None:
    stage_utils.create_new_stage()

    GroundPlane("/World/GroundPlane", positions=[0.0, 0.0, 0.0])

    light = DistantLight("/World/DistantLight")
    light.set_intensities(500)

    material = PreviewSurfaceMaterial("/World/Looks/blue")
    material.set_input_values("diffuseColor", [0.1, 0.45, 1.0])

    cube_shape = Cube(
        paths="/World/DynamicCube",
        positions=[0.0, 0.0, 2.0],
        sizes=1.0,
        scales=[0.4, 0.4, 0.4],
    )
    cube_shape.apply_visual_materials(material)

    cube = RigidPrim(paths="/World/DynamicCube", masses=1.0)
    GeomPrim(paths="/World/DynamicCube", apply_collision_apis=True)

    set_camera_view(
        eye=[3.0, -4.0, 2.5],
        target=[0.0, 0.0, 0.7],
        camera_prim_path="/OmniverseKit_Persp",
    )

    app_utils.play()
    simulation_app.update()

    cube.set_velocities(linear_velocities=[0.8, 0.0, 0.0], angular_velocities=[0.0, 0.0, 2.0])

    max_steps = 180 if not args.test else 20
    for step in range(max_steps):
        if step == 60:
            cube.set_world_poses(
                positions=[[0.0, 0.0, 2.5]],
                orientations=[[1.0, 0.0, 0.0, 0.0]],
            )
            cube.set_velocities(linear_velocities=[[0.0, 1.2, 0.0]], angular_velocities=[[0.0, 0.0, 4.0]])

        simulation_app.update()

        if step % 30 == 0:
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
        app_utils.stop()
        simulation_app.close()
