import unittest

import numpy as np
import pandas as pd

from src.core.config import Config, WindPowerLow
from src.core.simulation_context import SimulationContext
from src.geography.launch_site import LaunchSite
from src.make_report.make_dict import dynamic_pressure, make_dict, max_altitude
from src.make_report.result_for_report import ResultForReport


def flight_data() -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "time": 0.0,
                "on_launcher": True,
                "burning": True,
                "position_n": 0.0,
                "position_e": 0.0,
                "position_d": 0.0,
                "velocity_n": 0.0,
                "velocity_e": 0.0,
                "velocity_d": 0.0,
                "dynamic_pressure": 100.0,
                "velocity_air_body_frame_x": 1.0,
                "velocity_air_body_frame_y": 0.0,
                "velocity_air_body_frame_z": 0.0,
                "acceleration_body_frame_x": 1.0,
                "acceleration_body_frame_y": 0.0,
                "acceleration_body_frame_z": 0.0,
            },
            {
                "time": 1.25,
                "on_launcher": False,
                "burning": True,
                "position_n": 10.0,
                "position_e": 0.0,
                "position_d": -40.0,
                "velocity_n": 20.0,
                "velocity_e": 0.0,
                "velocity_d": -10.0,
                "dynamic_pressure": 2500.0,
                "velocity_air_body_frame_x": 6.0,
                "velocity_air_body_frame_y": 8.0,
                "velocity_air_body_frame_z": 0.0,
                "acceleration_body_frame_x": 2.0,
                "acceleration_body_frame_y": 0.0,
                "acceleration_body_frame_z": 0.0,
            },
            {
                "time": 8.0,
                "on_launcher": False,
                "burning": False,
                "position_n": 100.0,
                "position_e": 0.0,
                "position_d": -200.5,
                "velocity_n": 30.0,
                "velocity_e": 40.0,
                "velocity_d": 0.0,
                "dynamic_pressure": 9000.0,
                "velocity_air_body_frame_x": 3.0,
                "velocity_air_body_frame_y": 4.0,
                "velocity_air_body_frame_z": 0.0,
                "acceleration_body_frame_x": 0.0,
                "acceleration_body_frame_y": 0.0,
                "acceleration_body_frame_z": 0.0,
            },
            {
                "time": 15.5,
                "on_launcher": False,
                "burning": False,
                "position_n": 300.0,
                "position_e": 400.0,
                "position_d": 1.0,
                "velocity_n": 0.0,
                "velocity_e": 0.0,
                "velocity_d": 20.0,
                "dynamic_pressure": 10.0,
                "velocity_air_body_frame_x": 0.0,
                "velocity_air_body_frame_y": 0.0,
                "velocity_air_body_frame_z": 1.0,
                "acceleration_body_frame_x": 0.0,
                "acceleration_body_frame_y": 0.0,
                "acceleration_body_frame_z": 0.0,
            },
        ],
    )


class TestMakeDict(unittest.TestCase):
    def test_max_altitude_uses_airspeed(self) -> None:
        summary = max_altitude(flight_data())
        ground_speed = float(np.hypot(30.0, 40.0))
        self.assertEqual(
            summary,
            {
                "時刻/s": 8.0,
                "高度/m": 200.5,
                "対気速度/(m/s)": 5.0,
            },
        )
        self.assertNotEqual(summary["対気速度/(m/s)"], ground_speed)

    def test_dynamic_pressure_selects_burning_period(self) -> None:
        data = flight_data()
        burning_summary = dynamic_pressure(data, through_all_time=False)
        all_time_summary = dynamic_pressure(data, through_all_time=True)
        self.assertEqual(
            set(burning_summary),
            {"時刻/s", "高度/m", "動圧/kPa", "対気速度/(m/s)"},
        )
        self.assertEqual(
            burning_summary,
            {
                "時刻/s": 1.25,
                "高度/m": 40.0,
                "動圧/kPa": 2.5,
                "対気速度/(m/s)": 10.0,
            },
        )
        self.assertEqual(all_time_summary["動圧/kPa"], 9.0)
        self.assertEqual(all_time_summary["対気速度/(m/s)"], 5.0)

    def test_make_dict_reports_airspeed_and_burning_dynamic_pressure(self) -> None:
        data = flight_data()
        config = Config(
            mass=pd.DataFrame({"mass": [10.0, 9.0]}, index=[0.0, 1.0]),
            wind=WindPowerLow(
                reference_height=10.0,
                wind_speed=5.0,
                exponent=7.0,
                wind_direction=45.0,
            ),
            thrust=pd.DataFrame({"thrust": [100.0, 0.0]}, index=[0.0, 1.0]),
            CA=0.5,
            CN_alpha=2.0,
            body_area=0.01,
            wind_center=np.array([0.4, 0.0, 0.0]),
            dt=0.01,
            launcher_length=3.0,
            inertia_tensor_xx=1.0,
            inertia_tensor_yy=1.0,
            inertia_tensor_zz=0.1,
            inertia_tensor_zy=0.0,
            inertia_tensor_xz=0.0,
            inertia_tensor_xy=0.0,
            first_elevation=80.0,
            first_azimuth=0.0,
            first_roll=0.0,
            parachute_terminal_velocity=5.0,
            parachute_delay_time=2.0,
            first_gravity_center=np.array([0.5, 0.0, 0.0]),
            end_gravity_center=np.array([0.55, 0.0, 0.0]),
            length=1.0,
        )
        result = ResultForReport(
            config_nominal=config,
            context_nominal=SimulationContext(config),
            result_ideal_parachute_off=data,
            result_ideal_parachute_on=data,
            result_nominal_parachute_off=data,
            result_nominal_parachute_on=data,
            result_by_launcher_elevation=[],
        )
        site = LaunchSite.from_lat_lon(35.0, 135.0, [(35.01, 135.0), (35.01, 135.01), (35.0, 135.01)])
        summary = make_dict(result, site, config)
        self.assertEqual(summary["ideal_max_altitude"]["対気速度/(m/s)"], 5.0)
        self.assertEqual(summary["nominal_max_altitude"]["対気速度/(m/s)"], 5.0)
        self.assertEqual(summary["ideal_dynamic_pressure"]["動圧/kPa"], 2.5)
        self.assertEqual(summary["nominal_dynamic_pressure"]["動圧/kPa"], 2.5)
        self.assertEqual(summary["ideal_dynamic_pressure"]["対気速度/(m/s)"], 10.0)


if __name__ == "__main__":
    unittest.main()
