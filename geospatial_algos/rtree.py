"""
The basic idea of an R-tree is simple: leaf nodes of the tree hold spatial data,
whereas a branching node corresponds to the minimum bounding box that contains all of its children.

Functions:
- insert - accept a label and a bounding box to add to the index
- search - accept a bounding box to check for intersections in the index

Resources:
- https://towardsdatascience.com/speed-up-your-geospatial-data-analysis-with-r-trees-4f75abdc6025
- https://www.programiz.com/dsa/insertion-into-a-b-tree
"""

from typing import Optional

from shapely import Polygon, bounds, box, contains, difference, intersection, union

Bounds = tuple[float, float, float, float]


class Node:
    def __init__(self, bounds: Bounds, label: Optional[str] = None) -> None:
        self.bbox = box(*bounds)
        self.label = label
        self.children = []

    def __repr__(self):
        description = type(self).__name__
        if self.label:
            description = f"{description} '{self.label}'"
        return f"{description}: {self.bbox}"

    def add_child(self, child: "Node") -> None:
        self.children.append(child)


class Index:
    def __init__(self) -> None:
        self.root: Node = None

    def insert(self, label: str, bounds: Bounds) -> None:
        child = Node(bounds, label=label)

        # scenario 1: index is empty
        if self.root is None:
            self.root = Node(bounds)
            self.root.add_child(child)
            return

        # scenario 2: index has parent with bounds containing new child
        bbox = box(*bounds)
        parent = self.find_parent_node(bbox)
        if parent:
            parent.add_child(child)
            return

        # scenario 3: index needs new parent to contain new child
        new_root_bounds = self.get_union_bounds(self.root.bbox, bbox)
        new_root = Node(box(*new_root_bounds))

        new_parent_bbox = difference(new_root.bbox, self.root.bbox)
        new_parent = Node(bounds(new_parent_bbox), label=label)

        new_parent.add_child(child)
        new_root.add_child(new_parent)
        new_root.add_child(self.root)
        self.root = new_root

    def get_union_bounds(bbox_1: Polygon, bbox_2: Polygon) -> Bounds:
        union_geom = union(bbox_1, bbox_2)
        return bounds(union_geom)

    def find_parent_node(self, bbox: Polygon) -> Optional[Node]:
        # the outermost bounds of the dataset don't contain the bounds
        if not contains(self.root.bbox, bbox):
            return None

        parent = self.root
        while True:
            if eligible_child := next(
                (child for child in parent.children if contains(child.bbox, bbox)), None
            ):
                parent = eligible_child
            else:
                return parent

    def _get_leaf_nodes(self, parent: Node, leaf_nodes: list[Node]) -> None:
        if children := parent.children:
            for child in children:
                self._get_leaf_nodes(child, leaf_nodes)
        else:
            leaf_nodes.append(parent)

    def get_leaf_nodes(self, parent: Node) -> list[Node]:
        leaf_nodes = []
        self._get_leaf_nodes(parent, leaf_nodes)
        return leaf_nodes

    def filter_intersecting(self, nodes: list[Node], bbox: Polygon) -> list[Node]:
        return [
            node for node in nodes if node.bbox == bbox or intersection(node.bbox, bbox)
        ]

    def search(self, bounds: Bounds) -> list[Node]:
        bbox = box(*bounds)
        parent = self.find_parent_node(bbox)
        if parent is None:
            return []

        leaf_nodes = self.get_leaf_nodes(parent)
        return self.filter_intersecting(leaf_nodes, bbox)
