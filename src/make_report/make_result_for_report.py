from dataclasses import dataclass
from concurrent.futures import ProcessPoolExecutor
import itertools
from .result_for_report import ResultForReport
from ..core.simulation_result import SimulationResult
from ..core.simulation_context import SimulationContext
from ..core import simple_simulation
from ..core.config import Config


@dataclass
class ReportConfig:
    wind_speed_nominal: float
    wind_direction_nominal: float
    wind_speed_list: list[float]
    wind_direction_list: list[float]


@dataclass
class Setting:
    wind_speed: float
    wind_direction: float


def run_concurrent(config: Config, settings: list[Setting]) -> list[SimulationResult]:
    """シミュレーションを並列で実行する

    Args:
        config (Config): コンフィグ
        settings (list[Setting]): シミュレーションの設定リスト

    Returns:
        list[Wind]: シミュレーション結果のリスト。
            wind_speed_direction_pairsの順番に対応している。
    """

    def run(setting: Setting) -> SimulationResult:
        config.wind.wind_speed = setting.wind_speed
        config.wind.wind_direction = setting.wind_direction
        return simple_simulation.simulate(config, False)

    with ProcessPoolExecutor() as executor:
        results = list(executor.map(run, settings))
    return results


def make_result_for_report(
    config: Config, report_config: ReportConfig
) -> ResultForReport:
    context = SimulationContext(config)
    setting_ideal = Setting(
        wind_speed=0,
        wind_direction=0,
    )
    setting_nominal = Setting(
        wind_speed=report_config.wind_speed_nominal,
        wind_direction=report_config.wind_direction_nominal,
    )

    settings_wind_list = list(
        itertools.product(
            report_config.wind_speed_list, report_config.wind_direction_list
        )
    )
    settings_wind = [
        Setting(wind_speed=wind_speed, wind_direction=wind_direction)
        for wind_speed, wind_direction in settings_wind_list
    ]
    settings = [setting_ideal, setting_nominal] + settings_wind
    results = run_concurrent(config, settings)
    result_ideal = results[0]
    result_nominal = results[1]
    body = ResultForReport(
        config=config,
        context=context,
        result_ideal=result_ideal,
        result_nominal=result_nominal,
        result_by_wind_speed=[],
    )
    for setting, result in zip(settings[2:], results[2:]):
        body.append(
            wind_speed=setting.wind_speed,
            wind_direction=setting.wind_direction,
            result=result,
        )
    return body
