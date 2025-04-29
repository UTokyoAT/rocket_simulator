import unittest

import numpy as np

from src.make_report.geography import from_lat_lon_to_north_east, from_north_east_to_lat_lon


class TestGeography(unittest.TestCase):
    """地理座標変換関数のテスト"""

    def setUp(self) -> None:
        """テストで使用する基準点"""
        self.lat_0 = 36
        self.lon_0 = 140

    def test_zero_distance(self) -> None:
        """距離ゼロでの変換テスト"""
        # 変換
        lat, lon = from_north_east_to_lat_lon(0, 0, self.lat_0, self.lon_0)

        # 基準点と同じ座標になるはず
        self.assertAlmostEqual(lat, self.lat_0)
        self.assertAlmostEqual(lon, self.lon_0)

        # 逆変換
        north, east = from_lat_lon_to_north_east(lat, lon, self.lat_0, self.lon_0)

        # ゼロになるはず
        self.assertAlmostEqual(north, 0)
        self.assertAlmostEqual(east, 0)

    def test_transform(self) -> None:
        distance = 14293.818
        azimuth = np.deg2rad(39.04945)
        n = distance * np.cos(azimuth)
        e = distance * np.sin(azimuth)
        lat, lon = from_north_east_to_lat_lon(n, e, self.lat_0, self.lon_0)
        expected_lat = 36.1
        expected_lon = 140.1
        tolerance = 1e-5
        self.assertAlmostEqual(lat, expected_lat, delta=tolerance)
        self.assertAlmostEqual(lon, expected_lon, delta=tolerance)

        n_reverse, e_reverse = from_lat_lon_to_north_east(expected_lat, expected_lon, self.lat_0, self.lon_0)
        tolerance = 1e-1
        self.assertAlmostEqual(n_reverse, n, delta=tolerance)
        self.assertAlmostEqual(e_reverse, e, delta=tolerance)

if __name__ == "__main__":
    unittest.main()
