from pathlib import Path
from src import config_read
from src.core import simple_simulation
from concurrent.futures import ProcessPoolExecutor
import matplotlib.pyplot as plt


def simulate(wind_direction, wind_speed):
    config_path = Path("config")
    config = config_read.read(config_path)
    config.wind.wind_direction = wind_direction
    config.wind.wind_speed = wind_speed
    return simple_simulation.simulate(config, False)


def figure():
    with ProcessPoolExecutor() as e:
        r = list(e.map(simulate, range(0, 360, 45), [6] * 8))
    x1 = [r[0].last().position[1] for r in r]
    y1 = [r[0].last().position[0] for r in r]
    x2 = [r[1].last().position[1] for r in r]
    y2 = [r[1].last().position[0] for r in r]
    plt.plot(x1 + [x1[0]], y1 + [y1[0]])
    plt.plot(x2 + [x2[0]], y2 + [y2[0]])
    plt.show()


if __name__ == "__main__":
    figure()
