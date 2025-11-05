.PHONY: help
.DEFAULT_GOAL := help

help: ## This help
	@awk 'BEGIN {FS = ":.*?## "} /^[0-9a-zA-Z_-]+:.*?## / {printf "%-30s %s\n", $$1, $$2}' $(MAKEFILE_LIST)

env: ## Set virtual env
	python3 -m venv .venv
	@echo "use \"source .venv/bin/activate\" to enter in virtual env"

install: ## Install requirements
	pip install -r requirements.txt

run: ## Run app
	python3 pvcscr.py

create-bin: ## Create binary
	pip install pyinstaller
	pyinstaller --onefile --windowed pvcscr.py
