import unittest

import matplotlib as mpl

mpl.use("Agg")

import pandas as pd
from matplotlib import pyplot as plt

from src.geography.launch_site import LaunchSite
from src.make_report.make_graph import (
    altitude_downrange_figure,
    dynamic_pressure_figure,
    fall_dispersion_figure,
    landing_figure,
    rotation_figure,
)
from src.make_report.result_for_report import ResultByWindDirection, ResultByWindSpeed


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

    def test_spatial_figures_use_equal_aspect(self) -> None:
        trajectory = pd.DataFrame(
            [
                {
                    "burning": True,
                    "position_n": 0.0,
                    "position_e": 0.0,
                    "position_d": 0.0,
                },
                {
                    "burning": False,
                    "position_n": 300.0,
                    "position_e": 40.0,
                    "position_d": -200.0,
                },
            ],
        )
        site = LaunchSite.from_lat_lon(35.0, 135.0, [(35.01, 135.0), (35.01, 135.01), (35.0, 135.01)])
        landing = pd.DataFrame([{"position_n": 100.0, "position_e": 20.0}])
        dispersion = [
            ResultByWindSpeed(
                wind_speed=3.0,
                result=[
                    ResultByWindDirection(
                        wind_direction=0.0,
                        result_parachute_off=pd.DataFrame([{"position_n": 10.0, "position_e": 20.0}]),
                        result_parachute_on=pd.DataFrame([{"position_n": 30.0, "position_e": 40.0}]),
                    ),
                ],
            ),
        ]
        figures = [
            altitude_downrange_figure(trajectory),
            landing_figure(landing, site),
            fall_dispersion_figure(dispersion, site, parachute=False),
        ]
        for fig in figures:
            self.assertEqual(fig.axes[0].get_aspect(), 1)
            self.assertEqual(fig.axes[0].get_adjustable(), "box")


if __name__ == "__main__":
    unittest.main()
