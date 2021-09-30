checkfiles = alarmer/ tests/ examples/ conftest.py
black_opts = -l 100 -t py38
py_warn = PYTHONDEVMODE=1

up:
	@poetry update

deps:
	@poetry install

style: deps
	isort -src $(checkfiles)
	black $(black_opts) $(checkfiles)

check: deps
	black --check $(black_opts) $(checkfiles) || (echo "Please run 'make style' to auto-fix style issues" && false)
	flake8 $(checkfiles)
	bandit -x tests -r $(checkfiles)
	mypy $(checkfiles)

test: deps
	$(py_warn) pytest

build: deps
	@poetry build

ci: check test

publish:
	@poetry publish --build
