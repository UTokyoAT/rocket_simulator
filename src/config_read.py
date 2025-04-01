import pandas as pd
from core.simple_simulation import Config
from core import interpolation
from core import wind
from core.inertia_tensor import InertiaTensor
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
    mass_func = interpolation.df_to_function_1d(mass_df)
    thrust_func = interpolation.df_to_function_1d(thrust_df)
    wind_func = wind.wind_velocity_power(
        js["wind_reference_height"],
        js["wind_speed"],
        js["wind_exponent"],
        js["wind_direction"],
    )
    return Config(
        mass_func,
        wind_func,
        thrust_func,
        js["CA"],
        js["CN_alpha"],
        js["body_diameter"] ** 2 / 4 * np.pi,
        np.array(js["wind_center"]),
        js["dt"],
        js["launcher_length"],
        InertiaTensor(
            js["I_xx"], js["I_yy"], js["I_zz"], js["I_xy"], js["I_zy"], js["I_xz"]
        ),
        js["first_elevation"],
        js["first_azimuth"],
        js["first_roll"],
        js["propellant_CG_distance"],
        js["nozzle_CG_distance"],
        lambda t: js["m_dot"],
        js["roll_damping_coefficient"],
        js["pitch_damping_coefficient"],
        js["yaw_damping_coefficient"],
        js["overall_length"],
    )
