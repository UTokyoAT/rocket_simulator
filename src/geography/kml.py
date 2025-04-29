import re

from src.geography.launch_site import LaunchSite

re_place_mark = re.compile(r"<Placemark>(.*?)</Placemark>", re.DOTALL)
re_coordinates = re.compile(r"<coordinates>(.*?)</coordinates>", re.DOTALL)
re_name = re.compile(r"<name>(.*?)</name>", re.DOTALL)

def lat_lon(line: str) -> tuple[float, float]:
    splitted = line.split(",")
    return float(splitted[1].strip()), float(splitted[0].strip())


def parse_launch_site(kml_str: str, launch_point_name: str, allowed_area_name: str) -> LaunchSite:
    place_marks = re_place_mark.findall(kml_str)
    launch_point = next((pm for pm in place_marks if re_name.search(pm).group(1).strip() == launch_point_name), None)
    allowed_area = next((pm for pm in place_marks if re_name.search(pm).group(1).strip() == allowed_area_name), None)
    if launch_point is None:
        msg = f"発射地点 '{launch_point_name}' が見つかりません"
        raise ValueError(msg)
    if allowed_area is None:
        msg = f"落下可能域 '{allowed_area_name}' が見つかりません"
        raise ValueError(msg)
    launch_point_coordinates = re_coordinates.search(launch_point).group(1).strip()
    allowed_area_coordinates = re_coordinates.search(allowed_area).group(1).strip()
    launch_point_lat, launch_point_lon = lat_lon(launch_point_coordinates)
    allowed_area_lat_lon = [lat_lon(line) for line in allowed_area_coordinates.split("\n")]
    return LaunchSite.from_lat_lon(launch_point_lat, launch_point_lon, allowed_area_lat_lon)
