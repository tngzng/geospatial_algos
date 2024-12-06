import pytest
from shapely import Polygon
from shapely import bounds as make_bounds
from shapely import box as make_box
from shapely import contains, union

from geospatial_algos.geospatial_algos import rtree  # type: ignore


def extract_bounds(geo_feature: dict) -> tuple:
    x, y = geo_feature["geometry"]["coordinates"]
    return (x, y, x, y)


def extract_name(geo_feature: dict) -> str:
    return geo_feature["properties"]["name"]


def get_parent_bounds(node_1: Polygon, node_2: Polygon) -> rtree.Bounds:
    parent_geom = union(node_1.bbox, node_2.bbox)
    return make_bounds(parent_geom)


@pytest.fixture
def jackie_robinson():
    return {
        "type": "Feature",
        "properties": {"name": "Jackie Robinson"},
        "geometry": {"type": "Point", "coordinates": [-73.9284951, 40.6806745]},
    }


@pytest.fixture
def decatur():
    return {
        "type": "Feature",
        "properties": {"name": "Decatur"},
        "geometry": {"type": "Point", "coordinates": [-73.9355312, 40.6818194]},
    }


@pytest.fixture
def south_oxford():
    return {
        "type": "Feature",
        "properties": {"name": "South Oxford"},
        "geometry": {"type": "Point", "coordinates": [-73.972129, 40.6840711]},
    }


@pytest.fixture
def fort_greene():
    return {
        "type": "Feature",
        "properties": {"name": "Fort Greene"},
        "geometry": {"type": "Point", "coordinates": [-73.978382, 40.6898247]},
    }


@pytest.fixture
def jackie_robinson_node(jackie_robinson):
    return rtree.Node(extract_bounds(jackie_robinson), extract_name(jackie_robinson))


@pytest.fixture
def decatur_node(decatur):
    return rtree.Node(extract_bounds(decatur), extract_name(decatur))


@pytest.fixture
def south_oxford_node(south_oxford):
    return rtree.Node(
        extract_bounds(south_oxford),
        extract_name(south_oxford),
    )


@pytest.fixture
def fort_greene_node(fort_greene):
    return rtree.Node(
        extract_bounds(fort_greene),
        extract_name(fort_greene),
    )


def test_find_parent_node(
    jackie_robinson_node, decatur_node, south_oxford_node, fort_greene_node
):
    # setup test data
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


def test_search(
    jackie_robinson_node, decatur_node, south_oxford_node, fort_greene_node
):
    # setup test data
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
    nodes = idx.search(make_bounds(decatur_node.bbox))
    assert len(nodes) == 1
    assert nodes[0] == decatur_node


def test_insert__entry_not_contained_in_current_bounds(
    jackie_robinson, decatur, south_oxford, fort_greene
):
    idx = rtree.Index()

    # test insert decatur
    idx.insert(extract_name(decatur), extract_bounds(decatur))
    assert len(idx.root.children) == 1
    assert idx.root.children[0].label == extract_name(decatur)
    assert idx.root.bbox == make_box(*extract_bounds(decatur))

    # test insert jackie robinson
    idx.insert(extract_name(jackie_robinson), extract_bounds(jackie_robinson))
    assert len(idx.root.children) == 2
    child_names = [child.label for child in idx.root.children]
    assert sorted(child_names) == [extract_name(decatur), extract_name(jackie_robinson)]
    assert contains(idx.root.bbox, make_box(*extract_bounds(decatur)))
    assert contains(idx.root.bbox, make_box(*extract_bounds(jackie_robinson)))

    # test insert fort greene
    idx.insert(extract_name(fort_greene), extract_bounds(fort_greene))
    assert len(idx.root.children) == 2
    fort_greene_node, bedstuy_node = idx.root.children

    assert len(bedstuy_node.children) == 2
    bedstuy_child_names = [child.label for child in bedstuy_node.children]
    assert sorted(bedstuy_child_names) == [
        extract_name(decatur),
        extract_name(jackie_robinson),
    ]
    assert contains(bedstuy_node.bbox, make_box(*extract_bounds(decatur)))
    assert contains(bedstuy_node.bbox, make_box(*extract_bounds(jackie_robinson)))

    assert len(fort_greene_node.children) == 1
    assert contains(fort_greene_node.bbox, make_box(*extract_bounds(fort_greene)))

    # test insert south oxford
    idx.insert(extract_name(south_oxford), extract_bounds(south_oxford))
    assert len(idx.root.children) == 2
    fort_greene_node, bedstuy_node = idx.root.children

    assert len(bedstuy_node.children) == 2
    bedstuy_child_names = [child.label for child in bedstuy_node.children]
    assert sorted(bedstuy_child_names) == [
        extract_name(decatur),
        extract_name(jackie_robinson),
    ]
    assert contains(bedstuy_node.bbox, make_box(*extract_bounds(decatur)))
    assert contains(bedstuy_node.bbox, make_box(*extract_bounds(jackie_robinson)))

    assert len(fort_greene_node.children) == 2
    fort_greene_child_names = [child.label for child in fort_greene_node.children]
    assert sorted(fort_greene_child_names) == [
        extract_name(fort_greene),
        extract_name(south_oxford),
    ]
    assert contains(fort_greene_node.bbox, make_box(*extract_bounds(fort_greene)))
    assert contains(fort_greene_node.bbox, make_box(*extract_bounds(south_oxford)))


def test_insert__entry_contained_in_current_bounds(jackie_robinson, decatur):
    idx = rtree.Index()

    # test insert decatur
    idx.insert(extract_name(decatur), extract_bounds(decatur))
    assert len(idx.root.children) == 1
    assert idx.root.children[0].label == extract_name(decatur)
    assert idx.root.bbox == make_box(*extract_bounds(decatur))

    # test insert jackie robinson
    idx.insert(extract_name(jackie_robinson), extract_bounds(jackie_robinson))
    assert len(idx.root.children) == 2
    child_names = [child.label for child in idx.root.children]
    assert sorted(child_names) == [extract_name(decatur), extract_name(jackie_robinson)]
    assert contains(idx.root.bbox, make_box(*extract_bounds(decatur)))
    assert contains(idx.root.bbox, make_box(*extract_bounds(jackie_robinson)))

    # test insert decatur _again_
    idx.insert(f"{extract_name(decatur)} 2", extract_bounds(decatur))
    assert len(idx.root.children) == 2
    decatur_node, jackie_node = idx.root.children

    assert len(decatur_node.children) == 2
    child_names = [child.label for child in decatur_node.children]
    assert sorted(child_names) == [extract_name(decatur), f"{extract_name(decatur)} 2"]
    assert decatur_node.bbox == make_box(*extract_bounds(decatur))

    assert len(jackie_node.children) == 1
    assert jackie_node.children[0].label == extract_name(jackie_robinson)
    assert jackie_node.bbox == make_box(*extract_bounds(jackie_robinson))
