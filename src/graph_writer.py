import os
from .make_report.make_graph import Graphs


def write(path: str, graphs: Graphs):
    graphs.ideal_dynamic_pressure.savefig(
        os.path.join(path, "ideal_dynamic_pressure.png"),
    )