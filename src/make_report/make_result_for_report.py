import itertools
from concurrent.futures import ProcessPoolExecutor
from dataclasses import dataclass

import pandas as pd

from ..core import simple_simulation
from ..core.config import Config
from ..core.simulation_context import SimulationContext
from .result_for_report import ResultForReport


@dataclass
class ReportConfig:
    launcher_elevation: float
    wind_speed_nominal: float
    wind_direction_nominal: float
    wind_speed_list: list[float]
    wind_direction_list: list[float]
    launcher_elevation_list: list[float]


@dataclass
class Setting:
    launcher_elevation: float
    wind_speed: float
    wind_direction: float


def run(config: Config, setting: Setting) -> tuple[pd.DataFrame, pd.DataFrame]:
    config.first_elevation = setting.launcher_elevation
    config.wind.wind_speed = setting.wind_speed
    config.wind.wind_direction = setting.wind_direction
    results = simple_simulation.simulate(config, False)
    return (results[0].to_df(), results[1].to_df())


def run_concurrent(
    config: Config, settings: list[Setting],
) -> list[tuple[pd.DataFrame, pd.DataFrame]]:
    """シミュレーションを並列で実行する

    Args:
        config (Config): コンフィグ
        settings (list[Setting]): シミュレーションの設定リスト

    Returns:
        list[Wind]: シミュレーション結果のリスト。
            wind_speed_direction_pairsの順番に対応している。
    """
    with ProcessPoolExecutor() as executor:
        results = list(executor.map(run, [config] * len(settings), settings))
    return results


def make_result_for_report(
    config: Config, report_config: ReportConfig,
) -> ResultForReport:
    context = SimulationContext(config)
    setting_ideal = Setting(
        launcher_elevation=report_config.launcher_elevation,
        wind_speed=0,
        wind_direction=0,
    )
    setting_nominal = Setting(
        launcher_elevation=report_config.launcher_elevation,
        wind_speed=report_config.wind_speed_nominal,
        wind_direction=report_config.wind_direction_nominal,
    )

    settings_list = list(
        itertools.product(
            report_config.launcher_elevation_list,
            report_config.wind_speed_list,
            report_config.wind_direction_list,
        ),
    )
    settings_wind = [
        Setting(
            launcher_elevation=launcher_elevation,
            wind_speed=wind_speed,
            wind_direction=wind_direction,
        )
        for launcher_elevation, wind_speed, wind_direction in settings_list
    ]
    settings = [setting_ideal, setting_nominal] + settings_wind
    results = run_concurrent(config, settings)
    result_ideal = results[0]
    result_nominal = results[1]
    body = ResultForReport(
        config=config,
        context=context,
        result_ideal_parachute_off=result_ideal[0],
        result_ideal_parachute_on=result_ideal[1],
        result_nominal_parachute_off=result_nominal[0],
        result_nominal_parachute_on=result_nominal[1],
        result_by_launcher_elevation=[],
    )
    for setting, result in zip(settings[2:], results[2:], strict=False):
        body.append(
            wind_speed=setting.wind_speed,
            wind_direction=setting.wind_direction,
            launcher_elevation=setting.launcher_elevation,
            result_parachute_off=result[0],
            result_parachute_on=result[1],
        )
    return body
