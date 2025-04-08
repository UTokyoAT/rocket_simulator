import config_read
import os
from core import simple_simulation
from concurrent.futures import ProcessPoolExecutor
import matplotlib.pyplot as plt

exponent = 4.5
reference_height = 5


def simulate(wind_direction, wind_speed):
    config = config_read.read(os.path.abspath("config"))
    config.wind.wind_direction = wind_direction
    config.wind.wind_speed = wind_speed
    return simple_simulation.simulate(config, False)


def figure():
    with ProcessPoolExecutor() as e:
        r = list(e.map(simulate, range(0, 360, 45), [6] * 8))
    x = [r.last().position[1] for r in r]
    y = [r.last().position[0] for r in r]
    plt.plot(x + [x[0]], y + [y[0]])
    plt.show()


if __name__ == "__main__":
    figure()
