all: help

.PHONY: help
help: Makefile
	@echo
	@echo " Choose a make command to run"
	@echo
	@sed -n 's/^##//p' $< | column -t -s ':' |  sed -e 's/^/ /'
	@echo

## init: run this once to initialize a new python project
.PHONY: init
init:
	python3 -m venv .venv
	direnv allow .

## install: install project dependencies
.PHONY: install
install:
	python3 -m pip install --upgrade pip
	pip install -r requirements.txt
	pip freeze > piplock.txt

## start: run local project
.PHONY: start
start:
	clear
	@echo ""
	python -u main.py

## test: run unit tests
.PHONY: test
test:
	python -m unittest discover -s tests -p "*_test.py"

## build: build package
.PHONY: build
build:
	rm -rf dist
	python3 setup.py sdist
	twine check dist/*

## deploy: upload package to pypi
.PHONY: deploy
deploy: build
	twine upload dist/*
