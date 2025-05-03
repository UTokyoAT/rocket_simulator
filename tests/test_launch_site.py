import unittest

from src.geography.geography import from_lat_lon_to_north_east
from src.geography.launch_site import LaunchSite


class TestLaunchSite(unittest.TestCase):
    """LaunchSiteクラスのテスト"""

    def setUp(self) -> None:
        """テストで使用する基準点"""
        self.lat_0 = 36
        self.lon_0 = 140
        self.tolerance = 1e-5

    def test_from_lat_lon(self) -> None:
        """緯度経度からの初期化テスト"""
        # 発射地点と許可エリアの座標
        launch_lat = 36.1
        launch_lon = 140.1
        allowed_area = [
            (36.2, 140.2),
            (36.2, 140.0),
            (36.0, 140.0),
            (36.0, 140.2),
        ]

        # LaunchSiteの作成
        launch_site = LaunchSite.from_lat_lon(launch_lat, launch_lon, allowed_area)

        # 発射地点の確認
        self.assertAlmostEqual(launch_site.launch_point.latitude, launch_lat, delta=self.tolerance)
        self.assertAlmostEqual(launch_site.launch_point.longitude, launch_lon, delta=self.tolerance)
        self.assertAlmostEqual(launch_site.launch_point.north, 0, delta=self.tolerance)
        self.assertAlmostEqual(launch_site.launch_point.east, 0, delta=self.tolerance)

        # 許可エリアの確認
        self.assertEqual(len(launch_site.allowed_area), len(allowed_area))
        for point, (lat, lon) in zip(launch_site.allowed_area, allowed_area, strict=False):
            self.assertAlmostEqual(point.latitude, lat, delta=self.tolerance)
            self.assertAlmostEqual(point.longitude, lon, delta=self.tolerance)
            north, east = from_lat_lon_to_north_east(lat, lon, launch_lat, launch_lon)
            self.assertAlmostEqual(point.north, north, delta=self.tolerance)
            self.assertAlmostEqual(point.east, east, delta=self.tolerance)

    def test_points_north_east(self) -> None:
        """points_northとpoints_eastのテスト"""
        # 発射地点と許可エリアの座標
        launch_lat = 36.1
        launch_lon = 140.1
        allowed_area = [
            (36.2, 140.2),  # 北東
            (36.2, 140.0),  # 北西
            (36.0, 140.0),  # 南西
            (36.0, 140.2),  # 南東
        ]

        # LaunchSiteの作成
        launch_site = LaunchSite.from_lat_lon(launch_lat, launch_lon, allowed_area)

        # points_northの確認
        north_points = launch_site.points_north()
        self.assertEqual(len(north_points), len(allowed_area))
        for north, (lat, lon) in zip(north_points, allowed_area, strict=True):
            expected_north, _ = from_lat_lon_to_north_east(lat, lon, launch_lat, launch_lon)
            self.assertAlmostEqual(north, expected_north, delta=self.tolerance)

        # points_eastの確認
        east_points = launch_site.points_east()
        self.assertEqual(len(east_points), len(allowed_area))
        for east, (lat, lon) in zip(east_points, allowed_area, strict=True):
            _, expected_east = from_lat_lon_to_north_east(lat, lon, launch_lat, launch_lon)
            self.assertAlmostEqual(east, expected_east, delta=self.tolerance)


if __name__ == "__main__":
    unittest.main()
