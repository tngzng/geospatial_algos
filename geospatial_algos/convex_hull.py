"""
Resources:
- https://medium.com/@errazkim/computing-the-convex-hull-in-python-60a6087e0faa
- https://medium.com/@pascal.sommer.ch/a-gentle-introduction-to-the-convex-hull-problem-62dfcabee90c
- https://www.mathsisfun.com/sine-cosine-tangent.html
- https://www.mathsisfun.com/algebra/vectors-cross-product.html
- https://www.geeksforgeeks.org/check-if-given-polygon-is-a-convex-polygon-or-not/
"""

import numpy as np

from .geo_utils import PointType, Polygon


def make_vector(point_1: PointType, point_2: PointType) -> PointType:
    return point_2[0] - point_1[0], point_2[1] - point_1[1]


def check_convex(point_1: PointType, point_2: PointType, point_3: PointType) -> bool:
    vector_1 = make_vector(point_1, point_2)
    vector_2 = make_vector(point_1, point_3)
    cross_product = np.cross(vector_1, vector_2)
    # In cases where both input vectors have dimension 2,
    # the z-component of the cross product is returned
    # From: https://numpy.org/doc/stable/reference/generated/numpy.cross.html#numpy.cross
    return bool(cross_product < 0)


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
    # (if duplicates, order by increasing distance from anchor point)
    points_by_angle: dict[float, PointType] = {}
    for point in points:
        x_dist = anchor[0] - point[0]
        y_dist = anchor[1] - point[1]
        angle = np.arctan(x_dist / y_dist)
        points_by_angle[angle] = point

    sorted_angles = sorted(points_by_angle.keys())

    # Initialize the hull with the anchor point and the first element in the sorted list
    hull: list[PointType] = [anchor, points_by_angle[sorted_angles[0]]]

    # Iterate over each point in the sorted list and determine if traversing to it from
    # the prior two points in the hull results in a concave or convex shape
    for angle in sorted_angles[1:]:
        point = points_by_angle[angle]
        # If shape is convex with the preceeding two points, add it to the hull
        if check_convex(hull[-2], hull[-1], point):
            hull.append(point)
        # If shape is concave with the preceeding two points, remove the middle point
        # and add the current point to the hull
        else:
            hull.pop()
            hull.append(point)

    return Polygon(hull)
