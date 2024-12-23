import geojson
import pytest

from geospatial_algos.geospatial_algos import convex_hull  # type: ignore


@pytest.fixture
def star_house():
    """
    STAR house was notable for many reasons —
    it was the first LGBT youth shelter in North America,
    the first trans woman of color-led organization in the US,
    and the first trans sex worker labor organization.

    In the 70s the legal rent for 213 was $310 a month,
    but the owner of the building told Sylvia Rivera and
    Marsha P. Johnson he'd take $200.

    In 2016, a unit in the building sold for $3,399,000.

    Resources:
    - https://www.villagepreservation.org/2020/10/29/revolutionaries-on-east-second-street-the-star-house  # noqa
    - https://streeteasy.com/building/213-east-2-street-new_york/7
    """
    return {
        "type": "Feature",
        "properties": {"name": "STAR House"},
        "geometry": {
            "coordinates": [
                [
                    [-73.98307446433638, 40.72176527799846],
                    [-73.98315564213495, 40.72180031349515],
                    [-73.9831273267312, 40.72170567587946],
                    [-73.98326651540587, 40.72159097703323],
                    [-73.98314301846652, 40.72164349109397],
                    [-73.983146993549, 40.72154241600467],
                    [-73.98306244470285, 40.721684464595995],
                    [-73.98295416149796, 40.721714646920816],
                    [-73.98302089883865, 40.72174273423863],
                    [-73.9829906752835, 40.721823183839746],
                    [-73.98307446433638, 40.72176527799846],
                ]
            ],
            "type": "Polygon",
        },
    }


def test_check_convex__is_convex():
    point_1, point_2, point_3 = (
        [-73.983146993549, 40.72154241600467],
        [-73.98326651540587, 40.72159097703323],
        [-73.98315564213495, 40.72180031349515],
    )
    assert convex_hull.check_convex(point_1, point_2, point_3) is True


def test_check_convex__is_concave():
    point_1, point_2, point_3 = (
        [-73.98315564213495, 40.72180031349515],
        [-73.98314301846652, 40.72164349109397],
        [-73.9831273267312, 40.72170567587946],
    )
    assert convex_hull.check_convex(point_1, point_2, point_3) is False


def test_convex_hull(star_house):
    hull = convex_hull.convex_hull(star_house["geometry"]["coordinates"][0])
    assert geojson.loads(geojson.dumps(hull)) == {
        "coordinates": [
            [
                [-73.983147, 40.721542],
                [-73.983267, 40.721591],
                [-73.983156, 40.7218],
                [-73.982991, 40.721823],
                [-73.982954, 40.721715],
                [-73.983147, 40.721542],
            ]
        ],
        "type": "Polygon",
    }
