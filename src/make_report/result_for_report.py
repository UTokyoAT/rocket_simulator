from dataclasses import dataclass

import pandas as pd

from src.core.config import Config
from src.core.simulation_context import SimulationContext


@dataclass
class ResultByWindDirection:
    wind_direction: float
    result_parachute_off: pd.DataFrame
    result_parachute_on: pd.DataFrame


@dataclass
class ResultByWindSpeed:
    wind_speed: float
    result: list[ResultByWindDirection]

    def append(
        self,
        wind_direction: float,
        result_parachute_off: pd.DataFrame,
        result_parachute_on: pd.DataFrame,
    ) -> None:

        self.result.append(
            ResultByWindDirection(
                wind_direction=wind_direction,
                result_parachute_off=result_parachute_off,
                result_parachute_on=result_parachute_on,
            ),
        )


@dataclass
class ResultByLauncherElevation:
    launcher_elevation: float
    result: list[ResultByWindSpeed]

    def append(
        self,
        wind_speed: float,
        wind_direction: float,
        result_parachute_off: pd.DataFrame,
        result_parachute_on: pd.DataFrame,
    ) -> None:
        for result_by_wind_speed in self.result:
            if result_by_wind_speed.wind_speed == wind_speed:
                result_by_wind_speed.append(
                    wind_direction, result_parachute_off, result_parachute_on,
                )
                return
        self.result.append(ResultByWindSpeed(wind_speed=wind_speed, result=[]))
        self.result[-1].append(
            wind_direction, result_parachute_off, result_parachute_on,
        )


@dataclass
class ResultForReport:
    config_nominal: Config
    context_nominal: SimulationContext
    result_ideal_parachute_off: pd.DataFrame
    result_ideal_parachute_on: pd.DataFrame
    result_nominal_parachute_off: pd.DataFrame
    result_nominal_parachute_on: pd.DataFrame
    result_by_launcher_elevation: list[ResultByLauncherElevation]

    def append(
        self,
        wind_speed: float,
        wind_direction: float,
        launcher_elevation: float,
        result_parachute_off: pd.DataFrame,
        result_parachute_on: pd.DataFrame,
    ) -> None:
        for result_by_launcher_elevation in self.result_by_launcher_elevation:
            if result_by_launcher_elevation.launcher_elevation == launcher_elevation:
                result_by_launcher_elevation.append(
                    wind_speed,
                    wind_direction,
                    result_parachute_off,
                    result_parachute_on,
                )
                return
        self.result_by_launcher_elevation.append(
            ResultByLauncherElevation(launcher_elevation=launcher_elevation, result=[]),
        )
        self.result_by_launcher_elevation[-1].append(
            wind_speed,
            wind_direction,
            result_parachute_off,
            result_parachute_on,
        )
