import shutil
import json
from pathlib import Path

from src import config_read, graph_writer, report_config_read
from src.geography.kml import landing_range_to_kml, parse_launch_site
from src.geography.landing_range import LandingRange
from src.geography.launch_site import LaunchSite
from src.make_report import make_graph, make_dict, make_result_for_report
from src.make_report.result_for_report import ResultForReport


def write_row_data(result: ResultForReport) -> None:
    output_dir = Path("output") / "report" / "raw"
    output_dir.mkdir(parents=True, exist_ok=True)
    result.result_ideal_parachute_off.to_csv(
        output_dir / "ideal_parachute_off.csv",
    )
    result.result_ideal_parachute_on.to_csv(
        output_dir / "ideal_parachute_on.csv",
    )
    result.result_nominal_parachute_off.to_csv(
        output_dir / "nominal_parachute_off.csv",
    )
    result.result_nominal_parachute_on.to_csv(
        output_dir / "nominal_parachute_on.csv",
    )
    for elev_result in result.result_by_launcher_elevation:
        for wind_result in elev_result.result:
            for dir_result in wind_result.result:
                name = (
                    f"launcher_elevation_{elev_result.launcher_elevation}"
                    f"_wind_speed_{wind_result.wind_speed}"
                    f"_wind_direction_{dir_result.wind_direction}"
                )
                dir_result.result_parachute_off.to_csv(
                    output_dir / f"{name}_parachute_off.csv",
                )
                dir_result.result_parachute_on.to_csv(
                    output_dir / f"{name}_parachute_on.csv",
                )


def write_landing_range_kml(result: ResultForReport, launch_site: LaunchSite) -> None:
    """着陸範囲をKMLファイルとして出力する

    Args:
        result: シミュレーション結果
        launch_site: 発射地点情報
    """
    output_dir = Path("output") / "report" / "kml"
    output_dir.mkdir(parents=True, exist_ok=True)

    # 各発射角度ごとにLandingRangeを作成
    for elev_result in result.result_by_launcher_elevation:
        landing_range = LandingRange.from_result_by_launcher_elevation(
            launch_site.launch_point.latitude,
            launch_site.launch_point.longitude,
            elev_result,
        )
        # KMLファイルとして出力
        kml_str = landing_range_to_kml(landing_range)
        output_path = output_dir / f"landing_range_elevation_{elev_result.launcher_elevation}.kml"
        output_path.write_text(kml_str)


def run() -> None:
    # 既存のoutputフォルダを削除
    output_dir = Path("output")
    if output_dir.exists():
        shutil.rmtree(output_dir)

    config_path = Path("config")
    config = config_read.read(config_path)
    report_config = report_config_read.read(config_path)

    # launch_site.kmlから発射地点情報を読み込む
    launch_site_kml = (config_path / "launch_site.kml").read_text()
    launch_site = parse_launch_site(launch_site_kml, "発射地点", "落下可能域")

    result = make_result_for_report.make_result_for_report(config, report_config)
    write_row_data(result)

    result_dict = make_dict.make_dict(result, launch_site)
    output_dir = Path("output") / "report"
    output_dir.mkdir(parents=True, exist_ok=True)
    path_dict = output_dir / "result_text.json"
    path_dict.write_text(json.dumps(result_dict, indent=4, ensure_ascii=False), encoding="utf-8")

    graphs = make_graph.make_graph(result, launch_site)
    path_graph = Path("output") / "report" / "graph"
    path_graph.mkdir(parents=True, exist_ok=True)
    graph_writer.write(
        path=path_graph,
        graphs=graphs,
    )

    # 着陸範囲をKMLファイルとして出力
    write_landing_range_kml(result, launch_site)


if __name__ == "__main__":
    run()
