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


@dataclass
class ResultForReport:
    config: Config
    context: SimulationContext
    result_ideal: SimulationResult
    result_nominal: SimulationResult
    result_by_wind_speed: list[ResultByWindSpeed]
