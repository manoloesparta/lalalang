PYTHON = venv/bin/python
PIP = venv/bin/pip

.PHONY: install
install:
	# Adding the repl and interpreter to system, use setup.py, setup.cfg or pyproject.toml

setup:
	virtualenv -p $(env) venv
	$(PIP) install -r requirements.txt

unit:
	$(PYTHON) -m coverage run -m unittest discover -s tests/unit
	$(PYTHON) -m coverage report -m

accept:
	# Acceptance tests: Pending on run_acceptance_tests.sh, use behave

freeze:
	$(PIP) freeze > requirements.txt

format:
	$(PYTHON) -m black --diff .
	$(PYTHON) -m black .

clean:
	find . -name __pycache__ | xargs rm -rf

