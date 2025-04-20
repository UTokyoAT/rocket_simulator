import os
from .make_report.make_graph import Graphs


def write(path: str, graphs: Graphs):
    graphs.ideal_dynamic_pressure.savefig(
        os.path.join(path, "ideal_dynamic_pressure.png"),
    )
    graphs.ideal_air_velocity_figure.savefig(
        os.path.join(path, "ideal_air_velocity_figure.png"),
    )