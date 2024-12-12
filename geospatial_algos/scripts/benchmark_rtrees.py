import random
import sys
import time

sys.path.insert(0, ".")

from geospatial_algos.geo_utils import get_intersection, make_box
from geospatial_algos.rtree import Index

NUM_LOOPS = 1_000

public_courts: list[dict] = [
    {
        "type": "Feature",
        "properties": {
            "name": "South Oxford",
        },
        "geometry": {"type": "Point", "coordinates": [73.972129, 40.6840711]},
    },
    {
        "type": "Feature",
        "properties": {
            "name": "Jackie Robinson",
        },
        "geometry": {"type": "Point", "coordinates": [73.9284951, 40.6806745]},
    },
    {
        "type": "Feature",
        "properties": {
            "name": "Decatur",
        },
        "geometry": {"type": "Point", "coordinates": [73.9355312, 40.6818194]},
    },
    # {
    #     "type": "Feature",
    #     "properties": {
    #         "name": "Fort Greene",
    #     },
    #     "geometry": {"type": "Point", "coordinates": [73.978382, 40.6898247]},
    # },
    # {
    #     "type": "Feature",
    #     "properties": {
    #         "name": "Lincoln Terrace",
    #     },
    #     "geometry": {"type": "Point", "coordinates": [73.925451, 40.668831]},
    # },
    # {
    #     "type": "Feature",
    #     "properties": {
    #         "name": "Prospect Park",
    #     },
    #     "geometry": {"type": "Point", "coordinates": [73.961844, 40.6549845]},
    # },
    # {
    #     "type": "Feature",
    #     "properties": {
    #         "name": "Mccarren",
    #     },
    #     "geometry": {"type": "Point", "coordinates": [73.9534005, 40.7222456]},
    # },
    # {
    #     "type": "Feature",
    #     "properties": {
    #         "name": "Forest Hills",
    #     },
    #     "geometry": {"type": "Point", "coordinates": [73.8904704, 40.6823958]},
    # },
    # {
    #     "type": "Feature",
    #     "properties": {
    #         "name": "Leif Ericson",
    #     },
    #     "geometry": {"type": "Point", "coordinates": [74.0171488, 40.6335201]},
    # },
    # {
    #     "type": "Feature",
    #     "properties": {
    #         "name": "Cooper",
    #     },
    #     "geometry": {"type": "Point", "coordinates": [73.9381716, 40.7162868]},
    # },
    # {
    #     "type": "Feature",
    #     "properties": {
    #         "name": "Bensonhurst",
    #     },
    #     "geometry": {"type": "Point", "coordinates": [74.0015034, 40.5950783]},
    # },
]


def extract_bounds(geo_feature: dict) -> tuple:
    x, y = geo_feature["geometry"]["coordinates"]
    return (x, y, x, y)


def extract_name(geo_feature: dict) -> str:
    return geo_feature["properties"]["name"]


# populate index
idx = Index()

for court in public_courts:
    idx.insert(extract_name(court), extract_bounds(court))

# make it fair so we're not constantly making the bbox in the brute force approach
for court in public_courts:
    court["bbox"] = make_box(*extract_bounds(court))

# test rtree
random.shuffle(public_courts)
rtree_start = time.time()
for _ in range(NUM_LOOPS):
    for court in public_courts:
        found = idx.search(extract_bounds(court))
        try:
            assert len(found) == 1
        except AssertionError as e:
            breakpoint()
            x = 1
        assert found[0].label == extract_name(court)

rtree_time = time.time() - rtree_start
print(f"Rtree took {rtree_time} seconds")


# test brute force
def brute_force_search(target: dict) -> list[dict]:
    res = []
    for court in public_courts:
        if court["bbox"] == target["bbox"] or get_intersection(
            court["bbox"], target["bbox"]
        ):
            res.append(court)

    return res


random.shuffle(public_courts)
brute_force_start = time.time()
for _ in range(NUM_LOOPS):
    for court in public_courts:
        brute_found = brute_force_search(court)
        assert len(brute_found) == 1
        assert extract_name(brute_found[0]) == extract_name(court)

brute_force_time = time.time() - brute_force_start
print(f"Brute force took {brute_force_time} seconds")

print(f"Rtree was {brute_force_time / rtree_time} times faster")
