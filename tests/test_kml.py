import unittest

from src.geography.geography import Point
from src.geography.kml import landing_range_to_kml, parse_launch_site
from src.geography.landing_range import LandingRange, Loop

TEST_LAUNCH_SITE_KML = """<?xml version="1.0" encoding="UTF-8"?>
<kml xmlns="http://www.opengis.net/kml/2.2" xmlns:gx="http://www.google.com/kml/ext/2.2" xmlns:kml="http://www.opengis.net/kml/2.2" xmlns:atom="http://www.w3.org/2005/Atom">
	<Document>
		<name>test.kml</name>
		<open>1</open>
		<Placemark>
			<name>ランチャー</name>
			<Point>
				<coordinates>150,40,0</coordinates>
			</Point>
		</Placemark>
		<Placemark>
			<name>落下可能域</name>
			<styleUrl>#6</styleUrl>
			<Polygon>
				<outerBoundaryIs>
					<LinearRing>
						<tessellate>1</tessellate>
						<coordinates>
							130,30,0
							140,30,0
						</coordinates>
					</LinearRing>
				</outerBoundaryIs>
			</Polygon>
		</Placemark>
	</Document>
</kml>"""  # noqa: E501

expected_landing_range_kml = """<?xml version="1.0" encoding="UTF-8"?>
<kml xmlns="http://www.opengis.net/kml/2.2" xmlns:gx="http://www.google.com/kml/ext/2.2" xmlns:kml="http://www.opengis.net/kml/2.2" xmlns:atom="http://www.w3.org/2005/Atom">
<Document>
<name>test landing range</name>
<open>1</open>
<Placemark>
<name>test loop1</name>
<LineString>
<coordinates>
150,40,0
140,30,0
150,40,0
</coordinates>
</LineString>
</Placemark>
<Placemark>
<name>test loop2</name>
<LineString>
<coordinates>
140,40,0
130,30,0
140,40,0
</coordinates>
</LineString>
</Placemark>
</Document>
</kml>"""  # noqa: E501


class TestKml(unittest.TestCase):
    """KMLファイルのテスト"""

    def test_parse_launch_site(self) -> None:
        """発射地点と落下可能域の読み込みテスト"""
        launch_site = parse_launch_site(TEST_LAUNCH_SITE_KML, "ランチャー", "落下可能域")
        self.assertEqual(launch_site.launch_point.latitude, 40)
        self.assertEqual(launch_site.launch_point.longitude, 150)
        self.assertEqual(len(launch_site.allowed_area), 2)
        self.assertEqual(launch_site.allowed_area[0].latitude, 30)
        self.assertEqual(launch_site.allowed_area[0].longitude, 130)
        self.assertEqual(launch_site.allowed_area[1].latitude, 30)
        self.assertEqual(launch_site.allowed_area[1].longitude, 140)

    def test_landing_range_to_kml(self) -> None:
        """落下可能域のKMLファイルのテスト"""
        landing_range = LandingRange("test landing range", 0, 0)
        landing_range.loops = [
            Loop("test loop1", [Point.from_lat_lon(40, 150, 0, 0), Point.from_lat_lon(30, 140, 0, 0)]),
            Loop("test loop2", [Point.from_lat_lon(40, 140, 0, 0), Point.from_lat_lon(30, 130, 0, 0)]),
        ]
        result = landing_range_to_kml(landing_range)
        self.assertEqual(result, expected_landing_range_kml)
