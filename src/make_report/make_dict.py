from dataclasses import dataclass

import japanize_matplotlib  # noqa: F401
import numpy as np
import pandas as pd
import math
from matplotlib import pyplot as plt
from matplotlib.figure import Figure

from src.geography.launch_site import LaunchSite
from src.geography.geography import Point
from .result_for_report import ResultByLauncherElevation, ResultByWindSpeed, ResultForReport, SimulationContext


def velocity_norm(row) -> float:
    return (row.velocity_n**2 + row.velocity_e**2 + row.velocity_d**2) ** 0.5


def acc_norm(row) -> float:
    return (row.acceleration_body_frame_x**2 + row.acceleration_body_frame_y**2 + row.acceleration_body_frame_z**2) ** 0.5


def air_velocity_norm(row) -> float:
    return (
        row.velocity_air_body_frame_x**2 + row.velocity_air_body_frame_y**2 + row.velocity_air_body_frame_z**2
    ) ** 0.5

def burning_coasting_division(data: pd.DataFrame) -> pd.DataFrame:
    burning = data[data["burning"]]
    coasting = data[~data["burning"]]
    return burning, coasting

def launch_clear(data: pd.DataFrame) -> dict:
    """ランチクリア時の情報"""

    launch_clear = data[~data["on_launcher"]].iloc[0]
    v = (launch_clear.velocity_n**2 + launch_clear.velocity_e**2 + launch_clear.velocity_d**2) ** 0.5
    theta = np.deg2rad(SimulationContext.first_elevation)
    alpha = np.deg2rad(21)
    beta = np.deg2rad(20)
    w_alpha = v * np.tan(alpha) / (np.sin(theta) + np.cos(theta) * np.tan(alpha))
    w_beta = v * np.tan(beta)
    if v < 15:
        print("ランチクリア速度が遅すぎます.打ち上げできません")
    return {
        "時刻/s": round(launch_clear.time, 2),
        "速度/(m/s)": round(v, 2),
        "順風迎角21degの時の風速/(m/s)": round(w_alpha, 2),
        "側風迎角20degの時の風速/(m/s)": round(w_beta, 2),
        "風速制限/(m/s)": round(min(w_alpha, w_beta), 2),
    }

def dynamic_pressure(data: pd.DataFrame, all=False) -> dict:
    burning = data[data["burning"]]
    if all:
        pressure_max = data.loc[data["dynamic_pressure"].idxmax()]  #燃料を噴射している最中の圧力の最大値
    else:
        pressure_max = burning.loc[burning["dynamic_pressure"].idxmax()]
    air_velocity_norm = (
        pressure_max.velosity_air_body_frame_x**2
        + pressure_max.velosity_air_body_frame_y**2
        + pressure_max.velosity_air_body_frame_z**2) ** 0.5
    return {
        "時刻/s": round(pressure_max.time, 2),
        "高度/m": round(pressure_max.position_d, 2),
        "動圧/kPa": round(pressure_max.dynamic_pressure / 1000, 2),
        "対気速度/(m/s)": round(air_velocity_norm, 2),
    }

def max_altitude(data: pd.DataFrame) -> dict:
    print("最高高度")
    max_altitude = data.loc[data["position_d"].idxmin()]
    print(
        f"t={max_altitude.time}s,altitude={-(max_altitude.altitude)}m,velocity_air={air_velocity_norm(max_altitude)}m/s"
    )
    return {
        "時刻/s": round(max_altitude.time, 2),
        "高度/m": round(max_altitude.altitude, 2),
        "対気速度/(m/s)": round(air_velocity_norm(max_altitude), 2),
    }

def landing(data: pd.DataFrame, site: LaunchSite) -> dict:
    landing = data.iloc[-1]
    print("着地")
    print(
        f"t={landing.time}s, downrange={math.sqrt(landing.position_n**2 + landing.position_e**2)}m"
    )
    p = Point.from_north_east(landing.position_n, landing.position_e,
                              site.launch_point.latitude, site.launch_point.longitude)
    return {
        "時刻/s": round(landing.time, 2),
        "着地点緯度": p.latitude,
        "着地点経度": p.longitude,
        "ダウンレンジ/m": round(
            math.sqrt(landing.position_n**2 + landing.position_e**2),
            2,
        ),
    }


def make_dict(result: ResultForReport, site: LaunchSite) -> dict:
    ideal_launch_clear = launch_clear(result.result_ideal_parachute_off)
    ideal_dynamic_pressure = dynamic_pressure(result.result_ideal_parachute_off)
    ideal_max_altitude = max_altitude(result.result_ideal_parachute_off)
    ideal_landing = landing(result.result_ideal_parachute_off, site)

    nominal_launch_clear = launch_clear(result.result_nominal_parachute_off)
    nominal_dynamic_pressure = dynamic_pressure(result.result_nominal_parachute_off)
    nominal_max_altitude = max_altitude(result.result_nominal_parachute_off)
    nominal_landing = landing(result.result_nominal_parachute_off, site)

    text = dict(**ideal_launch_clear,
                **ideal_dynamic_pressure,
                **ideal_max_altitude,
                **ideal_landing,

                **nominal_launch_clear,
                **nominal_dynamic_pressure,
                **nominal_max_altitude,
                **nominal_landing,
                )
    return text
