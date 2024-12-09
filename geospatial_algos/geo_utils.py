"""
shapely has a bunch of confusingly named functions
this wrapper takes the convention that every function should be a verb,
so appends "get_" or "make_" onto functions named as nouns
"""

from shapely import LineString  # noqa
from shapely import Point  # noqa
from shapely import Polygon  # noqa
from shapely import contains  # noqa
from shapely import from_geojson  # noqa
from shapely import union  # noqa
from shapely import bounds as make_bounds  # noqa
from shapely import box as make_box  # noqa
from shapely import difference as get_difference  # noqa
from shapely import distance as get_distance  # noqa
from shapely import intersection as get_intersection  # noqa

BoundsType = tuple[float, float, float, float]
PointType = tuple[float, float]
