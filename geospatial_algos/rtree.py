"""
The basic idea of an R-tree is simple: leaf nodes of the tree hold spatial data, 
whereas a branching node corresponds to the minimum bounding box that contains all of its children.

Functions:
- insert - accept a label and a bounding box to add to the index
- intersection - accept a bounding box to check for overlaps in the index 

idx = Index()
bbox_0 = (0.0, 0.0, 1.0, 1.0) # (left, bottom, right, top)
bbox_1 = (3.0, 3.0, 6.0, 6.0)
idx.insert(0, bbox_0)
idx.insert(1, bbox_1)

search_window = (-1.0, -1.0, 2.0, 2.0) # ex. 1
list(idx.intersection(search_window))
>>> [0]
search_window = (4.0, 4.0, 5.0, 5.0)   # ex. 2
list(idx.intersection(search_window))
>>> [1]
search_window = (0.0, 0.0, 6.0, 6.0)   # ex. 3
list(idx.intersection(search_window))
>>> [0, 1]
search_window = (1.01, 1.01, 2.0, 2.0) # ex. 4
list(idx.intersection(search_window))
>>> []

Resources:
- https://towardsdatascience.com/speed-up-your-geospatial-data-analysis-with-r-trees-4f75abdc6025
- https://www.programiz.com/dsa/b-tree 
- https://www.programiz.com/dsa/insertion-into-a-b-tree 
"""

from typing import Optional

from shapely import box, contains

Bounds = tuple[float, float, float, float]


class Node:
    def __init__(self, bounds: Bounds) -> None:
        self.bbox = bounds
        self.children = []

    def __repr__(self):
        class_name = type(self).__name__
        return f"{class_name} {self.bbox}"


def search(node: Node, bbox) -> Node:
    print(f"searching node {node.bbox}")
    """
    return the node that is greater than or equal to the passed bbox
    """


def contains(x, y):
    return x >= y


one = Node(1)
two = Node(2)
three = Node(3)
four = Node(4)
five = Node(5)

five.children = [two, four]
two.children = [one]
four.children = [three]

found = search(five, 4)


class Index:
    def __init__(self) -> None:
        self.root: Node = None

    def insert(self, label: str, bounds: Bounds) -> None:
        if self.root is None:
            self.root = Node(box(bounds))
            return

    def intersection(self, bounds: Bounds) -> None:
        bbox = box(bounds)
        # the outermost bounds of the dataset don't contain the query bounds
        if not contains(self.root.bbox, bbox):
            return []
        parent_node = search(self.root, bbox)
