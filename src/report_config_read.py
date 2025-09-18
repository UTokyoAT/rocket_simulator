import json
from pathlib import Path

from src.make_report.make_result_for_report import ReportConfig


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
