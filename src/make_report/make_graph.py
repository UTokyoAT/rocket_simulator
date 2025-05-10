from dataclasses import dataclass
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from matplotlib.figure import Figure
from src.geography.launch_site import LaunchSite
from .result_for_report import ResultForReport
from .result_for_report import SimulationContext
from src.core.gravity_center import thrust_end_time


@dataclass
class Graphs:
    ideal_dynamic_pressure: Figure
    ideal_air_velocity_figure: Figure
    ideal_altitude_downrange_figure: Figure
    ideal_time_altitude_figure: Figure
    ideal_landing_figure: Figure
    ideal_stability_figure: Figure
    ideal_wind_figure: Figure

#def velocity_norm(row):
    #return (row.vel_NED_x**2 + row.vel_NED_y**2 + row.vel_NED_z**2) ** 0.5


#def acc_norm(row):
    #return (row.acc_BODY_x**2 + row.acc_BODY_y**2 + row.acc_BODY_z**2) ** 0.5


#def air_velocity_norm(row):
    #return (
       #row.vel_AIR_BODY_x**2 + row.vel_AIR_BODY_y**2 + row.vel_AIR_BODY_z**2
    #) ** 0.5


#def mode_change_row(data: pd.DataFrame, mode):
    #return data[data["mode"] == mode].iloc[0]


#def launch_clear(data: pd.DataFrame):
    """ランチクリア時の情報"""

    #launch_clear = mode_change_row(flight_data, 1)
    #v = velocity_norm(launch_clear)
    #theta = np.deg2rad(document_config()["最小射角"])
    #alpha = np.deg2rad(21)
    #beta = np.deg2rad(20)
    #w_alpha = v * np.tan(alpha) / (np.sin(theta) + np.cos(theta) * np.tan(alpha))
    #w_beta = v * np.tan(beta)
    #if v < 15:
        #print("ランチクリア速度が遅すぎます．打ち上げできません")
    #return {
        #"時刻/s": round(launch_clear.time, 2),
        #"速度/(m/s)": round(v, 2),
        #"順風迎角21degの時の風速/(m/s)": round(w_alpha, 2),
        #"側風迎角20degの時の風速/(m/s)": round(w_beta, 2),
        #"風速制限/(m/s)": round(min(w_alpha, w_beta), 2),
    #}

def burning_coasting_division(data: pd.DataFrame):
    burning = data[data["burning"] == True]
    coasting = data[data["burning"] == False]
    return burning, coasting

#def dynamic_pressure(flight_data, all=False):
    #burning, coasting = burning_coasting_division(flight_data)
    ### plt.plot(burning["time"],burning["dynamic_pressure"],label="burning")
    ### plt.plot(coasting["time"],coasting["dynamic_pressure"],label="coasting")
    ### plt.legend()
    ### # plt.title("dynamic pressure")
    ### plt.xlabel("time/s")
    ### plt.ylabel("dynamic pressure/Pa")
    ### plt.grid(which="both")

    ### plt.savefig("dynamic_pressure.png")
    ### plt.clf()
    #if all:
        #pressure_max = flight_data.loc[flight_data["dynamic_pressure"].idxmax()]
    #else:
        #pressure_max = burning.loc[burning["dynamic_pressure"].idxmax()]
    #return {
        #"時刻/s": round(pressure_max.time, 2),
        #"高度/m": round(pressure_max.altitude, 2),
        #"動圧/kPa": round(pressure_max.dynamic_pressure / 1000, 2),
        #"対気速度/(m/s)": round(air_velocity_norm(pressure_max), 2),
    #}
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

#def altitude_downrange_figure(data: pd.DataFrame) -> Figure:
    #burning, coasting = burning_coasting_division(data)

    #def downrange(row):
        #return geography.distance(
            #data.lat[0], data.lon[0], row.lat, row.lon
        #)

    # plt.plot(burning.apply(downrange,axis=1),burning.altitude,label="burning")
    # plt.plot(coasting.apply(downrange,axis=1),coasting.altitude,label="coasting")
    # plt.legend()
    # # plt.title("altitude-downrange")
    # plt.xlabel("downrange/m")
    # plt.ylabel("altitude/m")
    # plt.grid(which="both")
    # plt.savefig("altitude-downrange.png")
    # plt.clf()
    
    
    #fig, ax = plt.subplots()
    #ax.plot(burning.apply(downrange, axis=1), burning.altitude, label="burning")
    #ax.plot(coasting.apply(downrange, axis=1), coasting.altitude, label="coasting")
    #ax.legend()
    #ax.set_xlabel("downrange/m")
    #ax.set_ylabel("altitude/m")
    #ax.grid(which="both")
    #return fig

def time_altitude_figure(data: pd.DataFrame) -> Figure:
    burning, coasting = burning_coasting_division(data)
    # plt.plot(burning["time"],burning["altitude"],label="burning")
    # plt.plot(coasting["time"],coasting["altitude"],label="coasting")
    # plt.xlabel("time/s")
    # plt.ylabel("altitude/m")
    # plt.legend()
    # plt.grid(which="both")
    # plt.savefig("time-altitude.png")
    # plt.clf()
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
    ax.plot(site.points_east() + [site.points_east()[0]],  
            site.points_north() + [site.points_north()[0]],
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
    # plt.plot(wind_df["wind_speed"],wind_df["altitude"])
    # # plt.title("wind speed")
    # plt.ylabel("altitude/m")
    # plt.xlabel("wind speed/m/s")
    # plt.grid(which="both")
    # plt.savefig("wind_speed.png")
    # plt.clf()
    fig, ax = plt.subplots()
    ax.plot(altitude, wind_speed)
    ax.set_ylabel("altitude/m")
    ax.set_xlabel("wind speed/m/s")
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
    )
