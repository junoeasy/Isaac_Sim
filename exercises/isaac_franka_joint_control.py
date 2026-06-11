from __future__ import annotations

import argparse
import sys

parser = argparse.ArgumentParser()
parser.add_argument("--headless", action="store_true")
parser.add_argument("--test", action="store_true")
args, _ = parser.parse_known_args()

from isaacsim import SimulationApp

simulation_app = SimulationApp({"headless": args.headless})

import carb
import isaacsim.core.experimental.utils.app as app_utils
import isaacsim.core.experimental.utils.stage as stage_utils
from isaacsim.core.experimental.objects import DistantLight, GroundPlane
from isaacsim.core.experimental.prims import Articulation, XformPrim
from isaacsim.core.utils.viewports import set_camera_view
from isaacsim.storage.native import get_assets_root_path


def main() -> None:
    assets_root_path = get_assets_root_path()
    if assets_root_path is None:
        carb.log_error("Could not find Isaac Sim assets folder")
        sys.exit(1)

    stage_utils.create_new_stage()
    stage_utils.set_stage_units(meters_per_unit=1.0)

    GroundPlane("/World/GroundPlane", positions=[0.0, 0.0, 0.0])

    light = DistantLight("/World/DistantLight")
    light.set_intensities(500)

    franka_usd = assets_root_path + "/Isaac/Robots/FrankaRobotics/FrankaPanda/franka.usd"
    stage_utils.add_reference_to_stage(usd_path=franka_usd, path="/World/Franka")

    franka_xform = XformPrim("/World/Franka")
    franka_xform.set_world_poses(positions=[0.0, 0.0, 0.0])

    robot = Articulation("/World/Franka")

    set_camera_view(
        eye=[2.8, -3.2, 2.0],
        target=[0.0, 0.0, 0.8],
        camera_prim_path="/OmniverseKit_Persp",
    )

    app_utils.play()
    simulation_app.update()

    print("DOF names:")
    for index, name in enumerate(robot.dof_names):
        print(f"  {index}: {name}")

    home = [0.0, -0.4, 0.0, -2.2, 0.0, 2.0, 0.8, 0.04, 0.04]
    reach_left = [0.4, -0.7, 0.2, -2.0, 0.0, 1.6, 1.0, 0.04, 0.04]
    reach_right = [-0.4, -0.7, -0.2, -2.0, 0.0, 1.6, 1.0, 0.02, 0.02]

    targets = [home, reach_left, reach_right, home]
    hold_steps = 120 if not args.test else 20

    for cycle, target in enumerate(targets):
        print(f"target cycle: {cycle}")
        robot.set_dof_position_targets(target)

        for step in range(hold_steps):
            simulation_app.update()

            if step % 40 == 0:
                print("  joint positions:", robot.get_dof_positions())


if __name__ == "__main__":
    try:
        main()
    finally:
        app_utils.stop()
        simulation_app.close()
