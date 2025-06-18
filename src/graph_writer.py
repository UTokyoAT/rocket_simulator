from pathlib import Path

from matplotlib import pyplot as plt

from .make_report.make_graph import Graphs


def write(path: Path, graphs: Graphs) -> None:
    graphs.ideal_dynamic_pressure.savefig(
        path / "ideal_dynamic_pressure.png",
    )
    plt.close(graphs.ideal_dynamic_pressure)
    graphs.ideal_air_velocity_figure.savefig(
        path / "ideal_air_velocity_figure.png",
    )
    plt.close(graphs.ideal_air_velocity_figure)
    graphs.ideal_altitude_downrange_figure.savefig(
        path / "ideal_altitude_downrange_figure.png",
    )
    plt.close(graphs.ideal_altitude_downrange_figure)
    graphs.ideal_time_altitude_figure.savefig(
        path / "ideal_time_altitude_figure.png",
    )
    plt.close(graphs.ideal_time_altitude_figure)
    graphs.ideal_landing_figure.savefig(
        path / "ideal_landing_figure.png",
    )
    plt.close(graphs.ideal_landing_figure)
    graphs.ideal_stability_figure.savefig(
        path / "ideal_stability_figure.png",
    )
    plt.close(graphs.ideal_stability_figure)
    graphs.ideal_acceleration_figure.savefig(
        path / "ideal_acceleration_figure.png",
    )
    plt.close(graphs.ideal_acceleration_figure)
    graphs.ideal_rotation_figure.savefig(
        path / "ideal_rotation_figure.png",
    )
    plt.close(graphs.ideal_rotation_figure)
    graphs.nominal_dynamic_pressure.savefig(
        path / "nominal_dynamic_pressure.png",
    )
    plt.close(graphs.nominal_dynamic_pressure)
    graphs.nominal_air_velocity_figure.savefig(
        path / "nominal_air_velocity_figure.png",
    )
    plt.close(graphs.nominal_air_velocity_figure)
    graphs.nominal_altitude_downrange_figure.savefig(
        path / "nominal_altitude_downrange_figure.png",
    )
    plt.close(graphs.nominal_altitude_downrange_figure)
    graphs.nominal_time_altitude_figure.savefig(
        path / "nominal_time_altitude_figure.png",
    )
    plt.close(graphs.nominal_time_altitude_figure)
    graphs.nominal_landing_figure.savefig(
        path / "nominal_landing_figure.png",
    )
    plt.close(graphs.nominal_landing_figure)
    graphs.nominal_acceleration_figure.savefig(
        path / "nominal_acceleration_figure.png",
    )
    plt.close(graphs.nominal_acceleration_figure)
    graphs.nominal_rotation_figure.savefig(
        path / "nominal_rotation_figure.png",
    )
    plt.close(graphs.nominal_rotation_figure)
    graphs.nominal_wind_figure.savefig(
        path / "nominal_wind_figure.png",
    )
    plt.close(graphs.nominal_wind_figure)
    for elevation, fig in graphs.nominal_fall_dispersion_figure_parachute_off.items():
        filename = f"nominal_fall_dispersion_parachute_off{elevation:.1f}deg.png"
        fig.savefig(path / filename)
        plt.close(fig)
    for elevation, fig in graphs.nominal_fall_dispersion_figure_parachute_on.items():
        filename = f"nominal_fall_dispersion_parachute_on{elevation:.1f}deg.png"
        fig.savefig(path / filename)
        plt.close(fig)
