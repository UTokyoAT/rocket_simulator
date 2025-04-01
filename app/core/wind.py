import numpy as np
import typing as t
def wind_velocity_power(reference_height:float, wind_speed:float, exponent:float, wind_direction:float)->t.Callable[[float],np.ndarray]:
    """風速を計算する関数を生成する

    Args:
        reference_height (float): 基準高度
        wind_speed (float): 基準高度での風速
        exponent (float): べき定数
        wind_direction (float): 風上の方位角[deg]

    Returns:
        t.Callable[[float],np.ndarray]: 高度から風速への関数
    """
    def f(height:float)->np.ndarray:
        """高度から風速を計算する

        Args:
            height (float): 高度

        Returns:
            np.ndarray: 風速
        """
        theta = np.deg2rad(wind_direction)
        if height < 0:
            return np.zeros(3)
        return wind_speed * (height / reference_height)**(1/exponent) * np.array([-np.cos(theta),-np.sin(theta),0])
    return f