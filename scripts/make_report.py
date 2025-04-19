import os
from src import config_read, report_config_read
from src.make_report import make_result_for_report


def run():
    config = config_read.read(os.path.abspath("config"))
    report_config = report_config_read.read(os.path.abspath("config"))
    result = make_result_for_report.make_result_for_report(config, report_config)
    output_dir = os.path.join(os.path.abspath("output"), "report", "row")
    os.makedirs(output_dir, exist_ok=True)
    result.result_ideal_parachute_off.to_df().to_csv(
        os.path.join(output_dir, "ideal_parachute_off.csv"),
    )
    result.result_ideal_parachute_on.to_df().to_csv(
        os.path.join(output_dir, "ideal_parachute_on.csv"),
    )
    result.result_nominal_parachute_off.to_df().to_csv(
        os.path.join(output_dir, "nominal_parachute_off.csv"),
    )
    result.result_nominal_parachute_on.to_df().to_csv(
        os.path.join(output_dir, "nominal_parachute_on.csv"),
    )
    for result_by_launcher_elevation in result.result_by_launcher_elevation:
        for result_by_wind in result_by_launcher_elevation.result:
            for result_by_direction in result_by_wind.result:
                name = f"launcher_elevation_{result_by_launcher_elevation.launcher_elevation}_wind_speed_{result_by_wind.wind_speed}_wind_direction_{result_by_direction.wind_direction}"
                result_by_direction.result_parachute_off.to_df().to_csv(
                    os.path.join(
                        output_dir,
                        name + "_parachute_off.csv",
                    )
                )
                result_by_direction.result_parachute_on.to_df().to_csv(
                    os.path.join(
                        output_dir,
                        name + "_parachute_on.csv",
                    )
                )


if __name__ == "__main__":
    run()
