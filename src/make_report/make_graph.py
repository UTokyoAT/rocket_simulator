from dataclasses import dataclass
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.figure import Figure

from src.geography.launch_site import LaunchSite

from .result_for_report import ResultForReport


@dataclass
class Graphs:
    ideal_dynamic_pressure: Figure
    ideal_air_velocity_figure: Figure
    ideal_altitude_downrange_figure: Figure  
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


#def thrust_end_time():
    #thrust = pd.read_csv("simulator/files/thrust.csv")
    #thrust_not_first = thrust.iloc[10:]
    #return thrust_not_first[thrust_not_first["thrust"] == 0].iloc[0]["time"]


#def document_config():
    #with open("simulator/files/審査書用コンフィグ.json") as f:
        #return json.load(f)


#def flst():
    #with open("simulator/files/flst.json") as f:
        #return json.load(f)




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


def make_graph(result: ResultForReport) -> Graphs:
    return Graphs(
        ideal_dynamic_pressure = dynamic_pressure_figure(result.result_ideal_parachute_off),
        ideal_air_velocity_figure = air_velocity_figure(result.result_ideal_parachute_off),
        ideal_altitude_downrange_figure = altitude_downrange_figure(result.result_ideal_parachute_off),
    )