from dataclasses import dataclass

import pandas as pd

from src.util.type import NPVector


@dataclass
class WindPowerLow:
    reference_height: float
    wind_speed: float
    exponent: float
    wind_direction: float


@dataclass
class Config:
    mass: pd.DataFrame
    wind: WindPowerLow
    thrust: pd.DataFrame
    CA: float
    CN_alpha: float
    body_area: float
    wind_center: NPVector
    dt: float
    launcher_length: float
    inertia_tensor_xx: float
    inertia_tensor_yy: float
    inertia_tensor_zz: float
    inertia_tensor_zy: float
    inertia_tensor_xz: float
    inertia_tensor_xy: float
    first_elevation: float
    first_azimuth: float
    first_roll: float
    parachute_terminal_velocity: float
    parachute_delay_time: float
    first_gravity_center: NPVector
    end_gravity_center: NPVector
    length: float
