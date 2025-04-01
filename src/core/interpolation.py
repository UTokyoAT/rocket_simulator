import numpy as np
import pandas as pd
import typing as t

def df_to_function_1d(df:pd.DataFrame)->t.Callable[[float],float]:
    """線形補完によりDataFrameをインデックスから1番目のカラムへの関数に変換する

    Args:
        df (pd.DataFrame): DataFrame

    Returns:
        np.ndarray: 関数
    """
    return lambda x: float(np.interp(x,df.index,df.iloc[:,0]))