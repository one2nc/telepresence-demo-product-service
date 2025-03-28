IMAGE := "ttl.sh/telepresence-demo-product-svc:2h"

## Install for production
install:
	python -m pip install --upgrade pip
	python -m pip install -e .

## Install for development 
install-dev: install
	python -m pip install -e ".[dev]"

## Build dependencies
build: 
	pip-compile --resolver=backtracking --output-file=requirements.txt pyproject.toml
	pip-compile --resolver=backtracking --extra=dev --output-file=requirements-dev.txt pyproject.toml

build-docker: build
	docker build -t $(IMAGE) .
	docker push $(IMAGE)

## Format files using black
format:
	isort .
	black .

## create a cluster with k3d 
cluster-k3d:
	k3d cluster create devcluster --servers 1 --agents 3

## Set up Tilt
tilt: build
	tilt up

## Run checks (ruff + test)
check:
	ruff check .
	isort --check .
	black --diff --check .

fix: 
	ruff check --fix .
	isort .
	black .

deploy-dev: build-docker
	kubectl apply -f ./k8s/dev

deploy-dev-helm: build-docker 
	helm upgrade --install -f ./k8s/helm/dev.values.yaml products-svc --namespace api --create-namespace ./k8s/helm/dev
	