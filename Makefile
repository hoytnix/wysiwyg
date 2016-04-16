# Project settings
PROJECT := anavah
PACKAGE := framework
SOURCES := Makefile setup.py $(shell find $(PACKAGE) -name '*.py')

# Python settings
ifndef TRAVIS
	PYTHON_MAJOR ?= 3
	PYTHON_MINOR ?= 5
endif

# Test settings
UNIT_TEST_COVERAGE := 88
INTEGRATION_TEST_COVERAGE := 47
COMBINED_TEST_COVERAGE := 100

# System paths
PLATFORM := $(shell python -c 'import sys; print(sys.platform)')
ifneq ($(findstring win32, $(PLATFORM)), )
	WINDOWS := 1
	SYS_PYTHON_DIR := C:\\Python$(PYTHON_MAJOR)$(PYTHON_MINOR)
	SYS_PYTHON := $(SYS_PYTHON_DIR)\\python.exe
	# https://bugs.launchpad.net/virtualenv/+bug/449537
	export TCL_LIBRARY=$(SYS_PYTHON_DIR)\\tcl\\tcl8.5
else
	ifneq ($(findstring darwin, $(PLATFORM)), )
		MAC := 1
	else
		LINUX := 1
	endif
	SYS_PYTHON := python$(PYTHON_MAJOR)
	ifdef PYTHON_MINOR
		SYS_PYTHON := $(SYS_PYTHON).$(PYTHON_MINOR)
	endif
endif

# Virtual environment paths
ENV := env
ifneq ($(findstring win32, $(PLATFORM)), )
	BIN := $(ENV)/Scripts
	ACTIVATE := $(BIN)/activate.bat
	OPEN := cmd /c start
else
	BIN := $(ENV)/bin
	ACTIVATE := . $(BIN)/activate
	ifneq ($(findstring cygwin, $(PLATFORM)), )
		OPEN := cygstart
	else
		OPEN := open
	endif
endif

# Virtual environment executables
ifndef TRAVIS
	BIN_ := $(BIN)/
endif
PYTHON := $(BIN_)python
PIP := $(BIN_)pip -q
EASY_INSTALL := $(BIN_)easy_install
PEP8 := $(BIN_)pep8
PEP257 := $(BIN_)pep257
PYLINT := $(BIN_)pylint
PYTEST := $(BIN_)py.test
COVERAGE := $(BIN_)coverage

# Flags for PHONY targets
INSTALLED_FLAG := $(ENV)/.installed
DEPENDS_CI_FLAG := $(ENV)/.depends-ci
DEPENDS_DOC_FLAG := $(ENV)/.depends-doc
DEPENDS_DEV_FLAG := $(ENV)/.depends-dev
DOCS_FLAG := $(ENV)/.docs
ALL_FLAG := $(ENV)/.all

# Main Targets #################################################################

.PHONY: all
all: depends
$(ALL_FLAG): $(SOURCES)
	$(MAKE) check
	touch $(ALL_FLAG)  # flag to indicate all setup steps were successful

.PHONY: ci
ifdef TRAVIS
ci: check test tests
else
ci: check test tests #doc
endif

# Development Installation #####################################################

.PHONY: env
env: $(PIP) $(INSTALLED_FLAG)
$(INSTALLED_FLAG): Makefile setup.py requirements.txt
	VIRTUAL_ENV=$(ENV) $(PYTHON) setup.py develop
	@ touch $(INSTALLED_FLAG)  # flag to indicate package is installed

$(PIP):
	$(SYS_PYTHON) -m venv --clear $(ENV)
	$(PIP) install --upgrade pip setuptools

# Tools Installation ###########################################################

.PHONY: depends
depends: depends-ci depends-dev

.PHONY: depends-ci
depends-ci: env Makefile $(DEPENDS_CI_FLAG)
$(DEPENDS_CI_FLAG): Makefile
	$(PIP) install --upgrade pep8 pep257 pylint coverage pytest pytest-describe pytest-expecter pytest-cov pytest-random pytest-runfailed
	@ touch $(DEPENDS_CI_FLAG)  # flag to indicate dependencies are installed

.PHONY: depends-dev
depends-dev: env Makefile $(DEPENDS_DEV_FLAG)
$(DEPENDS_DEV_FLAG): Makefile
	$(PIP) install --upgrade pip pep8radius wheel pyinotify
	@ touch $(DEPENDS_DEV_FLAG)  # flag to indicate dependencies are installed

# Static Analysis ##############################################################

.PHONY: check
check: pep8 pep257 #pylint

.PHONY: pep8
pep8: depends-ci
	$(PEP8) $(PACKAGE) tests --config=.pep8rc

.PHONY: pep257
pep257: depends-ci
	$(PEP257) $(PACKAGE) tests

.PHONY: pylint
pylint: depends-ci
	$(PYLINT) $(PACKAGE) tests --rcfile=.pylintrc

.PHONY: fix
fix: depends-dev
	$(PEP8RADIUS) --docformatter --in-place

# Testing ######################################################################

RANDOM_SEED ?= $(shell date +%s)

PYTEST_CORE_OPTS := --doctest-modules -r xXw -vv
PYTEST_COV_OPTS := --cov=$(PACKAGE) --no-cov-on-fail --cov-report=term-missing
PYTEST_RANDOM_OPTS := --random --random-seed=$(RANDOM_SEED)

PYTEST_OPTS := $(PYTEST_CORE_OPTS) $(PYTEST_COV_OPTS) $(PYTEST_RANDOM_OPTS)
PYTEST_OPTS_FAILFAST := $(PYTEST_OPTS) --failed --exitfirst

FAILED_FLAG := .pytest/failed

.PHONY: test test-unit
test: test-unit
test-unit: depends-ci
	$(PYTEST) $(PYTEST_OPTS) $(PACKAGE)
ifndef TRAVIS
	$(COVERAGE) html --directory htmlcov --fail-under=$(UNIT_TEST_COVERAGE)
endif

.PHONY: test-int
test-int: depends-ci
	@ if test -e $(FAILED_FLAG); then $(MAKE) test-all; fi
	$(PYTEST) $(PYTEST_OPTS_FAILFAST) tests
ifndef TRAVIS
	@ rm -rf $(FAILED_FLAG)  # next time, don't run the previously failing test
	$(COVERAGE) html --directory htmlcov --fail-under=$(INTEGRATION_TEST_COVERAGE)
endif

.PHONY: tests test-all
tests: test-all
test-all: depends-ci
	@ if test -e $(FAILED_FLAG); then $(PYTEST) --failed $(PACKAGE) tests; fi
	$(PYTEST) $(PYTEST_OPTS_FAILFAST) $(PACKAGE) tests
ifndef TRAVIS
	@ rm -rf $(FAILED_FLAG)  # next time, don't run the previously failing test
	$(COVERAGE) html --directory htmlcov --fail-under=$(COMBINED_TEST_COVERAGE)
endif

.PHONY: read-coverage
read-coverage:
	$(OPEN) htmlcov/index.html

# Cleanup ######################################################################

.PHONY: clean
clean: .clean-test .clean-env .clean-build
	rm -rf $(ALL_FLAG)

.PHONY: .clean-build
.clean-build:
	find $(PACKAGE) tests -name '*.pyc' -delete
	find $(PACKAGE) tests -name '__pycache__' -delete
	rm -rf $(INSTALLED_FLAG) *.egg-info

.PHONY: .clean-test
.clean-test:
	rm -rf .pytest .coverage htmlcov

.PHONY: .clean-env
.clean-env: clean
	rm -rf $(ENV)

# System Installation ##########################################################

.PHONY: develop
develop:
	$(SYS_PYTHON) setup.py develop

.PHONY: install
install:
	$(SYS_PYTHON) setup.py install
