from dataclasses import dataclass

import numpy as np

from . import quaternion_util
from .rocket_state import RocketState
from .simulation_context import SimulationContext


@dataclass
class AirForceResult:
    """空気力の計算結果を表すクラス"""

    force: np.ndarray
    """剛体系での力"""

    moment: np.ndarray
    """剛体系でのモーメント"""

    dynamic_pressure: float
    """動圧"""

    velocity_air_body_frame: np.ndarray
    """剛体系での対気速度"""


def dynamic_pressure(airspeed: np.ndarray, air_density: float) -> float:
    """動圧を計算する

    Args:
        airspeed (np.ndarray): 剛体系での機体速度
        air_density (float): 空気密度

    Returns:
        float: 動圧
    """
    return 0.5 * air_density * sum(airspeed**2)


def axial_force(
    airspeed: np.ndarray,
    air_density: float,
    body_area: float,
    axial_force_coefficient: float,
) -> np.ndarray:
    """軸方向の力を計算する

    Args:
        airspeed (np.ndarray): 剛体系での機体の対気速度
        air_density (float): 空気密度
        body_area (float): 断面積
        axial_force_coefficient (float): 軸方向の力係数CA

    Returns:
        float: 軸方向の力
    """
    p = dynamic_pressure(airspeed, air_density)
    return np.array([-p * body_area * axial_force_coefficient, 0, 0])


def normal_force(
    airspeed: np.ndarray,
    air_density: float,
    body_area: float,
    normal_force_coefficient: float,
) -> np.ndarray:
    """法線方向の力を計算する

    Args:
        airspeed (np.ndarray): 剛体系での機体の対気速度
        air_density (float): 空気密度
        body_area (float): 断面積
        normal_force_coefficient (float): 法線方向の力係数CN

    Returns:
        float: 法線方向の力
    """
    normal_velocity_norm = (airspeed[1] ** 2 + airspeed[2] ** 2) ** 0.5
    zero_division_threshold = 1e-4
    if normal_velocity_norm < zero_division_threshold:
        return np.array([0, 0, 0])
    p = dynamic_pressure(airspeed, air_density)
    direction = np.array([0, -airspeed[1], -airspeed[2]]) / normal_velocity_norm
    return p * body_area * normal_force_coefficient * direction


def angle_of_attack(airspeed: np.ndarray) -> float:
    """迎角を計算する

    Args:
        airspeed (np.ndarray): 剛体系での機体速度

    Returns:
        float: 迎角[rad](速度ベクトルと機体軸とのなす角度)
    """
    return np.arctan2(np.linalg.norm(airspeed[1:], ord=2), airspeed[0])


def air_force_moment(force: np.ndarray, wind_center: np.ndarray) -> np.ndarray:
    """力のモーメントを計算する

    Args:
        force (np.ndarray): 剛体系での力
        wind_center (np.ndarray): 重心から見た風圧中心

    Returns:
        np.ndarray: モーメント
    """
    return np.cross(wind_center, force)


def normal_force_coefficient(angle_of_attack: float, cn_alpha: float) -> float:
    """法線方向の力係数を計算する

    Args:
        angle_of_attack (float): 迎角[rad]
        cn_alpha (float): 法線方向の力係数の迎角に対する傾き

    Returns:
        float: 法線方向の力係数
    """
    return cn_alpha * angle_of_attack


def parachute_force(
    velocity_air: np.ndarray, parachute_terminal_velocity: float, mass: float,
) -> np.ndarray:
    return (
        -9.8
        * mass
        / parachute_terminal_velocity**2
        * np.linalg.norm(velocity_air, ord=2)
        * velocity_air
    )


def calculate(
    rocket_state: RocketState, context: SimulationContext, t: float, *, parachute_on: bool,
) -> AirForceResult:
    """空気力を計算する

    Args:
        rocket_state (RocketState): ロケットの状態
        context (SimulationContext): ロケットの設定
        parachute_on (bool): パラシュートが展開されているかどうか
        t (float): 現在の時刻

    Returns:
        AirForceResult: 空気力の計算結果
    """
    z = -rocket_state.position[2]
    velocity_air_inertial_frame = rocket_state.velocity - context.wind(z)
    velocity_air_body_frame = quaternion_util.inertial_to_body(
        rocket_state.posture,
        velocity_air_inertial_frame,
    )
    angle_of_attack_ = angle_of_attack(velocity_air_body_frame)
    air_density = 1.204
    axial_force_ = axial_force(
        velocity_air_body_frame,
        air_density,
        context.body_area,
        context.CA,
    )
    cn = normal_force_coefficient(angle_of_attack_, context.CN_alpha)
    normal_force_ = normal_force(
        velocity_air_body_frame,
        air_density,
        context.body_area,
        cn,
    )
    if parachute_on:
        air_force = (
            axial_force_
            + normal_force_
            + parachute_force(
                velocity_air_body_frame,
                context.parachute_terminal_velocity,
                context.mass(100),
            )
        )
    else:
        air_force = axial_force_ + normal_force_
    # 重心位置を考慮してモーメントを計算
    gravity_center_pos = context.gravity_center(t)
    # 風圧中心から重心位置へのベクトルを計算
    wind_center_from_gravity = context.wind_center - gravity_center_pos
    moment = air_force_moment(air_force, wind_center_from_gravity)
    dynamic_pressure_ = dynamic_pressure(velocity_air_body_frame, air_density)
    return AirForceResult(
        force=air_force,
        moment=moment,
        dynamic_pressure=dynamic_pressure_,
        velocity_air_body_frame=velocity_air_body_frame,
    )
