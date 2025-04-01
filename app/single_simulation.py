import pandas as pd
import config_read
from core.rocket_state import RocketState
from core import simple_simulation
import itertools
import os
import matplotlib.pyplot as plt
import numpy as np
log = pd.read_csv("flight_flash_log.csv",index_col=0)
log = log[(970000 < log.index) & (log.index < 990000)]
def simulate()->list[list[tuple[float,RocketState]]]:
    """シミュレーションを行う

    Returns:
        list[list[tuple[float,RocketState]]]: 時刻とロケットの状態の組のリストをモードごとに格納したリスト
    """
    config = config_read.read(os.path.abspath('config'))
    return simple_simulation.simulate(config,False)

def max_altitude(result:list[list[tuple[float,RocketState]]])->float:
    """最大高度を求める

    Args:
        simulation (list[tuple[float,RocketState]]): シミュレーション結果

    Returns:
        float: 最大高度
    """
    return max([-result[1].position[2] for result in itertools.chain(*result)])
def figure(result):
    for r in result:
        t = [x[0] for x in r]
        plt.plot(t,[-x[1].position[2] for x in r],label="altitude")
        plt.plot(t,[x[1].position[0] for x in r],label="x")
        plt.plot(t,[x[1].position[1] for x in r],label="y")
    plt.legend()
    plt.grid()
    plt.title("position")
    plt.show()
    plt.clf()
    for r in result:
        t = [x[0] for x in r]
        plt.plot(t,[x[1].velocity[2] for x in r],label="z")
        plt.plot(t,[x[1].velocity[0] for x in r],label="x")
        plt.plot(t,[x[1].velocity[1] for x in r],label="y")
    plt.legend()
    plt.grid()
    plt.title("velocity")
    plt.show()
    plt.clf()
    for r in result:
        t = [x[0] for x in r if x[0] < 500]
        plt.plot(t,[x[1].rotation[1] for x in r][0:len(t)],label="pitch_sim")
        # plt.plot(t,[x[1].rotation[2] for x in r][0:len(t)],label="yaw_sim")
        # plt.plot(t,[x[1].rotation[0] for x in r][0:len(t)],label="roll_sim")
    plt.plot(log.index / 1000 - 970.9, -log["x_gyro_raw"]*0.003815/180*np.pi,label="x")
    plt.plot(log.index / 1000 - 970.9, -log["y_gyro_raw"]*0.003815/180*np.pi,label="y")
    plt.legend()
    plt.grid()
    plt.title("rotation")
    plt.show()
    plt.clf()


r = simulate()
figure(r)
print(max_altitude(r))
for r_ in r:
    t = [x[0] for x in r_ if x[0] < 8]
    plt.plot(t,[(x[1].rotation[1]**2 + x[1].rotation[2]**2)**0.5 for x in r_][:len(t)],label="simulation")
plt.grid()
data = pd.read_csv("rotation.csv",index_col=0)
plt.plot(data.index / 1000 - 971.3, data["r"]*0.003815/180*np.pi,label="measurement")
plt.xlabel("Time [s]")
plt.ylabel("Rotation [rad/s]")
plt.legend()
plt.show()
plt.clf()