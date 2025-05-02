import unittest

import numpy as np

from src.geography.geography import Point, from_lat_lon_to_north_east, from_north_east_to_lat_lon


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


class TestPoint(unittest.TestCase):
    """Pointクラスのテスト"""

    def setUp(self) -> None:
        """テストで使用する基準点"""
        self.lat_0 = 36
        self.lon_0 = 140
        self.tolerance = 1e-5

    def test_from_lat_lon(self) -> None:
        """緯度経度からの初期化テスト"""
        # 基準点と同じ座標
        point = Point.from_lat_lon(self.lat_0, self.lon_0, self.lat_0, self.lon_0)
        self.assertAlmostEqual(point.latitude, self.lat_0, delta=self.tolerance)
        self.assertAlmostEqual(point.longitude, self.lon_0, delta=self.tolerance)
        self.assertAlmostEqual(point.north, 0, delta=self.tolerance)
        self.assertAlmostEqual(point.east, 0, delta=self.tolerance)

        # 別の座標
        lat = 36.1
        lon = 140.1
        point = Point.from_lat_lon(lat, lon, self.lat_0, self.lon_0)
        self.assertAlmostEqual(point.latitude, lat, delta=self.tolerance)
        self.assertAlmostEqual(point.longitude, lon, delta=self.tolerance)
        north, east = from_lat_lon_to_north_east(lat, lon, self.lat_0, self.lon_0)
        self.assertAlmostEqual(point.north, north, delta=self.tolerance)
        self.assertAlmostEqual(point.east, east, delta=self.tolerance)

    def test_from_north_east(self) -> None:
        """北東座標からの初期化テスト"""
        # 基準点からの距離ゼロ
        point = Point.from_north_east(0, 0, self.lat_0, self.lon_0)
        self.assertAlmostEqual(point.latitude, self.lat_0, delta=self.tolerance)
        self.assertAlmostEqual(point.longitude, self.lon_0, delta=self.tolerance)
        self.assertAlmostEqual(point.north, 0, delta=self.tolerance)
        self.assertAlmostEqual(point.east, 0, delta=self.tolerance)

        # 別の座標
        north = 1000
        east = 2000
        point = Point.from_north_east(north, east, self.lat_0, self.lon_0)
        self.assertAlmostEqual(point.north, north, delta=self.tolerance)
        self.assertAlmostEqual(point.east, east, delta=self.tolerance)
        lat, lon = from_north_east_to_lat_lon(north, east, self.lat_0, self.lon_0)
        self.assertAlmostEqual(point.latitude, lat, delta=self.tolerance)
        self.assertAlmostEqual(point.longitude, lon, delta=self.tolerance)

    def test_to_lat_lon(self) -> None:
        """緯度経度の取得テスト"""
        lat = 36.1
        lon = 140.1
        point = Point.from_lat_lon(lat, lon, self.lat_0, self.lon_0)
        self.assertAlmostEqual(point.latitude, lat, delta=self.tolerance)
        self.assertAlmostEqual(point.longitude, lon, delta=self.tolerance)

    def test_to_north_east(self) -> None:
        """北東座標の取得テスト"""
        north = 1000
        east = 2000
        point = Point.from_north_east(north, east, self.lat_0, self.lon_0)
        self.assertAlmostEqual(point.north, north, delta=self.tolerance)
        self.assertAlmostEqual(point.east, east, delta=self.tolerance)


if __name__ == "__main__":
    unittest.main()
