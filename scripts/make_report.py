import os
from src import config_read, report_config_read
from src.make_report import make_result_for_report


def run():
    config = config_read.read(os.path.abspath("config"))
    report_config = report_config_read.read(os.path.abspath("config"))
    result = make_result_for_report.make_result_for_report(config, report_config)
    output_dir = os.path.join(os.path.abspath("output"), "report", "row")
    os.makedirs(output_dir, exist_ok=True)
    result.result_ideal.to_df().to_csv(
        os.path.join(output_dir, "ideal.json"),
    )
    result.result_nominal.to_df().to_csv(
        os.path.join(output_dir, "nominal.json"),
    )
    for result_by_wind in result.result_by_wind_speed:
        for result_by_direction in result_by_wind.result:
            result_by_direction.result.to_df().to_csv(
                os.path.join(
                    output_dir,
                    f"wind_speed_{result_by_wind.wind_speed}_wind_direction_{result_by_direction.wind_direction}.json",
                )
            )


if __name__ == "__main__":
    run()
