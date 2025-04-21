from pathlib import Path
from .make_report.make_graph import Graphs


def write(path: Path, graphs: Graphs):
    graphs.ideal_dynamic_pressure.savefig(
        path / "ideal_dynamic_pressure.png",
    )
    graphs.ideal_air_velocity_figure.savefig(
        path / "ideal_air_velocity_figure.png",
    )
