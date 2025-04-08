import typing
import numpy as np
from .inertia_tensor import InertiaTensor
from .config import Config
from . import interpolation
from . import wind


class SimulationContext:
    mass: typing.Callable[[float], float]
    """時間->質量"""
    wind: typing.Callable[[float], np.ndarray]
    """高度->風速ベクトル"""
    thrust: typing.Callable[[float], float]
    """時間->推力"""
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

    def __init__(self, config: Config):
        self.mass = interpolation.df_to_function_1d(config.mass)
        self.wind = wind.wind_velocity_power(
            config.wind.reference_height,
            config.wind.wind_speed,
            config.wind.exponent,
            config.wind.wind_direction,
        )
        self.thrust = interpolation.df_to_function_1d(config.thrust)
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
