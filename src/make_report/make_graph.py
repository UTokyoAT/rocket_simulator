from dataclasses import dataclass
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from .result_for_report import ResultForReport


@dataclass
class Graphs:
    ideal_dynamic_pressure: Figure


def dynamic_pressure(data: pd.DataFrame) -> Figure:
    fig, ax = plt.subplots()
    # TODO: グラフを書く処理
    return fig


def make_graph(result: ResultForReport) -> Graphs:
    return Graphs(
        ideal_dynamic_pressure=dynamic_pressure(result.result_ideal),
    )
