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

from shapely import box, contains

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


class Index:
    def __init__(self) -> None:
        self.root: Node = None

    def insert(self, label: str, bounds: Bounds) -> None:
        if self.root is None:
            self.root = Node(box(bounds))
            return
        # check if there is an appropriate node to append to
        # use the intersection func for this?
        # if no such node exists, make a new root node
        # by merging the existing root node with the new bounds
        # and giving the new root two children
        #   - the prev root,
        #   - and the new bounds minus the prev root bounds

    def search(self, bbox) -> None:
        # the outermost bounds of the dataset don't contain the query bounds
        if not contains(self.root.bbox, bbox):
            return []
        parent = self.root
        while True:
            if eligible_child := next(
                (child for child in parent.children if contains(child.bbox, bbox)), None
            ):
                parent = eligible_child
            else:
                return parent
