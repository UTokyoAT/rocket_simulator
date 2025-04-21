import numpy as np
import typing
import pandas as pd
from . import interpolation


def thrust_end_time(thrust_df: pd.DataFrame) -> float:
    return thrust_df[thrust_df["thrust"] < 1e-10].index[-1]["time"]


def create_gravity_center_function_from_dataframe(
    first_gravity_center: np.ndarray,
    end_gravity_center: np.ndarray,
    thrust_df: pd.DataFrame,
) -> typing.Callable[[float], np.ndarray]:
    """DataFrameから重心位置を計算する関数を作成する

    Args:
        first_gravity_center (np.ndarray): 初期重心位置
        end_gravity_center (np.ndarray): 最終重心位置
        thrust_df (pd.DataFrame): 推力データフレーム

    Returns:
        typing.Callable[[float], np.ndarray]: 時間から重心位置を計算する関数
    """
    # 閾値
    thrust_end_time_ = thrust_end_time(thrust_df)

    # 重心位置のデータフレームを作成
    gravity_center_df = pd.DataFrame(
        {
            "time": [0, thrust_end_time_, 1000],
            "gravity_center": [
                first_gravity_center,
                end_gravity_center,
                end_gravity_center,
            ],
        }
    ).set_index("time")

    # 補間関数を取得
    interp_func = interpolation.df_to_function_1d_array(gravity_center_df)

    # エラー処理を追加
    def gravity_center_func(time: float) -> np.ndarray:
        try:
            return interp_func(time)
        except ValueError:
            # 範囲外の値の場合は適切な値を返す
            if time < 0:
                return first_gravity_center
            else:
                return end_gravity_center

    return gravity_center_func
