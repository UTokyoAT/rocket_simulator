from dataclasses import dataclass

import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from matplotlib.figure import Figure

from src.core.gravity_center import thrust_end_time
from src.geography.launch_site import LaunchSite

from .result_for_report import ResultForReport, SimulationContext


@dataclass
class Graphs:
    ideal_dynamic_pressure: Figure
    ideal_air_velocity_figure: Figure
    ideal_altitude_downrange_figure: Figure
    ideal_time_altitude_figure: Figure
    ideal_landing_figure: Figure
    ideal_stability_figure: Figure
    ideal_wind_figure: Figure
    ideal_acceleration_figure: Figure
    ideal_rotation_figure: Figure

def burning_coasting_division(data: pd.DataFrame) -> pd.DataFrame:
    burning = data[data["burning"]]
    coasting = data[~data["burning"]]
    return burning, coasting

def dynamic_pressure_figure(data: pd.DataFrame) -> Figure:
    fig, ax = plt.subplots()
    burning, coasting = burning_coasting_division(data)
    fig, ax = plt.subplots()
    ax.plot(burning["time"], burning["dynamic_pressure"], label="burning")
    ax.plot(coasting["time"], coasting["dynamic_pressure"], label="coasting")
    ax.legend()
    ax.set_xlabel("time/s")
    ax.set_ylabel("dynamic pressure/Pa")
    ax.grid(which="both")
    return fig

def air_velocity_figure(data: pd.DataFrame) -> Figure:
    burning, coasting = burning_coasting_division(data)
    fig, ax = plt.subplots()
    ax.plot(burning["time"], burning["velocity_air_body_frame_x"], label="x burning")
    ax.plot(burning["time"], burning["velocity_air_body_frame_y"], label="y burning")
    ax.plot(burning["time"], burning["velocity_air_body_frame_z"], label="z burning")
    ax.plot(coasting["time"], coasting["velocity_air_body_frame_x"], label="x coasting")
    ax.plot(coasting["time"], coasting["velocity_air_body_frame_y"], label="y coasting")
    ax.plot(coasting["time"], coasting["velocity_air_body_frame_z"], label="z coasting")
    ax.legend()
    ax.set_ylabel("velocity/(m/s)")
    ax.set_xlabel("time/s")
    ax.grid(which="both")
    return fig

def time_altitude_figure(data: pd.DataFrame) -> Figure:
    burning, coasting = burning_coasting_division(data)
    fig, ax = plt.subplots()
    ax.plot(burning["time"], -burning["position_d"], label="burning")
    ax.plot(coasting["time"], -coasting["position_d"], label="coasting")
    ax.set_xlabel("time/s")
    ax.set_ylabel("altitude/m")
    ax.legend()
    ax.grid(which="both")
    return fig


def altitude_downrange_figure(data: pd.DataFrame) -> Figure:
    burning, coasting = burning_coasting_division(data)

    def downrange(row: pd.Series) -> float:
        return (row["position_n"]**2 + row["position_e"]**2) ** 0.5

    def altitude(row: pd.Series) -> float:
        return -row["position_d"]

    fig, ax = plt.subplots()
    ax.plot(burning.apply(downrange, axis=1), burning.apply(altitude, axis=1), label="burning")
    ax.plot(coasting.apply(downrange, axis=1), coasting.apply(altitude, axis=1), label="coasting")
    ax.legend()
    ax.set_xlabel("downrange/m")
    ax.set_ylabel("altitude/m")
    ax.grid(which="both")
    return fig

def landing_figure(data: pd.DataFrame, site: LaunchSite) -> Figure:
    fig, ax = plt.subplots()
    ax.plot([*site.points_east(), site.points_east()[0]],
            [*site.points_north(), site.points_north()[0]],
            label="allowed area", linestyle="--", color="gray")
    landing = data.iloc[-1]
    ax.scatter(landing["position_e"], landing["position_n"], label="landing point")
    ax.legend()
    ax.grid(which="both")
    ax.set_xlabel("East/m")
    ax.set_ylabel("North/m")
    return fig

def stability_figure(result: ResultForReport) -> Figure:
    fig, ax = plt.subplots()
    tet = thrust_end_time(result.config.thrust)
    end_time = result.result_ideal_parachute_off["time"].iloc[-1]
    times_burning = np.linspace(0, tet, int(tet/result.config.dt))
    times_coasting = np.linspace(tet, end_time, int((end_time-tet)/result.config.dt))
    # 各時刻における重心位置を取得
    gravity_centers_burning = np.array([result.context.gravity_center(t)[0] for t in times_burning])
    gravity_centers_coasting = np.array([result.context.gravity_center(t)[0] for t in times_coasting])
    wind_center = result.context.wind_center[0]
    length = result.config.length
    # 安定性 = 相対距離（風圧中心 - 重心） / 長さ × 100
    stability_burning = np.array([
    ((gc - wind_center) / length * 100) for gc in gravity_centers_burning
    ])
    stability_coasting = np.array([
    ((gc - wind_center) / length * 100) for gc in gravity_centers_coasting
    ])
    ax.plot(times_burning,  stability_burning, label="burning")
    ax.plot(times_coasting,  stability_coasting, label="coasting")
    ax.legend()
    ax.set_xlabel("time/s")
    ax.set_ylabel("static stability [%]")
    ax.grid(which="both")
    return fig

def wind_figure(context: SimulationContext) -> Figure:
    altitude = np.arange(0, 500, 1)
    # 各高度における風速ベクトルの絶対値（速さ）を計算
    wind_speed = np.array([np.linalg.norm(context.wind(alt)) for alt in altitude])
    fig, ax = plt.subplots()
    ax.plot(altitude, wind_speed)
    ax.set_ylabel("altitude/m")
    ax.set_xlabel("wind speed/m/s")
    ax.grid(which="both")
    return fig

def acceleration_figure(data: pd.DataFrame) -> Figure:
    burning, coasting = burning_coasting_division(data)
    fig, ax = plt.subplots()
    ax.plot(burning["time"], burning["acceleration_body_frame_x"], label="x burning")
    ax.plot(burning["time"], burning["acceleration_body_frame_y"], label="y burning")
    ax.plot(burning["time"], burning["acceleration_body_frame_z"], label="z burning")
    ax.plot(coasting["time"], coasting["acceleration_body_frame_x"], label="x coasting")
    ax.plot(coasting["time"], coasting["acceleration_body_frame_y"], label="y coasting")
    ax.plot(coasting["time"], coasting["acceleration_body_frame_z"], label="z coasting")
    ax.legend()
    ax.set_ylabel("accelaration body flame/(m/s^2)")
    ax.set_xlabel("time/s")
    ax.grid(which="both")
    return fig

def rotation_figure(data: pd.DataFrame) -> Figure:
    burning, coasting = burning_coasting_division(data)
    fig, ax = plt.subplots()
    ax.plot(burning["time"], burning["rotation_n"], label="n burning")
    ax.plot(burning["time"], burning["rotation_e"], label="e burning")
    ax.plot(burning["time"], burning["rotation_d"], label="d burning")
    ax.plot(coasting["time"], coasting["rotation_n"], label="n coasting")
    ax.plot(coasting["time"], coasting["rotation_e"], label="e coasting")
    ax.plot(coasting["time"], coasting["rotation_d"], label="d coasting")
    ax.legend()
    ax.set_ylabel("rotation/(rad/s)")
    ax.set_xlabel("time/s")
    ax.grid(which="both")
    return fig

def make_graph(result: ResultForReport, site: LaunchSite) -> Graphs:
    return Graphs(
        ideal_dynamic_pressure = dynamic_pressure_figure(result.result_ideal_parachute_off),
        ideal_air_velocity_figure = air_velocity_figure(result.result_ideal_parachute_off),
        ideal_altitude_downrange_figure = altitude_downrange_figure(result.result_ideal_parachute_off),
        ideal_time_altitude_figure = time_altitude_figure(result.result_ideal_parachute_off),
        ideal_landing_figure = landing_figure(result.result_ideal_parachute_off, site),
        ideal_stability_figure = stability_figure(result),
        ideal_wind_figure = wind_figure(result.context),
        ideal_acceleration_figure = acceleration_figure(result.result_ideal_parachute_off),
        ideal_rotation_figure = rotation_figure(result.result_ideal_parachute_off),
    )
