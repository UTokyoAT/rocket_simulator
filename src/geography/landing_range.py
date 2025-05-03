from dataclasses import dataclass

import pandas as pd

from src.geography.geography import Point
from src.make_report.result_for_report import ResultByLauncherElevation


@dataclass
class Loop:
    name: str
    points: list[Point]


def get_last_position(df: pd.DataFrame) -> tuple[float, float]:
    """DataFrameの最後の行から位置を取得する

    Args:
        df: 位置情報を含むDataFrame

    Returns:
        tuple[float, float]: 最後の行の位置((north, east)の形式)
    """
    last_row = df.iloc[-1]
    return (last_row["position_n"], last_row["position_e"])


@dataclass
class LandingRange:
    name: str
    launch_point: Point
    loops: list[Loop]

    def __init__(self, name: str, launch_point_latitude: float, launch_point_longitude: float) -> None:
        self.name = name
        self.launch_point = Point.from_lat_lon(
            launch_point_latitude,
            launch_point_longitude,
            launch_point_latitude,
            launch_point_longitude,
        )
        self.loops = []

    def append_loop(self, points_north_east: list[tuple[float, float]], name: str) -> None:
        points = [
            Point.from_north_east(
                north,
                east,
                self.launch_point.latitude,
                self.launch_point.longitude,
            )
            for north, east in points_north_east
        ]
        self.loops.append(Loop(name, points))

    @classmethod
    def from_result_by_launcher_elevation(
        cls,
        launch_point_latitude: float,
        launch_point_longitude: float,
        result: ResultByLauncherElevation,
    ) -> "LandingRange":
        """ResultByLauncherElevationからLandingRangeを作成する

        Args:
            name: 着陸範囲の名前
            launch_point_latitude: 発射地点の緯度
            launch_point_longitude: 発射地点の経度
            result: 発射角度ごとの結果

        Returns:
            LandingRange: 作成された着陸範囲
        """
        name = f"launcher elevation = {result.launcher_elevation} deg"
        landing_range = cls(name, launch_point_latitude, launch_point_longitude)

        # 各風速ごとにループを作成
        for wind_speed_result in result.result:
            # 各風向の結果を集める
            points = [
                get_last_position(wind_direction_result.result_parachute_off)
                for wind_direction_result in wind_speed_result.result
            ]
            landing_range.append_loop(points, f"wind speed = {wind_speed_result.wind_speed} m/s, parachute off")
            points = [
                get_last_position(wind_direction_result.result_parachute_on)
                for wind_direction_result in wind_speed_result.result
            ]
            landing_range.append_loop(points, f"wind speed = {wind_speed_result.wind_speed} m/s, parachute on")

        return landing_range
