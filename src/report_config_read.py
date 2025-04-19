import os
import json
from .make_report.make_result_for_report import ReportConfig


def read(folder_path: str) -> ReportConfig:
    with open(os.path.join(folder_path, "report_config.json"), "r") as file:
        js = json.load(file)
    return ReportConfig(
        launcher_elevation=js["launcher_elevation"],
        wind_speed_nominal=js["wind_speed_nominal"],
        wind_direction_nominal=js["wind_direction_nominal"],
        wind_speed_list=js["wind_speed_list"],
        wind_direction_list=js["wind_direction_list"],
        launcher_elevation_list=js["launcher_elevation_list"]
    )
