from pathlib import Path

from src import config_read
from src.core import simple_simulation

config = config_read.read(Path("config"))
result = simple_simulation.simulate(config, parachute_on=False)
Path("output").mkdir(exist_ok=True)
result.to_df().to_csv("output/result.csv")
