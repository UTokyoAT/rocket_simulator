from dataclasses import dataclass
from ..core.simulation_result import SimulationResult
from ..core.simulation_context import SimulationContext
from ..core.config import Config


@dataclass
class ResultByWindDirection:
    wind_direction: float
    result: SimulationResult


@dataclass
class ResultByWindSpeed:
    wind_speed: float
    result: list[ResultByWindDirection]

    def append(self, wind_direction: float, result: SimulationResult):
        self.result.append(
            ResultByWindDirection(wind_direction=wind_direction, result=result)
        )


@dataclass
class ResultForReport:
    config: Config
    context: SimulationContext
    result_ideal: SimulationResult
    result_nominal: SimulationResult
    result_by_wind_speed: list[ResultByWindSpeed]

    def append(self, wind_speed: float, wind_direction: float, result: SimulationResult):
        for result_by_wind_speed in self.result_by_wind_speed:
            if result_by_wind_speed.wind_speed == wind_speed:
                result_by_wind_speed.append(wind_direction, result)
                return
        self.result_by_wind_speed.append(
            ResultByWindSpeed(
                wind_speed=wind_speed,
                result=[ResultByWindDirection(wind_direction=wind_direction, result=result)],
            )
        )
