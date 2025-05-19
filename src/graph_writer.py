from pathlib import Path

from .make_report.make_graph import Graphs


def write(path: Path, graphs: Graphs) -> None:
    graphs.ideal_dynamic_pressure.savefig(
        path / "ideal_dynamic_pressure.png",
    )
    graphs.ideal_air_velocity_figure.savefig(
        path / "ideal_air_velocity_figure.png",
    )
    graphs.ideal_altitude_downrange_figure.savefig(
        path / "ideal_altitude_downrange_figure.png",
    )
    graphs.ideal_time_altitude_figure.savefig(
        path / "ideal_time_altitude_figure.png",
    )
    graphs.ideal_altitude_downrange_figure.savefig(
        path / "ideal_altitude_downrange_figure.png",
    )
    graphs.ideal_landing_figure.savefig(
        path / "ideal_landing_figure.png",
    )
    graphs.ideal_stability_figure.savefig(
        path / "deal_stability_figure.png",
    )
    graphs.ideal_acceleration_figure.savefig(
        path / "ideal_acceleration_figure.png",
    )
    graphs.ideal_rotation_figure.savefig(
        path / "ideal_rotation_figure.png",
    )
    graphs.nominal_dynamic_pressure.savefig(
        path / "nominal_dynamic_pressure.png",
    )
    graphs.nominal_air_velocity_figure.savefig(
        path / "nominal_air_velocity_figure.png",
    )
    graphs.nominal_altitude_downrange_figure.savefig(
        path / "nominal_altitude_downrange_figure.png",
    )
    graphs.nominal_time_altitude_figure.savefig(
        path / "nominal_time_altitude_figure.png",
    )
    graphs.nominal_landing_figure.savefig(
        path / "nominal_landing_figure.png",
    )
    graphs.nominal_acceleration_figure.savefig(
        path / "nominal_acceleration_figure.png",
    )
    graphs.nominal_rotation_figure.savefig(
        path / "nominal_rotation_figure.png",
    )
    graphs.nominal_wind_figure.savefig(
        path / "ideal_wind_figure.png",
    )
