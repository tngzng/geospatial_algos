# geospatial_algos

Algorithms for storing, manipulating, and analyzing geospatial data.

## Algorithms

### Line Simplification
Reduce the complexity of a line geometry by removing points that don't meet a distance threshold. 

![Sample output showing a line geometry before and after simplification.](assets/line_simplification.png)

### Convex Hull
Enclose a set of points in a convex polygon by checking the cross product of vectors for candidate points.

![Sample output showing a concave polygon and it's corresponding convex hull.](assets/convex_hull.png)

## Pansharpening 
Combine data from lower resolution color imagery and higher resolution greyscale imagery to "sharpen" the color imagery, making it appear more detailed.

Input (low-res color photo):

![Low-res color photo of two tabby cats.](assets/tabby_cats__lowres.png)

Input (hi-res greyscale photo): 

![Hi-res greyscale photo of two tabby cats.](assets/tabby_cats__greyscale.png)

Pansharpened result:

![Pansharpened photo of two tabby cats.](assets/tabby_cats__pansharpened.png)


## Developing

1. Activate venv
    ``` bash
    python3 -m venv .venv
    source .venv/bin/activate
    ```
1. Install python requirements
    ``` bash
    pip3 install -r requirements.txt
    ```
1. Run tests
    ``` bash 
    pytest tests
    ``` 

## Updating Requirements

1. Add requirement to `requirements.in`
1. Compile the `requirements.txt` file
    ``` bash
    python3 -m pip install pip-tools
    pip-compile --output-file=requirements.txt requirements.in
    ```
1. Install python requirements
    ``` bash
    pip3 install -r requirements.txt
    ```