import pytest

from geospatial_algos.geospatial_algos import geo_utils  # type: ignore
from geospatial_algos.geospatial_algos import line_simplification  # type: ignore


@pytest.fixture
def bk_bridge_park():
    return {
        "type": "Feature",
        "properties": {"name": "Brooklyn Bridge Park"},
        "geometry": {
            "coordinates": [
                [-73.99559380060667, 40.703125074967176],
                [-73.99619710514658, 40.703353756788744],
                [-73.9979693122329, 40.701524280231325],
                [-73.99668729008492, 40.70100973089589],
                [-73.99732830115892, 40.699608993122524],
                [-73.99940216051516, 40.70029507244689],
                [-73.9998923454542, 40.6994374721873],
                [-73.9979693122329, 40.69860844810765],
                [-73.99834637757033, 40.69806528880608],
                [-74.00030711732505, 40.69872279686993],
                [-74.00083500879747, 40.69786517636845],
                [-73.99872344290776, 40.69712189633623],
                [-74.00026941079162, 40.69497777285565],
                [-74.00238097668131, 40.695692488349806],
                [-74.0029465746878, 40.69477765114365],
                [-74.00091042186496, 40.69406292583548],
                [-74.00113386528426, 40.693283611236836],
                [-74.0033236107992, 40.69402904278206],
                [-74.00372580895535, 40.6932158443193],
                [-74.0016701294919, 40.69260593895913],
                [-74.00200981846702, 40.6918594825047],
                [-74.00442196486846, 40.69250430307761],
                [-74.00474667688417, 40.691730517641275],
                [-74.00069550792706, 40.69061671979671],
                [-74.00105114489692, 40.68997188095611],
                [-74.00528786357721, 40.69106224116828],
                [-74.00565896302358, 40.69024154159422],
                [-74.00340144139119, 40.689596699123],
                [-74.00380346579115, 40.68898702413844],
                [-74.00635477448567, 40.689631872509466],
                [-74.00665582556881, 40.68884001829494],
                [-74.00466862153195, 40.68819423517047],
                [-74.0049930630073, 40.68757919780549],
                [-74.00738581888832, 40.68822498688996],
                [-74.00771026036368, 40.68748694171143],
                [-74.00552028040511, 40.68681039311673],
                [-74.00579749569894, 40.686131883940334],
            ],
            "type": "LineString",
        },
    }


def test_simplify(bk_bridge_park):
    original = geo_utils.from_geojson(bk_bridge_park)
    simplified = line_simplification.simplify(original)
