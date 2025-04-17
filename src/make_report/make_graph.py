from dataclasses import dataclass
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from .result_for_report import ResultForReport


@dataclass
class Graphs:
    ideal_dynamic_pressure: Figure
    ideal_air_velocity_figure: Figure

def burning_coasting_division(data: pd.DataFrame):
    burning = data[data['burning'] == True]
    coasting = data[data['burning'] == False]
    return burning, coasting

def dynamic_pressure(data: pd.DataFrame) -> Figure:
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


def make_graph(result: ResultForReport) -> Graphs:
    return Graphs(
        ideal_dynamic_pressure = dynamic_pressure(result.result_ideal),
        ideal_air_velocity_figure = air_velocity_figure(result.result_ideal),
    )
