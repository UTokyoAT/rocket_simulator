import typing as t

import numpy as np
import pandas as pd


def df_to_function_1d(df: pd.DataFrame) -> t.Callable[[float], float]:
    """線形補完によりDataFrameをインデックスから1番目のカラムへの関数に変換する

    Args:
        df (pd.DataFrame): DataFrame

    Returns:
        np.ndarray: 関数
    """
    return lambda x: float(np.interp(x, df.index, df.iloc[:, 0]))


def df_to_function_1d_array(
    df: pd.DataFrame,
) -> t.Callable[[float], np.ndarray]:
    """インデックスから1番目のカラムへの関数をnumpy配列で返す

    DataFrameから線形補間により関数を作成し、結果をnumpy配列として返します。
    注意: 範囲外の値(外挿)に対してはValueErrorが発生します。

    Args:
        df (pd.DataFrame): DataFrame

    Returns:
        t.Callable[[float], np.ndarray]: numpy配列を返す関数

    Raises:
        ValueError: 補間範囲外の値が指定された場合
    """
    # DataFrameからデータを取得
    indices = np.array(df.index)
    values = df.iloc[:, 0].to_numpy()

    min_x = float(indices[0])
    max_x = float(indices[-1])

    def interpolate_array(x: float) -> np.ndarray:
        # x値がインデックスの範囲外の場合はエラー
        if x < min_x or x > max_x:
            err_msg = "補間範囲外の値です"
            raise ValueError(err_msg, x, min_x, max_x)

        # 境界値の場合はその値を返す
        if x == min_x:
            return values[0]
        if x == max_x:
            return values[-1]

        # 補間用のインデックスを検索
        idx = np.searchsorted(indices, x) - 1
        idx_next = idx + 1

        # 補間係数を計算
        t = (x - indices[idx]) / (indices[idx_next] - indices[idx])

        # 線形補間を実行
        return (1 - t) * values[idx] + t * values[idx_next]

    return interpolate_array
