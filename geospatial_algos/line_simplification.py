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


def _simplify(
    polyline: LineString, simplified_points: list[PointType], epsilon: float = 0.0
) -> None:
    first, last = polyline.coords[0], polyline.coords[-1]
    baseline = LineString([first, last])

    for i, point in enumerate(polyline.coords):
        if get_distance(baseline, Point(point)) > epsilon:
            simplified_points.append(point)
            # TODO: figure out how to handle correct ordering of points
            # may have to return line segments from recursive functions and
            # stitch them together correctly in the end
            # depending on if they were recursed from the left or right sides...
            if len(polyline.coords[0:i]) > 2:
                _simplify(LineString(polyline.coords[0:i]), simplified_points, epsilon)
            if len(polyline.coords[i:-1]) > 2:
                _simplify(LineString(polyline.coords[i:-1]), simplified_points, epsilon)


def simplify(polyline: LineString, epsilon: float = 0.0) -> LineString:
    first, last = polyline.coords[0], polyline.coords[-1]
    simplified_points: list[PointType] = [first]
    _simplify(polyline, simplified_points, epsilon)
    simplified_points.append(last)
    return LineString(simplified_points)
