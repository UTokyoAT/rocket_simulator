import numpy as np
import pymap3d as pm


def from_north_east_to_lat_lon(north: float, east: float, lat_0: float, lon_0: float) -> tuple[float, float]:
    """
    北方向と東方向の移動距離から緯度経度を計算する。

    Args:
        north (float): 北方向の移動距離(m)
        east (float): 東方向の移動距離(m)
        lat_0 (float): 出発点の緯度(deg)
        lon_0 (float): 出発点の経度(deg)

    Returns:
        tuple[float, float]: 緯度(deg)と経度(deg)
    """
    # pymap3dのned2geodetic関数を使用して北東距離から緯度経度を計算
    lat, lon, _ = pm.ned2geodetic(north, east, 0, lat_0, lon_0, 0)
    return lat, lon


def from_lat_lon_to_north_east(lat: float, lon: float, lat_0: float, lon_0: float) -> tuple[float, float]:
    """
    緯度経度から北方向と東方向の移動距離を計算する。

    Args:
        lat (float): 目標地点の緯度(deg)
        lon (float): 目標地点の経度(deg)
        lat_0 (float): 基準点の緯度(deg)
        lon_0 (float): 基準点の経度(deg)

    Returns:
        tuple[float, float]: 北方向と東方向の移動距離(m)
    """
    # pymap3dのgeodetic2ned関数を使用して緯度経度から北東距離を計算
    north, east, _ = pm.geodetic2ned(lat, lon, 0, lat_0, lon_0, 0)
    return north, east

