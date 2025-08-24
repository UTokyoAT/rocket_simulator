import json
from dataclasses import dataclass
from pathlib import Path


@dataclass
class ReportConfig:
    launcher_elevation: float
    wind_speed_nominal: float
    wind_direction_nominal: float
    wind_speed_list: list[float]
    wind_direction_list: list[float]
    launcher_elevation_list: list[float]


def read(folder_path: Path) -> ReportConfig:
    config_file = folder_path / "report_config.json"
    js = json.loads(config_file.read_text())
    return ReportConfig(
        launcher_elevation=js["launcher_elevation"],
        wind_speed_nominal=js["wind_speed_nominal"],
        wind_direction_nominal=js["wind_direction_nominal"],
        wind_speed_list=js["wind_speed_list"],
        wind_direction_list=js["wind_direction_list"],
        launcher_elevation_list=js["launcher_elevation_list"],
    )
