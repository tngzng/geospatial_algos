# geospatial_algos

Algorithms for storing, manipulating, and analyzing geospatial data.

## Developing

1. Activate venv
    ``` bash
    python3 -m venv .venv
    source .venv/bin/activate
    ```
1. Install python requirements
    ``` bash
    make install
    ```
1. Run tests
    ``` bash 
    make test
    ``` 

## Updating Requirements

1. Add requirement to `requirements.in`
1. Compile the `requirements.txt` file
    ``` bash
    make pip-compile
    ```
