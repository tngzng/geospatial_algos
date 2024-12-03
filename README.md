# geospatial_algos

Algorithms for storing, manipulating, and analyzing geospatial data.

## Developing
1. Install python requirements
    ``` bash
    source .venv/bin/activate
    pip3 install -r requirements.txt
    ```

## Updating Requirements

1. Add requirement to `requirements.in`
1. Compile the `requirements.txt` file
    ``` bash
    python3 -m pip install pip-tools
    pip-compile --output-file=requirements.txt requirements.in
    ```
