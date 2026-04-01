.PHONY: help install test test-structural structural-cov cov-statement cov-statement-html clean

PYTHON ?= $(if $(wildcard venv/bin/python),venv/bin/python,python)
PIP := $(PYTHON) -m pip
PYTEST := $(PYTHON) -m pytest
COV_TARGET := App
TEST_DIR := tests
STRUCTURAL_TEST_DIR := tests/structural_coverage
STRUCTURAL_STATEMENT_FILE := $(STRUCTURAL_TEST_DIR)/test_statement_coverage.py
STRUCTURAL_BRANCH_FILE := $(STRUCTURAL_TEST_DIR)/test_branch_coverage.py
STRUCTURAL_CONDITION_FILE := $(STRUCTURAL_TEST_DIR)/test_condition_coverage.py
STRUCTURAL_PATHS_FILE := $(STRUCTURAL_TEST_DIR)/test_independent_paths_coverage.py
COV_ARGS := --cov=$(COV_TARGET) --cov-config=.coveragerc
KIND ?= statement
MODE ?= statement
HTML ?= 0

help:
	@echo "Targets:"
	@echo "  install          Install deps from requirements.txt"
	@echo "  test             Run all tests"
	@echo "  test-structural  Run structural coverage tests only"
	@echo "  structural-cov   Structural coverage on one file"
	@echo "                   KIND=statement|branch|condition|paths"
	@echo "                   MODE=statement|branch"
	@echo "                   HTML=0|1"
	@echo "                   Examples:"
	@echo "                     make structural-cov KIND=statement MODE=statement HTML=0"
	@echo "                     make structural-cov KIND=statement MODE=statement HTML=1"
	@echo "                     make structural-cov KIND=branch MODE=branch HTML=0"
	@echo "  cov-statement    Alias for statement + no HTML"
	@echo "  cov-statement-html Alias for statement + HTML"
	@echo "  clean            Remove cache/artifacts"

install:
	$(PIP) install -r requirements.txt

test:
	$(PYTEST) $(TEST_DIR)

test-structural:
	$(PYTEST) $(STRUCTURAL_TEST_DIR)

structural-cov:
	@case "$(KIND)" in \
		statement) TEST_FILE="$(STRUCTURAL_STATEMENT_FILE)" ;; \
		branch) TEST_FILE="$(STRUCTURAL_BRANCH_FILE)" ;; \
		condition) TEST_FILE="$(STRUCTURAL_CONDITION_FILE)" ;; \
		paths) TEST_FILE="$(STRUCTURAL_PATHS_FILE)" ;; \
		*) echo "Invalid KIND='$(KIND)'. Use: statement|branch|condition|paths"; exit 1 ;; \
	esac; \
	case "$(MODE)" in \
		statement) COV_MODE_ARGS="" ;; \
		branch) COV_MODE_ARGS="--cov-branch" ;; \
		*) echo "Invalid MODE='$(MODE)'. Use: statement|branch"; exit 1 ;; \
	esac; \
	case "$(HTML)" in \
		0) HTML_ARGS="" ;; \
		1) HTML_ARGS="--cov-report=html" ;; \
		*) echo "Invalid HTML='$(HTML)'. Use: 0|1"; exit 1 ;; \
	esac; \
	echo "Running structural coverage: KIND=$(KIND) MODE=$(MODE) HTML=$(HTML) FILE=$$TEST_FILE"; \
	$(PYTEST) $(COV_ARGS) $$COV_MODE_ARGS --cov-report=term-missing $$HTML_ARGS $$TEST_FILE

cov-statement:
	$(MAKE) structural-cov KIND=statement MODE=statement HTML=0

cov-statement-html:
	$(MAKE) structural-cov KIND=statement MODE=statement HTML=1

clean:
	rm -rf .pytest_cache .coverage coverage.xml htmlcov
	find . -type d -name "__pycache__" -prune -exec rm -rf {} +
