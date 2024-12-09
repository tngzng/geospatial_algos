"""
The Douglas–Peucker, or iterative end-point fit, algorithm smooths polylines
(lines that are composed of linear line segments) by reducing the number of points.
The simplified curve preserves the rough shape of the original curve by preserving
the subset of points that exceed a coarsening threshold parameter called epsilon.

Resources:
- https://cartography-playground.gitlab.io/playgrounds/douglas-peucker-algorithm/
- https://medium.com/@indemfeld/the-ramer-douglas-peucker-algorithm-d542807093e7
"""

from .geo_utils import LineString, Point, PointType, get_distance


def _simplify(line_coords: list[PointType], epsilon: float = 0.0) -> list[PointType]:
    if len(line_coords) <= 2:
        return line_coords

    first, last = line_coords[0], line_coords[-1]
    baseline = LineString([first, last])

    notable_point_idx = next(
        (
            idx
            for idx, coord in enumerate(line_coords)
            if get_distance(baseline, Point(coord)) > epsilon
        ),
        None,
    )
    if notable_point_idx:
        left = _simplify([first, line_coords[notable_point_idx]], epsilon)
        right = _simplify(line_coords[notable_point_idx:], epsilon)
        return left + right[1:]

    else:
        return [first, last]


def simplify(polyline: LineString, epsilon: float = 0.0) -> LineString:
    simplified_points = _simplify(polyline.coords, epsilon)
    return LineString(simplified_points)
