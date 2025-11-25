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

remove-config: ## Remove config
	rm -fr ~/.pvcscr

create-bin: ## Create binary
	python3 generate_version_file.py
	pip install pyinstaller
	pyinstaller --onefile --windowed pvcscr.py
