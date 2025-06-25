import numpy as np
import quaternion as quart  # ty: ignore


def square_norm(q: quart.quaternion) -> float:
    """クォータニオンのノルムの二乗を計算する

    Args:
        q (quart.quaternion): クォータニオン

    Returns:
        float: クォータニオンのノルムの二乗
    """
    return q.w**2 + q.x**2 + q.y**2 + q.z**2


def quaternion_derivative(
    q: quart.quaternion,
    angular_velocity: np.ndarray,
) -> quart.quaternion:
    """クォータニオンの時間微分を計算する

    Args:
        q (quart.quaternion): クォータニオン
        angular_velocity (np.ndarray): 剛体系での角速度

    Returns:
        quart.quaternion: クォータニオンの時間微分
    """
    return 0.5 * q * quart.quaternion(0, *angular_velocity)


def inertial_to_body(q: quart.quaternion, v: np.ndarray) -> np.ndarray:
    """慣性系から剛体系への座標変換を行う

    Args:
        q (quart.quaternion): クォータニオン
        v (np.ndarray): 慣性系でのベクトル

    Returns:
        np.ndarray: 剛体系でのベクトル
    """
    return (q.conj() * quart.quaternion(0, *v) * q).vec / square_norm(q)


def body_to_inertial(q: quart.quaternion, v: np.ndarray) -> np.ndarray:
    """剛体系から慣性系への座標変換を行う

    Args:
        q (quart.quaternion): クォータニオン
        v (np.ndarray): 剛体系でのベクトル

    Returns:
        np.ndarray: 慣性系でのベクトル
    """
    return (q * quart.quaternion(0, *v) * q.conj()).vec / square_norm(q)


def from_euler_angle(elevation: float, azimuth: float, roll: float) -> quart.quaternion:
    """オイラー角からクォータニオンを生成する

    Args:
        elevation (float): 仰角[deg]
        azimuth (float): 方位角[deg]
        roll (float): ロール角[deg]

    Returns:
        quart.quaternion: クォータニオン
    """
    max_elevation = 90
    max_azimuth = 360
    max_roll = 360
    if not (0 <= elevation <= max_elevation):
        err_msg = f"仰角は0から{max_elevation}の範囲内である必要があります"
        raise ValueError(err_msg)
    if not (0 <= azimuth <= max_azimuth):
        err_msg = f"方位角は0から{max_azimuth}の範囲内である必要があります"
        raise ValueError(err_msg)
    if not (0 <= roll <= max_roll):
        err_msg = f"ロール角は0から{max_roll}の範囲内である必要があります"
        raise ValueError(err_msg)
    elevation_rad = np.deg2rad(elevation)
    azimuth_rad = np.deg2rad(azimuth)
    roll_rad = np.deg2rad(roll)
    azimuth_rotate = quart.quaternion(
        np.cos(azimuth_rad / 2),
        0,
        0,
        np.sin(azimuth_rad / 2),
    )
    elevation_rotate = quart.quaternion(
        np.cos(elevation_rad / 2),
        0,
        np.sin(elevation_rad / 2),
        0,
    )
    roll_rotate = quart.quaternion(np.cos(roll_rad / 2), np.sin(roll_rad / 2), 0, 0)
    return azimuth_rotate * elevation_rotate * roll_rotate


def sum_vector_inertial_frame(
    vectors_body_frame: list[np.ndarray],
    vectors_inertial_frame: list[np.ndarray],
    posture: quart.quaternion,
) -> np.ndarray:
    """剛体座標系でのベクトルと慣性座標系でのベクトルを合成して慣性座標系でのベクトルを返す

    Args:
        vectors_body_frame (list[np.ndarray]): 機体座標系でのベクトル
        vectors_inertial_frame (list[np.ndarray]): 慣性系でのベクトル
        posture (quart.quaternion): 機体の姿勢

    Returns:
        np.ndarray: 慣性系でのベクトルの和
    """
    vectors_body_frame_sum = np.sum(vectors_body_frame, axis=0)
    vectors_inertial_frame_sum = np.sum(vectors_inertial_frame, axis=0)
    return vectors_inertial_frame_sum + body_to_inertial(
        posture,
        vectors_body_frame_sum,
    )


def sum_vector_body_frame(
    vectos_body_frame: list[np.ndarray],
    vectors_inertial_frame: list[np.ndarray],
    posture: quart.quaternion,
) -> np.ndarray:
    """慣性座標系でのベクトルと機体座標系でのベクトルを合成して機体座標系でのベクトルを返す

    Args:
        vectos_body_frame (list[np.ndarray]): 機体座標系でのベクトル
        vectors_inertial_frame (list[np.ndarray]): 慣性系でのベクトル
        posture (quart.quaternion): 機体の姿勢

    Returns:
        np.ndarray: 機体座標系でのベクトルの和
    """
    vectors_body_frame_sum = np.sum(vectos_body_frame, axis=0)
    vectors_inertial_frame_sum = np.sum(vectors_inertial_frame, axis=0)
    return vectors_body_frame_sum + inertial_to_body(
        posture,
        vectors_inertial_frame_sum,
    )
