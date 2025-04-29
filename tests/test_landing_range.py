import unittest

from src.geography.geography import from_north_east_to_lat_lon
from src.geography.landing_range import LandingRange


class TestLandingRange(unittest.TestCase):
    """LandingRangeクラスのテスト"""

    def setUp(self) -> None:
        """テストで使用する基準点"""
        self.lat_0 = 36
        self.lon_0 = 140
        self.tolerance = 1e-5

    def test_init(self) -> None:
        """初期化テスト"""
        # LandingRangeの作成
        landing_range = LandingRange(self.lat_0, self.lon_0)

        # 発射地点の確認
        self.assertAlmostEqual(landing_range.launch_point.latitude, self.lat_0, delta=self.tolerance)
        self.assertAlmostEqual(landing_range.launch_point.longitude, self.lon_0, delta=self.tolerance)
        self.assertAlmostEqual(landing_range.launch_point.north, 0, delta=self.tolerance)
        self.assertAlmostEqual(landing_range.launch_point.east, 0, delta=self.tolerance)

        # ループの確認
        self.assertEqual(len(landing_range.loops), 0)

    def test_append_loop(self) -> None:
        """ループの追加テスト"""
        # LandingRangeの作成
        landing_range = LandingRange(self.lat_0, self.lon_0)

        # ループの座標
        loop_name = "Test Loop"
        points_north_east = [
            (1000, 1000),
            (1000, -1000),
            (-1000, -1000),
            (-1000, 1000)
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


if __name__ == "__main__":
    unittest.main()
