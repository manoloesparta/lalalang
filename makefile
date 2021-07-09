PYTHON = venv/bin/python
PIP = venv/bin/pip

.PHONY: install
install:
	./setup.py build install --user

setup:
	virtualenv -p $(env) venv
	$(PIP) install -r requirements.txt

.PHONY: tests
tests:
	$(PYTHON) -m coverage run -m unittest discover -s tests
	$(PYTHON) -m coverage report -m

freeze:
	$(PIP) freeze > requirements.txt

format:
	$(PYTHON) -m black --diff .
	$(PYTHON) -m black .

clean:
	find . -name __pycache__ | xargs rm -rf
	rm -rf build dist *.egg-info .eggs .coverage