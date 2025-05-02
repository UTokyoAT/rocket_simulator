import unittest

import pandas as pd

from src.geography.geography import from_north_east_to_lat_lon
from src.geography.landing_range import LandingRange, get_last_position
from src.make_report.result_for_report import ResultByLauncherElevation, ResultByWindDirection, ResultByWindSpeed


class TestLandingRange(unittest.TestCase):
    """LandingRangeクラスのテスト"""

    def setUp(self) -> None:
        """テストで使用する基準点"""
        self.name = "Test Landing Range"
        self.lat_0 = 36
        self.lon_0 = 140
        self.tolerance = 1e-5

    def test_init(self) -> None:
        """初期化テスト"""
        # LandingRangeの作成
        landing_range = LandingRange(self.name, self.lat_0, self.lon_0)

        # 発射地点の確認
        self.assertEqual(landing_range.name, self.name)
        self.assertAlmostEqual(landing_range.launch_point.latitude, self.lat_0, delta=self.tolerance)
        self.assertAlmostEqual(landing_range.launch_point.longitude, self.lon_0, delta=self.tolerance)
        self.assertAlmostEqual(landing_range.launch_point.north, 0, delta=self.tolerance)
        self.assertAlmostEqual(landing_range.launch_point.east, 0, delta=self.tolerance)

        # ループの確認
        self.assertEqual(len(landing_range.loops), 0)

    def test_append_loop(self) -> None:
        """ループの追加テスト"""
        # LandingRangeの作成
        landing_range = LandingRange(self.name, self.lat_0, self.lon_0)

        # ループの座標
        loop_name = "Test Loop"
        points_north_east = [
            (1000, 1000),
            (1000, -1000),
            (-1000, -1000),
            (-1000, 1000),
        ]

        # ループの追加
        landing_range.append_loop(points_north_east, loop_name)

        # ループの確認
        self.assertEqual(len(landing_range.loops), 1)
        loop = landing_range.loops[0]
        self.assertEqual(loop.name, loop_name)
        self.assertEqual(len(loop.points), len(points_north_east))

        # 各点の確認
        for point, (north, east) in zip(loop.points, points_north_east, strict=True):
            self.assertAlmostEqual(point.north, north, delta=self.tolerance)
            self.assertAlmostEqual(point.east, east, delta=self.tolerance)
            lat, lon = from_north_east_to_lat_lon(north, east, self.lat_0, self.lon_0)
            self.assertAlmostEqual(point.latitude, lat, delta=self.tolerance)
            self.assertAlmostEqual(point.longitude, lon, delta=self.tolerance)

    def test_get_last_position(self) -> None:
        """get_last_position関数のテスト"""
        # テスト用のDataFrameを作成
        df = pd.DataFrame({
            "position_n": [100, 200, 300],
            "position_e": [400, 500, 600],
        })

        # 最後の位置を取得
        position = get_last_position(df)

        # 位置の確認
        self.assertEqual(position, (300, 600))

    def test_from_result_by_launcher_elevation(self) -> None:
        """from_result_by_launcher_elevationメソッドのテスト"""
        # テスト用のデータを作成
        result = ResultByLauncherElevation(launcher_elevation=45, result=[])

        # 風速5m/sの結果を追加
        wind_speed_result = ResultByWindSpeed(wind_speed=5, result=[])
        # 風向0度の結果を追加
        wind_direction_result = ResultByWindDirection(
            wind_direction=0,
            result_parachute_off=pd.DataFrame({
                "position_n": [100, 200, 300],
                "position_e": [400, 500, 600],
            }),
            result_parachute_on=pd.DataFrame({
                "position_n": [150, 250, 350],
                "position_e": [450, 550, 650],
            }),
        )
        wind_speed_result.result.append(wind_direction_result)
        result.result.append(wind_speed_result)

        # LandingRangeの作成
        landing_range = LandingRange.from_result_by_launcher_elevation(
            self.lat_0,
            self.lon_0,
            result,
        )

        # 名前の確認
        self.assertEqual(landing_range.name, "launcher elevation = 45 deg")

        # ループの確認
        self.assertEqual(len(landing_range.loops), 2)
        loop = landing_range.loops[0]
        self.assertEqual(loop.name, "wind speed = 5 m/s, parachute off")
        loop = landing_range.loops[1]
        self.assertEqual(loop.name, "wind speed = 5 m/s, parachute on")

        self.assertEqual(landing_range.loops[0].points[0].north, 300) #パラシュートなしの結果
        self.assertEqual(landing_range.loops[0].points[0].east, 600) #パラシュートなしの結果
        self.assertEqual(landing_range.loops[1].points[0].north, 350) #パラシュートありの結果
        self.assertEqual(landing_range.loops[1].points[0].east, 650) #パラシュートありの結果


if __name__ == "__main__":
    unittest.main()
