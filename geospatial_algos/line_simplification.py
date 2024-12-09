"""
The Douglas–Peucker, or iterative end-point fit, algorithm smooths polylines
(lines that are composed of linear line segments) by reducing the number of points.
The simplified curve preserves the rough shape of the original curve by preserving
the subset of points that exceed a coarsening threshold parameter called epsilon.

Resources:
- https://cartography-playground.gitlab.io/playgrounds/douglas-peucker-algorithm/
- https://medium.com/@indemfeld/the-ramer-douglas-peucker-algorithm-d542807093e7
"""
