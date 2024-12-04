install:
	pip3 install -r requirements.txt

test:
	pytest tests

pip-compile:
	python3 -m pip install pip-tools; \
    pip-compile --output-file=requirements.txt requirements.in
