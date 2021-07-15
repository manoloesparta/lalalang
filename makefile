PYTHON = venv/bin/python
PIP = venv/bin/pip

.PHONY: setup 
setup:
	virtualenv -p $(env) venv
	$(PIP) install -r requirements.txt

.PHONY: check 
check:
	$(MAKE) analyze --no-print-directory
	$(MAKE) format --no-print-directory
	$(MAKE) tests --no-print-directory

.PHONY: install
install:
	./setup.py build install --user

.PHONY: tests
tests:
	$(PYTHON) -m coverage run -m unittest discover -s tests
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
	rm -rf build dist *.egg-info .eggs .coverage .mypy_cache
