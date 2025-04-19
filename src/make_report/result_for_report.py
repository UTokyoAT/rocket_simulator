from dataclasses import dataclass
from ..core.simulation_result import SimulationResult
from ..core.simulation_context import SimulationContext
from ..core.config import Config


@dataclass
class ResultByWindDirection:
    wind_direction: float
    result_parachute_off: SimulationResult
    result_parachute_on: SimulationResult


@dataclass
class ResultByWindSpeed:
    wind_speed: float
    result: list[ResultByWindDirection]

    def append(
        self,
        wind_direction: float,
        result_parachute_off: SimulationResult,
        result_parachute_on: SimulationResult,
    ):
        self.result.append(
            ResultByWindDirection(
                wind_direction=wind_direction,
                result_parachute_off=result_parachute_off,
                result_parachute_on=result_parachute_on,
            )
        )


@dataclass
class ResultByLauncherElevation:
    launcher_elevation: float
    result: list[ResultByWindSpeed]

    def append(
        self,
        wind_speed: float,
        wind_direction: float,
        result_parachute_off: SimulationResult,
        result_parachute_on: SimulationResult,
    ):
        for result_by_wind_speed in self.result:
            if result_by_wind_speed.wind_speed == wind_speed:
                result_by_wind_speed.append(
                    wind_direction, result_parachute_off, result_parachute_on
                )
                return
        self.result.append(ResultByWindSpeed(wind_speed=wind_speed, result=[]))
        self.result[-1].append(
            wind_direction, result_parachute_off, result_parachute_on
        )


@dataclass
class ResultForReport:
    config: Config
    context: SimulationContext
    result_ideal_parachute_off: SimulationResult
    result_ideal_parachute_on: SimulationResult
    result_nominal_parachute_off: SimulationResult
    result_nominal_parachute_on: SimulationResult
    result_by_launcher_elevation: list[ResultByLauncherElevation]

    def append(
        self,
        wind_speed: float,
        wind_direction: float,
        launcher_elevation: float,
        result_parachute_off: SimulationResult,
        result_parachute_on: SimulationResult,
    ):
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
            ResultByLauncherElevation(launcher_elevation=launcher_elevation, result=[])
        )
        self.result_by_launcher_elevation[-1].append(
            wind_speed,
            wind_direction,
            result_parachute_off,
            result_parachute_on,
        )
