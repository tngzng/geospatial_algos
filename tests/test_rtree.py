from shapely import bounds as make_bounds
from shapely import union

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
        return make_bounds(parent_geom)

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
        return make_bounds(parent_geom)

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


def test_insert():
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
    lincoln_terrace = {
        "type": "Feature",
        "properties": {"name": "Lincoln Terrace"},
        "geometry": {"type": "Point", "coordinates": [-73.925451, 40.668831]},
    }

    def extract_bounds(geo_feature: dict) -> tuple:
        x, y = geo_feature["geometry"]["coordinates"]
        return (x, y, x, y)

    def extract_name(geo_feature: dict) -> str:
        return geo_feature["properties"]["name"]

    idx = rtree.Index()

    # test insert
    idx.insert(extract_name(decatur), extract_bounds(decatur))
    # index should have root
    # one child - decatur

    idx.insert(extract_name(jackie_robinson), extract_bounds(jackie_robinson))
    # index should have root
    # two children - decatur + jackie

    idx.insert(extract_name(fort_greene), extract_bounds(fort_greene))
    # index should have root
    # two children - bedstuy, fort greene
    # bedstuy has two children - decatur + jackie
    # fort greene has one child - fort greene

    idx.insert(extract_name(south_oxford), extract_bounds(south_oxford))
    # index should have root
    # two children - bedstuy, fort greene
    # bedstuy has two children - decatur + jackie
    # fort greene has two children - fort greene + south oxford

    idx.insert(f"{extract_name(south_oxford)} 2", extract_bounds(south_oxford))
    # index should have root
    # two children - bedstuy, fort greene
    # bedstuy has two children - decatur + jackie
    # fort greene has two children - fort greene + south oxford
