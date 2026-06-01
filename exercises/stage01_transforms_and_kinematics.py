from pathlib import Path
import os

os.environ.setdefault("MPLCONFIGDIR", str(Path("/tmp/isaac-sim-study-matplotlib")))
import matplotlib.pyplot as plt
import numpy as np


def transform_2d(x: float, y: float, theta: float) -> np.ndarray:
    """평행이동과 yaw 각도로 2D 동차변환행렬을 만듭니다."""
    c = np.cos(theta)
    s = np.sin(theta)
    return np.array(
        [
            [c, -s, x],
            [s, c, y],
            [0.0, 0.0, 1.0],
        ],
        dtype=float,
    )


def apply_transform(transform: np.ndarray, point_xy: np.ndarray) -> np.ndarray:
    point_h = np.array([point_xy[0], point_xy[1], 1.0], dtype=float)
    result = transform @ point_h
    return result[:2]


def forward_kinematics_2link(q: np.ndarray, link_lengths: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    q1, q2 = q
    l1, l2 = link_lengths

    elbow = np.array([l1 * np.cos(q1), l1 * np.sin(q1)])
    ee = elbow + np.array([l2 * np.cos(q1 + q2), l2 * np.sin(q1 + q2)])
    return elbow, ee


def inverse_kinematics_2link(target: np.ndarray, link_lengths: np.ndarray) -> np.ndarray:
    x, y = target
    l1, l2 = link_lengths
    r2 = x * x + y * y

    cos_q2 = (r2 - l1 * l1 - l2 * l2) / (2.0 * l1 * l2)
    cos_q2 = np.clip(cos_q2, -1.0, 1.0)
    q2 = np.arccos(cos_q2)

    k1 = l1 + l2 * np.cos(q2)
    k2 = l2 * np.sin(q2)
    q1 = np.arctan2(y, x) - np.arctan2(k2, k1)

    return np.array([q1, q2])


def plot_arm(q: np.ndarray, link_lengths: np.ndarray, target: np.ndarray, output_path: Path) -> None:
    elbow, ee = forward_kinematics_2link(q, link_lengths)
    points = np.vstack(([0.0, 0.0], elbow, ee))

    fig, ax = plt.subplots(figsize=(5, 5))
    ax.plot(points[:, 0], points[:, 1], marker="o", linewidth=3, label="2-link arm")
    ax.scatter([target[0]], [target[1]], marker="x", s=100, label="target")
    ax.set_aspect("equal", adjustable="box")
    ax.grid(True)
    ax.set_xlim(-2.2, 2.2)
    ax.set_ylim(-2.2, 2.2)
    ax.legend()
    ax.set_title("Stage 01: 2-link arm IK result")

    output_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output_path, dpi=160)
    plt.close(fig)


def main() -> None:
    robot_in_world = transform_2d(x=1.0, y=2.0, theta=np.deg2rad(90.0))
    point_in_robot = np.array([1.0, 0.0])
    point_in_world = apply_transform(robot_in_world, point_in_robot)

    print("좌표 변환 테스트")
    print("robot frame의 점:", point_in_robot)
    print("world frame으로 변환된 점:", np.round(point_in_world, 4))

    link_lengths = np.array([1.0, 0.8])
    target = np.array([1.2, 0.7])
    q = inverse_kinematics_2link(target, link_lengths)
    elbow, ee = forward_kinematics_2link(q, link_lengths)

    print("\n2-link 로봇팔 역기구학 테스트")
    print("목표점:", target)
    print("joint 각도(rad):", np.round(q, 4))
    print("joint 각도(deg):", np.round(np.rad2deg(q), 2))
    print("팔꿈치 위치:", np.round(elbow, 4))
    print("end-effector 위치:", np.round(ee, 4))
    print("위치 오차:", np.linalg.norm(target - ee))

    output_path = Path("outputs/stage01_2link_arm.png")
    plot_arm(q, link_lengths, target, output_path)
    print("\n저장된 그림:", output_path)


if __name__ == "__main__":
    main()
