"""
The Douglas–Peucker, or iterative end-point fit, algorithm smooths polylines
(lines that are composed of linear line segments) by reducing the number of points.
The simplified curve preserves the rough shape of the original curve by preserving
the subset of points that exceed a coarsening threshold parameter called epsilon.

Resources:
- https://cartography-playground.gitlab.io/playgrounds/douglas-peucker-algorithm/
- https://medium.com/@indemfeld/the-ramer-douglas-peucker-algorithm-d542807093e7
"""

from .geo_utils import LineString


def simplify(polyline: LineString, epsilon: float = 0.0) -> LineString:
    pass
    # take first and last point in polyline
    # define the baseline as a new line from those two points
    # for all points in the polyline, identify the
    # first point (notable point or significant point or good point)
    # whose distance from the baseline exceeds epsilon
    # keep that point and discard intermediary points
    # (points between the first point in the polyline
    # and the notable point that exceeded the baseline)
    # if no notable point is found, the geometry has been simplified!
    # if a notable point is found, make two new polylines
    #   one starting with the notable point and
    #   ending with the last point in the original polyline
    #
    #   one starting with the first point in the original polyline
    #   and ending with the notable point

    #   simplify the two new polylines
