"""
The basic idea of an R-tree is simple: leaf nodes of the tree hold spatial data,
whereas a branching node corresponds to the minimum bounding box that contains all of its children.

Functions:
- insert - accept a label and a bounding box to add to the index
- search - accept a bounding box to check for intersections in the index

Resources:
- https://towardsdatascience.com/speed-up-your-geospatial-data-analysis-with-r-trees-4f75abdc6025
"""

from itertools import combinations
from typing import Optional

import geojson
from shapely import Polygon
from shapely import bounds as make_bounds
from shapely import box as make_box
from shapely import contains
from shapely import difference as get_difference
from shapely import distance as get_distance
from shapely import intersection as get_intersection
from shapely import union

Bounds = tuple[float, float, float, float]
MAX_CHILDREN = 2


class Node:
    def __init__(self, bounds: Bounds, label: Optional[str] = None) -> None:
        self.bbox = make_box(*bounds)
        self.label = label
        self.children = []

    def __repr__(self) -> str:
        description = type(self).__name__
        if self.label:
            description = f"{description} '{self.label}'"

        # put geojson on newline to easily copy/paste while debugging
        return f"{description}:\n{geojson.dumps(self.bbox)}"

    def add_child(self, child: "Node") -> None:
        self.children.append(child)

    def update_bounds(self, bounds: Bounds) -> None:
        self.bbox = make_box(*bounds)

    def reset_children(self) -> None:
        self.children = []


class Index:
    def __init__(self) -> None:
        self.root: Node = None
        self.labels: set[str] = set()

    def search(self, bounds: Bounds) -> list[Node]:
        bbox = make_box(*bounds)
        parent = self.find_parent_node(bbox)
        if parent is None:
            return []

        leaf_nodes = self.get_leaf_nodes(parent)
        return self.filter_intersecting(leaf_nodes, bbox)

    def find_parent_node(self, bbox: Polygon) -> Optional[Node]:
        # the outermost outer bounds of the dataset don't contain the query bbox
        if not contains(self.root.bbox, bbox):
            return None

        # traverse children to find the smallest bbox that contains the query bbox
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
            node
            for node in nodes
            if node.bbox == bbox or get_intersection(node.bbox, bbox)
        ]

    def insert(self, label: str, bounds: Bounds) -> None:
        assert (
            label not in self.labels
        ), f"Label {label} already in dataset. Must use a unique name."
        self.labels.add(label)

        new_child = Node(bounds, label=label)

        # scenario 1: index is empty
        if self.root is None:
            # TODO: add helper to standardize auto-generated labels
            self.root = Node(bounds, label=f"New Root: {label}")
            self.root.add_child(new_child)
            return

        # scenario 2: index has parent with bounds containing new child
        bbox = make_box(*bounds)
        parent = self.find_parent_node(bbox)
        if parent:
            if len(parent.children) < MAX_CHILDREN:
                parent.add_child(new_child)
                return

            # TODO: reconsider this approach if MAX_CHILDREN is increased
            # taking the two closest children might not make sense if there are
            # five children, and the two closest are centrally located
            children = parent.children + [new_child]
            children_by_label = {child.label: child for child in children}
            child_pairs = combinations(children, 2)
            min_distance, min_pair = float("inf"), None
            for child_pair in child_pairs:
                distance = get_distance(child_pair[0].bbox, child_pair[1].bbox)
                if distance < min_distance:
                    min_distance = distance
                    min_pair = child_pair

            for child in min_pair:
                del children_by_label[child.label]

            parent.reset_children()
            new_parent_bbox = self.get_union_bbox(min_pair[0].bbox, min_pair[1].bbox)
            new_parent = Node(
                make_bounds(new_parent_bbox), label=f"New Parent 1: {label}"
            )
            new_parent.add_child(min_pair[0])
            new_parent.add_child(min_pair[1])
            parent.add_child(new_parent)

            remaining_children = [child for child in children_by_label.values()]
            new_parent_bbox = remaining_children[0].bbox
            for child in remaining_children[1:]:
                new_parent_bbox = self.get_union_bbox(new_parent_bbox, child.bbox)

            new_parent = Node(
                make_bounds(new_parent_bbox), label=f"New Parent 2: {label}"
            )
            for child in remaining_children:
                new_parent.add_child(child)
            parent.add_child(new_parent)
            return

        # scenario 3: index needs new or updated parent to contain new child
        new_root_bbox = self.get_union_bbox(self.root.bbox, bbox)
        new_root_bounds = make_bounds(new_root_bbox)
        if len(self.root.children) < MAX_CHILDREN:
            self.root.update_bounds(new_root_bounds)
            self.root.add_child(new_child)
            return

        new_root = Node(new_root_bounds, label=f"New Root: {label}")
        new_parent_bbox = get_difference(new_root.bbox, self.root.bbox)
        new_parent = Node(make_bounds(new_parent_bbox), label=f"New Parent: {label}")

        new_parent.add_child(new_child)
        new_root.add_child(new_parent)
        new_root.add_child(self.root)
        self.root = new_root

    def get_union_bbox(self, bbox_1: Polygon, bbox_2: Polygon) -> Bounds:
        union_geom = union(bbox_1, bbox_2) if bbox_1 != bbox_2 else bbox_1
        return union_geom
