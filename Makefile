.PHONY: help install test test-structural test-file test-structural-statement test-structural-branch test-structural-condition test-structural-paths cov cov-branch cov-html cov-xml cov-statement cov-statement-html mermaid-build clean

PYTHON ?= $(if $(wildcard venv/bin/python),venv/bin/python,python)
PIP := $(PYTHON) -m pip
PYTEST := $(PYTHON) -m pytest
COV_TARGET := App
TEST_DIR := tests
STRUCTURAL_TEST_DIR := tests/structural_coverage
STRUCTURAL_STATEMENT_FILE := $(STRUCTURAL_TEST_DIR)/test_statement_coverage.py
STRUCTURAL_BRANCH_FILE := $(STRUCTURAL_TEST_DIR)/test_branch_coverage.py
STRUCTURAL_CONDITION_FILE := $(STRUCTURAL_TEST_DIR)/test_condition_mcdc_coverage.py
STRUCTURAL_PATHS_FILE := $(STRUCTURAL_TEST_DIR)/test_independent_paths_coverage.py
MERMAID_DOC := docs/tax_calculator_cfg_mermaid.md
COV_ARGS := --cov=$(COV_TARGET) --cov-config=.coveragerc
STATEMENT_TEST := $(STRUCTURAL_STATEMENT_FILE)::test_statement_coverage

help:
	@echo "Targets:"
	@echo "  install          Install deps from requirements.txt"
	@echo "  test             Run all tests"
	@echo "  test-structural  Run structural coverage tests only"
	@echo "  test-structural-statement Run statement structural tests"
	@echo "  test-structural-branch Run branch structural tests"
	@echo "  test-structural-condition Run condition/MCDC structural tests"
	@echo "  test-structural-paths Run independent paths structural tests"
	@echo "  test-file        Run one test file: make test-file TEST=tests/...py"
	@echo "  cov              Coverage (line) + missing lines in terminal"
	@echo "  cov-branch       Branch coverage + missing lines in terminal"
	@echo "  cov-html         Branch coverage + HTML report (htmlcov/)"
	@echo "  cov-xml          Branch coverage + XML report (coverage.xml)"
	@echo "  cov-statement    Coverage only for test_statement_coverage"
	@echo "  cov-statement-html Coverage for test_statement_coverage + HTML report"
	@echo "  mermaid-build    Build Mermaid diagrams from markdown into docs/build"
	@echo "  clean            Remove cache/artifacts"

install:
	$(PIP) install -r requirements.txt

test:
	$(PYTEST) $(TEST_DIR)

test-structural:
	$(PYTEST) $(STRUCTURAL_TEST_DIR)

test-structural-statement:
	$(PYTEST) $(STRUCTURAL_STATEMENT_FILE)

test-structural-branch:
	$(PYTEST) $(STRUCTURAL_BRANCH_FILE)

test-structural-condition:
	$(PYTEST) $(STRUCTURAL_CONDITION_FILE)

test-structural-paths:
	$(PYTEST) $(STRUCTURAL_PATHS_FILE)

test-file:
	@test -n "$(TEST)" || (echo "Missing TEST. Example: make test-file TEST=tests/structural_coverage/test_statement_coverage.py" && exit 1)
	$(PYTEST) $(TEST)

cov:
	$(PYTEST) $(COV_ARGS) --cov-report=term-missing $(TEST_DIR)

cov-branch:
	$(PYTEST) $(COV_ARGS) --cov-branch --cov-report=term-missing $(TEST_DIR)

cov-html:
	$(PYTEST) $(COV_ARGS) --cov-branch --cov-report=term-missing --cov-report=html $(TEST_DIR)

cov-xml:
	$(PYTEST) $(COV_ARGS) --cov-branch --cov-report=term-missing --cov-report=xml $(TEST_DIR)

cov-statement:
	$(PYTEST) $(COV_ARGS) --cov-report=term-missing $(STATEMENT_TEST)

cov-statement-html:
	$(PYTEST) $(COV_ARGS) --cov-report=term-missing --cov-report=html $(STATEMENT_TEST)

mermaid-build:
	bash scripts/build_mermaid.sh $(MERMAID_DOC)

clean:
	rm -rf .pytest_cache .coverage coverage.xml htmlcov docs/build
	find . -type d -name "__pycache__" -prune -exec rm -rf {} +
