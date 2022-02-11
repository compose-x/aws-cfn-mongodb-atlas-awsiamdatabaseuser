.PHONY: clean clean-test clean-pyc clean-build docs help
.DEFAULT_GOAL := help

define BROWSER_PYSCRIPT
import os, webbrowser, sys

from urllib.request import pathname2url

webbrowser.open("file://" + pathname2url(os.path.abspath(sys.argv[1])))
endef
export BROWSER_PYSCRIPT

define PRINT_HELP_PYSCRIPT
import re, sys

for line in sys.stdin:
	match = re.match(r'^([a-zA-Z_-]+):.*?## (.*)$$', line)
	if match:
		target, help = match.groups()
		print("%-20s %s" % (target, help))
endef
export PRINT_HELP_PYSCRIPT

BROWSER := python -c "$$BROWSER_PYSCRIPT"

ifndef BUCKET
BUCKET	:= eu-west-1.files.ews-network.net
endif
ifndef PYTHON_VERSION
PYTHON_VERSION	:= python37
endif


help:
	@python -c "$$PRINT_HELP_PYSCRIPT" < $(MAKEFILE_LIST)

clean: clean-build clean-test ## remove all build, test, coverage and Python artifacts

clean-build: ## remove build artifacts
	rm -fr build/
	rm -fr dist/
	rm -fr src/dist
	rm -fr .eggs/
# 	find . -name '*.egg-info' -exec rm -fr {} +
# 	find . -name '*.egg' -exec rm -rf {} +

clean-test: ## remove test and coverage artifacts
	rm -fr .tox/
	rm -f .coverage
	rm -fr htmlcov/
	rm -fr .pytest_cache

lint:	conform ## check style with flake8
	flake8 cfn_kafka_topic_provider tests

test: ## run tests quickly with the default Python
	pytest

test-all: ## run tests on every Python version with tox
	tox

coverage: ## check code coverage quickly with the default Python
	coverage run --source src -m pytest
	coverage report -m
	coverage html
	$(BROWSER) htmlcov/index.html

docs: ## generate Sphinx HTML documentation, including API docs
	rm -f docs/cfn_kafka_topic_provider.rst
	rm -f docs/modules.rst
	sphinx-apidoc -o docs/ src
	$(MAKE) -C docs clean
	$(MAKE) -C docs html
	$(BROWSER) docs/_build/html/index.html

servedocs: docs ## compile the docs watching for changes
	watchmedo shell-command -p '*.rst' -c '$(MAKE) -C docs html' -R -D .

conform	: ## Conform to a standard of coding syntax
	isort --profile black src
	black src
	find src -name "*.json" -type f  -exec sed -i '1s/^\xEF\xBB\xBF//' {} +

python38	: dist
			test -d build && rm -rf build || mkdir build
			docker run -u $(shell bash -c 'id -u'):$(shell bash -c 'id -u') \
			--rm -it -v $(PWD):/app --entrypoint /bin/bash \
			lambci/lambda:build-python3.8 \
			-c "pip install /app/dist/*.whl -t /app/build"

python37	: dist
			test -d build && rm -rf build || mkdir build
			docker run -u $(shell bash -c 'id -u'):$(shell bash -c 'id -u') \
			--rm -it -v $(PWD):/app --entrypoint /bin/bash \
			lambci/lambda:build-python3.7 \
			-c "pip install /app/dist/*.whl -t /app/build"


dist:		clean ## builds source and wheel package
			poetry build

requirements:	clean $(PYTHON_VERSION)
			poetry update
			poetry export --without-hashes > requirements.txt

package:	dist $(PYTHON_VERSION)

make build:		requirements

resource-zip:
				jq < mongodb-atlas-awsiamdatabaseuser.json > schema.json
				cd build; zip -q -r9 ../ResourceProvider.zip * ; cd -
				zip -D -r9 mongodb-atlas-awsiamdatabaseuser-manual.zip \
				schema.json \
				.rpdk-config \
				ResourceProvider.zip \
				src \
				inputs
