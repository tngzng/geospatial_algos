'''
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
'''

class Index:
    pass