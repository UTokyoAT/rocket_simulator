import unittest

import matplotlib as mpl

mpl.use("Agg")

import pandas as pd
from matplotlib import pyplot as plt

from src.make_report.make_graph import dynamic_pressure_figure, rotation_figure


def flight_data() -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "time": 0.0,
                "burning": True,
                "dynamic_pressure": 100.0,
                "rotation_x": 0.1,
                "rotation_y": 0.2,
                "rotation_z": 0.3,
            },
            {
                "time": 1.0,
                "burning": False,
                "dynamic_pressure": 50.0,
                "rotation_x": 0.4,
                "rotation_y": 0.5,
                "rotation_z": 0.6,
            },
        ],
    )


class TestMakeGraph(unittest.TestCase):
    def tearDown(self) -> None:
        plt.close("all")

    def test_dynamic_pressure_figure_creates_one_figure(self) -> None:
        before = set(plt.get_fignums())
        fig = dynamic_pressure_figure(flight_data())
        created = set(plt.get_fignums()) - before
        self.assertEqual(created, {fig.number})

    def test_rotation_figure_uses_body_axes(self) -> None:
        data = flight_data()
        fig = rotation_figure(data)
        labels = [line.get_label() for line in fig.axes[0].get_lines()]
        self.assertEqual(
            labels,
            [
                "x burning",
                "y burning",
                "z burning",
                "x coasting",
                "y coasting",
                "z coasting",
            ],
        )
        burning = data[data["burning"]]
        np_rotation_x = burning["rotation_x"].to_numpy()
        self.assertEqual(list(fig.axes[0].get_lines()[0].get_ydata()), list(np_rotation_x))


if __name__ == "__main__":
    unittest.main()
