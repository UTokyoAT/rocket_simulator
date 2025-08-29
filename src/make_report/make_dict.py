from dataclasses import dataclass

import japanize_matplotlib  # noqa: F401
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from matplotlib.figure import Figure

from src.geography.launch_site import LaunchSite

from .result_for_report import ResultByLauncherElevation, ResultByWindSpeed, ResultForReport, SimulationContext


def velocity_norm(row) -> float:
    return (row.velocity_n**2 + row.velocity_e**2 + row.velocity_d**2) ** 0.5


def acc_norm(row) -> float:
    return (row.acceleration_body_frame_x**2 + row.acceleration_body_frame_y**2 + row.acceleration_body_frame_z**2) ** 0.5


def air_velocity_norm(row) -> float:
    return (
        row.velocity_air_body_frame_x**2 + row.velocity_air_body_frame_y**2 + row.velocity_air_body_frame_z**2
    ) ** 0.5


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