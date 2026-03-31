.PHONY: help install test test-structural test-file cov cov-branch cov-html cov-xml mermaid-build clean

PYTHON ?= $(if $(wildcard venv/bin/python),venv/bin/python,python)
PIP := $(PYTHON) -m pip
PYTEST := $(PYTHON) -m pytest
COV_TARGET := App
TEST_DIR := tests
MERMAID_DOC := docs/tax_calculator_cfg_mermaid.md

help:
	@echo "Targets:"
	@echo "  install          Install deps from requirements.txt"
	@echo "  test             Run all tests"
	@echo "  test-structural  Run structural coverage tests only"
	@echo "  test-file        Run one test file: make test-file TEST=tests/...py"
	@echo "  cov              Coverage (line) + missing lines in terminal"
	@echo "  cov-branch       Branch coverage + missing lines in terminal"
	@echo "  cov-html         Branch coverage + HTML report (htmlcov/)"
	@echo "  cov-xml          Branch coverage + XML report (coverage.xml)"
	@echo "  mermaid-build    Build Mermaid diagrams from markdown into docs/build"
	@echo "  clean            Remove cache/artifacts"

install:
	$(PIP) install -r requirements.txt

test:
	$(PYTEST) $(TEST_DIR)

test-structural:
	$(PYTEST) tests/structural_coverage

test-file:
	@test -n "$(TEST)" || (echo "Missing TEST. Example: make test-file TEST=tests/structural_coverage/test_structural_coverage.py" && exit 1)
	$(PYTEST) $(TEST)

cov:
	$(PYTEST) --cov=$(COV_TARGET) --cov-config=.coveragerc --cov-report=term-missing $(TEST_DIR)

cov-branch:
	$(PYTEST) --cov=$(COV_TARGET) --cov-config=.coveragerc --cov-branch --cov-report=term-missing $(TEST_DIR)

cov-html:
	$(PYTEST) --cov=$(COV_TARGET) --cov-config=.coveragerc --cov-branch --cov-report=term-missing --cov-report=html $(TEST_DIR)

cov-xml:
	$(PYTEST) --cov=$(COV_TARGET) --cov-config=.coveragerc --cov-branch --cov-report=term-missing --cov-report=xml $(TEST_DIR)

mermaid-build:
	bash scripts/build_mermaid.sh $(MERMAID_DOC)

clean:
	rm -rf .pytest_cache .coverage coverage.xml htmlcov docs/build
	find . -type d -name "__pycache__" -prune -exec rm -rf {} +
