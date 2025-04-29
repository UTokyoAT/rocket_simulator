from dataclasses import dataclass

from src.geography.geography import Point


@dataclass
class Loop:
    name: str
    points: list[Point]


@dataclass
class LandingRange:
    launch_point: Point
    loops: list[Loop]

    def __init__(self, launch_point_latitude: float, launch_point_longitude: float) -> None:
        self.launch_point = Point.from_lat_lon(launch_point_latitude, launch_point_longitude, launch_point_latitude, launch_point_longitude)
        self.loops = []

    def append_loop(self, points_north_east: list[tuple[float, float]], name: str) -> None:
        points = [Point.from_north_east(north, east, self.launch_point.latitude, self.launch_point.longitude) for north, east in points_north_east]
        self.loops.append(Loop(name, points))
