from pathlib import Path

import mujoco
import numpy as np


XML_PATH = Path(__file__).with_name("simple_pendulum.xml")


def main() -> None:
    model = mujoco.MjModel.from_xml_path(str(XML_PATH))
    data = mujoco.MjData(model)

    print("Loaded XML:", XML_PATH)
    print("joint names:", [mujoco.mj_id2name(model, mujoco.mjtObj.mjOBJ_JOINT, i) for i in range(model.njnt)])
    print("actuator names:", [mujoco.mj_id2name(model, mujoco.mjtObj.mjOBJ_ACTUATOR, i) for i in range(model.nu)])
    print("site names:", [mujoco.mj_id2name(model, mujoco.mjtObj.mjOBJ_SITE, i) for i in range(model.nsite)])

    data.qpos[0] = np.deg2rad(20.0)
    mujoco.mj_forward(model, data)

    print("\nstep, hinge_angle_deg, hinge_velocity, tip_position")
    for step in range(200):
        if step < 80:
            data.ctrl[0] = 0.3
        elif step < 140:
            data.ctrl[0] = -0.3
        else:
            data.ctrl[0] = 0.0

        mujoco.mj_step(model, data)

        if step % 20 == 0:
            hinge_angle_deg = np.rad2deg(data.qpos[0])
            hinge_velocity = data.qvel[0]
            tip_position = data.site_xpos[0].copy()
            print(
                f"{step:3d}, "
                f"{hinge_angle_deg:8.3f}, "
                f"{hinge_velocity:8.3f}, "
                f"{tip_position}"
            )


if __name__ == "__main__":
    main()
