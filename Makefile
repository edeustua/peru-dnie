##@ Development

venv: ## Create python venv environment
	python3 -m venv venv
.PHONY: venv

format: ## Format project
	black src/ tests/
.PHONY: black

validate: ## Run static analysis
	mypy --strict src/
.PHONY: validate

test: ## Run tests
	pytest \
		-v \
		--capture no \
		--pointers-report \
		--pointers-func-min-pass=1 \
		./tests
.PHONY: test

##@ Help

# An automatic help command: https://www.padok.fr/en/blog/beautiful-makefile-awk
.DEFAULT_GOAL := help

help: ## (DEFAULT) This command, show the help message
	@echo "Create a python local environment"
	@echo "  > make venv"
	@echo ""
	@awk 'BEGIN {FS = ":.*##"; printf "\nUsage:\n  make \033[36m<target>\033[0m\n"} /^[a-zA-Z_0-9-]+:.*?##/ { printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2 } /^##@/ { printf "\n\033[1m%s\033[0m\n", substr($$0, 5) } ' $(MAKEFILE_LIST)
.PHONY: help
