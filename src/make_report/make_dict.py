import math

import numpy as np
import pandas as pd

from src.core.config import Config
from src.geography.geography import Point
from src.geography.launch_site import LaunchSite

from .result_for_report import ResultForReport, SimulationContext


def burning_coasting_division(data: pd.DataFrame) -> pd.DataFrame:
    burning = data[data["burning"]]
    coasting = data[~data["burning"]]
    return burning, coasting

def launch_clear(data: pd.DataFrame, context: SimulationContext) -> dict:
    """ランチクリア時の情報"""
    launch_clear = data[~data["on_launcher"]].iloc[0]
    v = (launch_clear.velocity_n**2 + launch_clear.velocity_e**2 + launch_clear.velocity_d**2) ** 0.5
    theta = np.deg2rad(context.first_elevation)
    alpha = np.deg2rad(21)
    beta = np.deg2rad(20)
    w_alpha = v * np.tan(alpha) / (np.sin(theta) + np.cos(theta) * np.tan(alpha))
    w_beta = v * np.tan(beta)
    return {
        "時刻/s": round(launch_clear.time, 2),
        "速度/(m/s)": round(v, 2),
        "順風迎角21degの時の風速/(m/s)": round(w_alpha, 2),
        "側風迎角20degの時の風速/(m/s)": round(w_beta, 2),
        "風速制限/(m/s)": round(min(w_alpha, w_beta), 2),
    }

def dynamic_pressure(data: pd.DataFrame, *, through_all_time: bool) -> dict:
    burning = data[data["burning"]]
    if through_all_time:
        pressure_max = data.loc[data["dynamic_pressure"].idxmax()]
    else:
        pressure_max = burning.loc[burning["dynamic_pressure"].idxmax()]
    air_velocity_norm = (
        pressure_max.velocity_air_body_frame_x**2
        + pressure_max.velocity_air_body_frame_y**2
        + pressure_max.velocity_air_body_frame_z**2) ** 0.5
    return {
        "時刻/s": round(pressure_max.time, 2),
        "高度/m": round(-(pressure_max.position_d), 2),
        "動圧/kPa": round(pressure_max.dynamic_pressure / 1000, 2),
        "対気速度/(m/s)": round(air_velocity_norm, 2),
    }

def max_altitude(data: pd.DataFrame) -> dict:
    max_altitude = data.loc[data["position_d"].idxmin()]
    velocity_air = np.sqrt(max_altitude.velocity_n**2
                          + max_altitude.velocity_e**2
                          + max_altitude.velocity_d**2)
    return {
        "時刻/s": round(max_altitude.time, 2),
        "高度/m": round(-(max_altitude.position_d), 2),
        "対気速度/(m/s)": round(velocity_air, 2),
    }

def landing(data: pd.DataFrame, site: LaunchSite) -> dict:
    landing = data.iloc[-1]
    landing_position = Point.from_north_east(landing.position_n, landing.position_e,
                              site.launch_point.latitude, site.launch_point.longitude)
    return {
        "時刻/s": round(landing.time, 2),
        "着地点緯度": landing_position.latitude,
        "着地点経度": landing_position.longitude,
        "ダウンレンジ/m": round(
            math.sqrt(landing.position_n**2 + landing.position_e**2),
            2,
        ),
    }

def _stability(config: Config) -> tuple[float, float]:
    length = config.length
    wind_center = config.wind_center[0]
    cg_first = config.first_gravity_center[0]
    cg_end = config.end_gravity_center[0]
    first_stability = (cg_first - wind_center) / length * 100
    end_stability = (cg_end - wind_center) / length * 100
    return first_stability, end_stability


def stability(config: Config) ->dict:
    first_stability, end_stability = _stability(config)
    return {
        "最小値/%": round(min(first_stability, end_stability), 2),
        "最大値/%": round(max(first_stability, end_stability), 2),
    }

def acceleration(data: pd.DataFrame) ->dict:
    acc_norm = np.sqrt(data["acceleration_body_frame_x"]**2
                + data["acceleration_body_frame_y"]**2
                + data["acceleration_body_frame_z"]**2)
    max_idx = acc_norm.idxmax()    #acc_normが最大のインデックス
    max_acc = data.loc[max_idx]  #acc_normが最大の行のデータを取得
    return {
        "時刻/s": round(max_acc.time, 2),
        "最大加速度/(m/s^2)": round(acc_norm[max_idx], 2),
        "高度/m": round(-(max_acc.position_d), 2),
    }

def make_dict(result: ResultForReport, site: LaunchSite, config: Config) -> dict:
    ideal_launch_clear = launch_clear(result.result_ideal_parachute_off, result.context_nominal)
    ideal_dynamic_pressure = dynamic_pressure(result.result_ideal_parachute_off, all=False)
    ideal_max_altitude = max_altitude(result.result_ideal_parachute_off)
    ideal_landing = landing(result.result_ideal_parachute_off, site)
    ideal_acceleration = acceleration(result.result_ideal_parachute_off)
    nominal_launch_clear = launch_clear(result.result_nominal_parachute_off, result.context_nominal)
    nominal_dynamic_pressure = dynamic_pressure(result.result_nominal_parachute_off, through_all_time=False)
    nominal_max_altitude = max_altitude(result.result_nominal_parachute_off)
    nominal_landing = landing(result.result_nominal_parachute_off, site)
    nominal_stability = stability(config)
    nominal_acceleration = acceleration(result.result_nominal_parachute_off)

    return {
    "ideal_launch_clear": ideal_launch_clear,
    "ideal_dynamic_pressure": ideal_dynamic_pressure,
    "ideal_max_altitude": ideal_max_altitude,
    "ideal_landing": ideal_landing,
    "ideal_acceleration": ideal_acceleration,
    "nominal_launch_clear": nominal_launch_clear,
    "nominal_dynamic_pressure": nominal_dynamic_pressure,
    "nominal_max_altitude": nominal_max_altitude,
    "nominal_landing": nominal_landing,
    "nominal_stability": nominal_stability,
    "nominal_acceleration": nominal_acceleration,
    }
