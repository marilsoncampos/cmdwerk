SHELL:=/usr/bin/env bash
.DEFAULT_GOAL := build

build: ## Builds package using flit
	flit build

install: ## Install package using flit
	flit install

tests: ## Run pytest suite for the package
	@cd src/test
	pytest ./

checks: ## Check code base with pylint
	pylint  src/cmdwerk


help: ## show help message
	@awk 'BEGIN {FS = ":.*##"; printf "\nUsage:\n  make \033[36m\033[0m\n"} /^[$$()% a-zA-Z_-]+:.*?##/ { printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2 } /^##@/ { printf "\n\033[1m%s\033[0m\n", substr($$0, 5) } ' $(MAKEFILE_LIST)

