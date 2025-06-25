from dataclasses import dataclass


@dataclass
class ReportConfig:
    launcher_elevation: float
    wind_speed_nominal: float
    wind_direction_nominal: float
    wind_speed_list: list[float]
    wind_direction_list: list[float]
    launcher_elevation_list: list[float]
