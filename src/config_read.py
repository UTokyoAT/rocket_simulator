import pandas as pd
from .core.config import Config, WindPowerLow
import json
import numpy as np
import os


def read(folder_path: str) -> Config:
    """フォルダから設定を読み込む

    Args:
        folder_path (str): フォルダのパス

    Returns:
        Config: 設定
    """
    mass_df = pd.read_csv(os.path.join(folder_path, "mass.csv"), index_col=0)
    thrust_df = pd.read_csv(os.path.join(folder_path, "thrust.csv"), index_col=0)
    with open(os.path.join(folder_path, "config.json"), "r") as file:
        js = json.load(file)
    wind = WindPowerLow(
        js["wind_reference_height"],
        js["wind_speed"],
        js["wind_exponent"],
        js["wind_direction"],
    )
    return Config(
        mass_df,
        wind,
        thrust_df,
        js["CA"],
        js["CN_alpha"],
        js["body_diameter"] ** 2 / 4 * np.pi,
        np.array(js["wind_center"]),
        js["dt"],
        js["launcher_length"],
        js["I_xx"],
        js["I_yy"],
        js["I_zz"],
        js["I_zy"],
        js["I_xz"],
        js["I_xy"],
        js["first_elevation"],
        js["first_azimuth"],
        js["first_roll"],
        js["parachute_terminal_velocity"],
        js["parachute_delay_time"],
    )
