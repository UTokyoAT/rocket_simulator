import numpy as np
from dataclasses import dataclass
from .rocket_state import RocketState
from .simulation_context import SimulationContext
from . import quaternion_util


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
    if normal_velocity_norm < 1e-4:  # ０除算を防ぐ
        return np.array([0, 0, 0])
    p = dynamic_pressure(airspeed, air_density)
    direction = np.array([0, -airspeed[1], -airspeed[2]]) / normal_velocity_norm
    return p * body_area * normal_force_coefficient * direction


def angle_of_attack(airspeed: np.ndarray) -> float:
    """迎角を計算する

    Args:
        airspeed (np.ndarray): 剛体系での機体速度

    Returns:
        float: 迎角[rad]（速度ベクトルと機体軸とのなす角度）
    """
    return np.arctan2(np.linalg.norm(airspeed[1:], ord=2), airspeed[0])


def air_dumping_moment(
    rotation: np.ndarray,
    roll_damping_coefficient: float,
    pitch_damping_coefficient: float,
    yaw_damping_coefficient: float,
    air_velocity: np.ndarray,
    overall_length: float,
    air_density: float,
    body_area: float,
) -> np.ndarray:
    """空気抵抗によるモーメントを計算する

    Args:
        rotation (np.ndarray): 機体の角速度
        roll_damping_coefficient (float): ロール軸周りの空気抵抗係数
        pitch_damping_coefficient (float): ピッチ軸周りの空気抵抗係数
        yaw_damping_coefficient (float): ヨー軸周りの空気抵抗係数
        air_velocity (np.ndarray): 剛体系での機体速度
        overall_length (float): 機体の全長
        air_density (float): 空気密度
        body_area (float): 断面積

    Returns:
        np.ndarray: 空気抵抗によるモーメント
    """
    p = dynamic_pressure(air_velocity, air_density)
    return (
        p
        * body_area
        * overall_length**2
        / 2
        / np.linalg.norm(air_velocity, ord=2)
        * np.array(
            [
                roll_damping_coefficient,
                pitch_damping_coefficient,
                yaw_damping_coefficient,
            ]
        )
        * rotation
    )


def air_force_moment(force: np.ndarray, wind_center: np.ndarray) -> np.ndarray:
    """力のモーメントを計算する

    Args:
        force (np.ndarray): 剛体系での力
        wind_center (np.ndarray): 重心から見た風圧中心

    Returns:
        np.ndarray: モーメント
    """
    return np.cross(wind_center, force)


def normal_force_coefficient(angle_of_attack: float, CN_alpha) -> float:
    """法線方向の力係数を計算する

    Args:
        angle_of_attack (float): 迎角[rad]
        CN_alpha (float): 法線方向の力係数の迎角に対する傾き

    Returns:
        float: 法線方向の力係数
    """
    return CN_alpha * angle_of_attack


def calculate(rocket_state: RocketState, context: SimulationContext) -> AirForceResult:
    """空気力を計算する

    Args:
        rocket_state (RocketState): ロケットの状態
        context (SimulationContext): ロケットの設定

    Returns:
        AirForceResult: 空気力の計算結果
    """
    z = -rocket_state.position[2]
    velocity_air_body_frame = rocket_state.velocity - context.wind(z)
    airspeed = quaternion_util.inertial_to_body(
        rocket_state.posture,
        velocity_air_body_frame,
    )
    angle_of_attack_ = angle_of_attack(airspeed)
    AIR_DENSITY = 1.204
    axial_force_ = axial_force(
        airspeed,
        AIR_DENSITY,
        context.body_area,
        context.CA,
    )
    CN = normal_force_coefficient(angle_of_attack_, context.CN_alpha)
    normal_force_ = normal_force(
        airspeed,
        AIR_DENSITY,
        context.body_area,
        CN,
    )
    air_force = axial_force_ + normal_force_
    moment = air_force_moment(air_force, context.wind_center)
    dynamic_pressure_ = dynamic_pressure(airspeed, AIR_DENSITY)
    return AirForceResult(
        force=air_force,
        moment=moment,
        dynamic_pressure=dynamic_pressure_,
        velocity_air_body_frame=velocity_air_body_frame,
    )
