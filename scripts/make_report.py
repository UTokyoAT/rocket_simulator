import shutil
from pathlib import Path

from src import config_read, graph_writer, report_config_read
from src.make_report import make_graph, make_result_for_report
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


def run() -> None:
    # 既存のoutputフォルダを削除
    output_dir = Path("output")
    if output_dir.exists():
        shutil.rmtree(output_dir)

    config_path = Path("config")
    config = config_read.read(config_path)
    report_config = report_config_read.read(config_path)
    result = make_result_for_report.make_result_for_report(config, report_config)
    write_row_data(result)

    graphs = make_graph.make_graph(result)
    path_graph = Path("output") / "report" / "graph"
    path_graph.mkdir(parents=True, exist_ok=True)
    graph_writer.write(
        path=path_graph,
        graphs=graphs,
    )


if __name__ == "__main__":
    run()
