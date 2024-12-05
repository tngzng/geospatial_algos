import pytest
from shapely import bounds, union

from geospatial_algos.geospatial_algos import rtree  # type: ignore


def test_find_parent_node():
    # setup test data
    south_oxford = {
        "type": "Feature",
        "properties": {"name": "South Oxford"},
        "geometry": {"type": "Point", "coordinates": [-73.972129, 40.6840711]},
    }
    fort_greene = {
        "type": "Feature",
        "properties": {"name": "Fort Greene"},
        "geometry": {"type": "Point", "coordinates": [-73.978382, 40.6898247]},
    }
    jackie_robinson = {
        "type": "Feature",
        "properties": {"name": "Jackie Robinson"},
        "geometry": {"type": "Point", "coordinates": [-73.9284951, 40.6806745]},
    }
    decatur = {
        "type": "Feature",
        "properties": {"name": "Decatur"},
        "geometry": {"type": "Point", "coordinates": [-73.9355312, 40.6818194]},
    }

    def extract_bounds(geo_feature: dict) -> tuple:
        x, y = geo_feature["geometry"]["coordinates"]
        return (x, y, x, y)

    def extract_name(geo_feature: dict) -> str:
        return geo_feature["properties"]["name"]

    south_oxford_node = rtree.Node(
        extract_bounds(south_oxford),
        extract_name(south_oxford),
    )
    fort_greene_node = rtree.Node(
        extract_bounds(fort_greene),
        extract_name(fort_greene),
    )
    jackie_robinson_node = rtree.Node(
        extract_bounds(jackie_robinson), extract_name(jackie_robinson)
    )
    decatur_node = rtree.Node(extract_bounds(decatur), extract_name(decatur))

    def get_parent_bounds(node1, node2):
        parent_geom = union(node1.bbox, node2.bbox)
        return bounds(parent_geom)

    fort_greene_clinton_hill_node = rtree.Node(
        get_parent_bounds(fort_greene_node, south_oxford_node),
        "Fort Greene / Clinton Hill",
    )
    bedstuy_node = rtree.Node(
        get_parent_bounds(jackie_robinson_node, decatur_node), "BedStuy"
    )
    root_node = rtree.Node(
        get_parent_bounds(fort_greene_clinton_hill_node, bedstuy_node), "Root"
    )
    root_node.children = [bedstuy_node, fort_greene_clinton_hill_node]
    bedstuy_node.children = [decatur_node, jackie_robinson_node]
    fort_greene_clinton_hill_node.children = [fort_greene_node, south_oxford_node]
    idx = rtree.Index()
    idx.root = root_node

    # test find_parent_node
    node = idx.find_parent_node(decatur_node.bbox)
    assert node == bedstuy_node

    node = idx.find_parent_node(jackie_robinson_node.bbox)
    assert node == bedstuy_node

    node = idx.find_parent_node(south_oxford_node.bbox)
    assert node == fort_greene_clinton_hill_node

    node = idx.find_parent_node(fort_greene_node.bbox)
    assert node == fort_greene_clinton_hill_node


def test_search():
    # setup test data
    south_oxford = {
        "type": "Feature",
        "properties": {"name": "South Oxford"},
        "geometry": {"type": "Point", "coordinates": [-73.972129, 40.6840711]},
    }
    fort_greene = {
        "type": "Feature",
        "properties": {"name": "Fort Greene"},
        "geometry": {"type": "Point", "coordinates": [-73.978382, 40.6898247]},
    }
    jackie_robinson = {
        "type": "Feature",
        "properties": {"name": "Jackie Robinson"},
        "geometry": {"type": "Point", "coordinates": [-73.9284951, 40.6806745]},
    }
    decatur = {
        "type": "Feature",
        "properties": {"name": "Decatur"},
        "geometry": {"type": "Point", "coordinates": [-73.9355312, 40.6818194]},
    }

    def extract_bounds(geo_feature: dict) -> tuple:
        x, y = geo_feature["geometry"]["coordinates"]
        return (x, y, x, y)

    def extract_name(geo_feature: dict) -> str:
        return geo_feature["properties"]["name"]

    south_oxford_node = rtree.Node(
        extract_bounds(south_oxford),
        extract_name(south_oxford),
    )
    fort_greene_node = rtree.Node(
        extract_bounds(fort_greene),
        extract_name(fort_greene),
    )
    jackie_robinson_node = rtree.Node(
        extract_bounds(jackie_robinson), extract_name(jackie_robinson)
    )
    decatur_node = rtree.Node(extract_bounds(decatur), extract_name(decatur))

    def get_parent_bounds(node1, node2):
        parent_geom = union(node1.bbox, node2.bbox)
        return bounds(parent_geom)

    fort_greene_clinton_hill_node = rtree.Node(
        get_parent_bounds(fort_greene_node, south_oxford_node),
        "Fort Greene / Clinton Hill",
    )
    bedstuy_node = rtree.Node(
        get_parent_bounds(jackie_robinson_node, decatur_node), "BedStuy"
    )
    root_node = rtree.Node(
        get_parent_bounds(fort_greene_clinton_hill_node, bedstuy_node), "Root"
    )
    root_node.children = [bedstuy_node, fort_greene_clinton_hill_node]
    bedstuy_node.children = [decatur_node, jackie_robinson_node]
    fort_greene_clinton_hill_node.children = [fort_greene_node, south_oxford_node]
    idx = rtree.Index()
    idx.root = root_node

    # test search
    nodes = idx.search(bounds(decatur_node.bbox))
    assert len(nodes) == 1
    assert nodes[0] == decatur_node


@pytest.mark.skip
def test_insert():
    """
    index the following point geometries:

    A-B---
    ------
    ------
    C-D--E
    """
    pass
    # idx = rtree.Index()
    # idx.insert("A", (1, 1, 1, 1))
    # idx.insert("C", (4, 1, 4, 1))
    # idx.insert("B", (1, 3, 1, 3))
    # idx.insert("E", (4, 5, 4, 5))
    # idx.insert("D", (4, 3, 4, 3))
