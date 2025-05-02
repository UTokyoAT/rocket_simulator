from dataclasses import dataclass

from src.geography.geography import Point


@dataclass
class LaunchSite:
    launch_point: Point
    allowed_area: list[Point]

    @classmethod
    def from_lat_lon(
        cls,
        latitude_launch_point: float,
        longitude_launch_point: float,
        allowed_area: list[tuple[float, float]],
    ) -> "LaunchSite":
        launch_point = Point.from_lat_lon(
            latitude_launch_point, longitude_launch_point, latitude_launch_point, longitude_launch_point,
        )
        allowed_area = [
            Point.from_lat_lon(
                latitude,
                longitude,
                latitude_launch_point,
                longitude_launch_point,
            )
            for latitude, longitude in allowed_area
        ]
        return cls(launch_point, allowed_area)

    def points_north(self) -> list[float]:
        return [point.north for point in self.allowed_area]

    def points_east(self) -> list[float]:
        return [point.east for point in self.allowed_area]
