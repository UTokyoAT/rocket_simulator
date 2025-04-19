import os
from src import config_read, report_config_read
from src.make_report import make_result_for_report
from src.make_report.result_for_report import ResultForReport
from src.make_report import make_graph
from src import graph_writer


def write_row_data(result: ResultForReport):
    output_dir = os.path.join(os.path.abspath("output"), "report", "raw")
    os.makedirs(output_dir, exist_ok=True)
    result.result_ideal_parachute_off.to_csv(
        os.path.join(output_dir, "ideal_parachute_off.csv"),
    )
    result.result_ideal_parachute_on.to_csv(
        os.path.join(output_dir, "ideal_parachute_on.csv"),
    )
    result.result_nominal_parachute_off.to_csv(
        os.path.join(output_dir, "nominal_parachute_off.csv"),
    )
    result.result_nominal_parachute_on.to_csv(
        os.path.join(output_dir, "nominal_parachute_on.csv"),
    )
    for result_by_launcher_elevation in result.result_by_launcher_elevation:
        for result_by_wind in result_by_launcher_elevation.result:
            for result_by_direction in result_by_wind.result:
                name = f"launcher_elevation_{result_by_launcher_elevation.launcher_elevation}_wind_speed_{result_by_wind.wind_speed}_wind_direction_{result_by_direction.wind_direction}"
                result_by_direction.result_parachute_off.to_csv(
                    os.path.join(
                        output_dir,
                        name + "_parachute_off.csv",
                    )
                )
                result_by_direction.result_parachute_on.to_csv(
                    os.path.join(
                        output_dir,
                        name + "_parachute_on.csv",
                    )
                )


def run():
    config = config_read.read(os.path.abspath("config"))
    report_config = report_config_read.read(os.path.abspath("config"))
    result = make_result_for_report.make_result_for_report(config, report_config)
    write_row_data(result)

    graphs = make_graph.make_graph(result)
    path_graph = os.path.join(
        os.path.abspath("output"),
        "report",
        "graph",
    )
    os.makedirs(path_graph, exist_ok=True)
    graph_writer.write(
        path=path_graph,
        graphs=graphs,
    )


if __name__ == "__main__":
    run()
