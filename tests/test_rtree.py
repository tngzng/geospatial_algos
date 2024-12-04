from typing import Iterator

import geojson

from geospatial_algos.geospatial_algos import rtree  # type: ignore

PUBLIC_COURTS_FILE = "assets/bk_named_courts.geojsonl"


def _load_test_data(test_file: str) -> Iterator[dict]:
    with open(test_file) as f:
        for line in f:
            datum = geojson.loads(line)
            yield datum


def test_insert():
    idx = rtree.Index()
    public_courts = _load_test_data(PUBLIC_COURTS_FILE)
    for court in public_courts:
        idx.insert(court["geometry"]["coordinates"])
