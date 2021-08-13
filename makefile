PYTHON = venv/bin/python
PIP = venv/bin/pip

.PHONY: setup 
setup:
	virtualenv -p $(env) venv
	$(PIP) install -r requirements.txt

.PHONY: build
build:
	$(PYTHON) setup.py sdist bdist_wheel

.PHONY: publish
publish:
	$(PYTHON) -m twine upload dist/*

.PHONY: install
install:
	./setup.py build install --user

.PHONY: tests
tests:
	$(PYTHON) -m coverage run -m pytest
	$(PYTHON) -m coverage report -m

.PHONY: analyze 
analyze:
	$(PYTHON) -m mypy lalalang --no-strict-optional

.PHONY: format 
format:
	$(PYTHON) -m black .

.PHONY: clean 
clean:
	find . -name __pycache__ | xargs rm -rf
	rm -rf build dist *.egg-info .eggs .coverage .mypy_cache .pytest_cache
