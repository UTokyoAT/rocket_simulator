import typing

import numpy as np

from . import gravity_center, interpolation, wind
from .config import Config
from .inertia_tensor import InertiaTensor


class SimulationContext:
    mass: typing.Callable[[float], float]
    """時間->質量"""
    wind: typing.Callable[[float], np.ndarray]
    """高度->風速ベクトル"""
    thrust: typing.Callable[[float], float]
    """時間->推力"""
    gravity_center: typing.Callable[[float], np.ndarray]
    """時間->重心位置"""
    CA: float
    """軸力係数"""
    CN_alpha: float
    """単位なす角あたりの法線力係数"""
    body_area: float
    """断面積"""
    wind_center: np.ndarray
    """風圧中心"""
    dt: float
    """時間刻み"""
    launcher_length: float
    """ランチャーの長さ"""
    inertia_tensor: InertiaTensor
    """慣性テンソル"""
    first_elevation: float
    """初期迎角"""
    first_azimuth: float
    """初期方位角"""
    first_roll: float
    """初期ロール角"""
    parachute_terminal_velocity: float
    """パラシュートの終端速度"""
    parachute_delay_time: float
    """最高高度到達からパラシュート展開までの時間"""

    def __init__(self, config: Config) -> None:
        self.mass = interpolation.df_to_function_1d(config.mass)
        self.wind = wind.wind_velocity_power(
            config.wind.reference_height,
            config.wind.wind_speed,
            config.wind.exponent,
            config.wind.wind_direction,
        )
        self.thrust = interpolation.df_to_function_1d(config.thrust)
        self.gravity_center = (
            gravity_center.create_gravity_center_function_from_dataframe(
                config.first_gravity_center,
                config.end_gravity_center,
                config.thrust,
            )
        )
        self.CA = config.CA
        self.CN_alpha = config.CN_alpha
        self.body_area = config.body_area
        self.wind_center = config.wind_center
        self.dt = config.dt
        self.launcher_length = config.launcher_length
        self.inertia_tensor = InertiaTensor(
            config.inertia_tensor_xx,
            config.inertia_tensor_yy,
            config.inertia_tensor_zz,
            config.inertia_tensor_xy,
            config.inertia_tensor_zy,
            config.inertia_tensor_xz,
        )
        self.first_elevation = config.first_elevation
        self.first_azimuth = config.first_azimuth
        self.first_roll = config.first_roll

        self.parachute_terminal_velocity = config.parachute_terminal_velocity
        self.parachute_delay_time = config.parachute_delay_time
