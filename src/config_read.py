import pandas as pd
from .core.config import Config, WindPowerLow
import json
import numpy as np
from pathlib import Path


def read(folder_path: Path) -> Config:
    """フォルダから設定を読み込む

    Args:
        folder_path (Path): フォルダのパス

    Returns:
        Config: 設定
    """
    mass_path = folder_path / "mass.csv"
    thrust_path = folder_path / "thrust.csv"
    config_path = folder_path / "config.json"

    mass_df = pd.read_csv(mass_path, index_col=0)
    thrust_df = pd.read_csv(thrust_path, index_col=0)
    with open(config_path, "r") as file:
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
        np.array(js["first_gravity_center"]),
        np.array(js["end_gravity_center"]),
    )
