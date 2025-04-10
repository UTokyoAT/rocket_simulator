from src import config_read
import os
from src.core import simple_simulation


config = config_read.read(os.path.abspath("config"))
result = simple_simulation.simulate(config, False)
os.makedirs("output", exist_ok=True)
result.to_df().to_csv("output/result.csv")
