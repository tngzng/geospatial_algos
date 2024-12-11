"""
Resources:
- https://medium.com/@errazkim/computing-the-convex-hull-in-python-60a6087e0faa
- https://www.mathsisfun.com/sine-cosine-tangent.html
- https://www.mathsisfun.com/algebra/vectors-cross-product.html
"""

import numpy as np

from .geo_utils import PointType, Polygon


def convex_hull(points: list[PointType]) -> Polygon:
    # Find the point anchor point with the lowest y-coordinate
    # (if duplicates, choose the one with lowest x-coordinate)
    min_point = points[0]
    for point in points:
        if point[1] < min_point[1]:
            min_point = point
        if point[1] == min_point[1]:
            if point[0] < min_point[0]:
                min_point = point

    anchor = min_point
    points = [p for p in points if p != anchor]
    # Sort the remaining points in order of increasing polar angle from the anchor point
    # (if duplicates, order by increasing distance from P)
    points_by_angle: dict[float, PointType] = {}
    for point in points:
        x_dist = anchor[0] - point[0]
        y_dist = anchor[1] - point[1]
        angle = np.arctan(x_dist / y_dist)
        points_by_angle[angle] = point

    sorted_angles = sorted(points_by_angle.keys())

    # Initialize the hull with the anchor point P and the first element in the sorted list
    hull: list[PointType] = [anchor, points_by_angle[sorted_angles[0]]]

    # Iterate over each point in the sorted list and determine if traversing to it from
    # the prior two points in the hull results in a concave or convex shape
    for angle in sorted_angles[1:]:
        point = points_by_angle[angle]
        # TODO: If shape is concave with the preceeding two points, add it to the hull

        # TODO: If shape is convex with the preceeding two points, remove the middle point
        # and add the current point to the hull

    return hull
