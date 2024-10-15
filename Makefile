SOURCE_COMMIT := $$(git rev-parse --short HEAD)
IMAGE_NAME := modeemi/website:latest
DOCKER_TAG := latest

test:
	docker-compose up -d
	tox

build:
	docker build -t "${IMAGE_NAME}" --build-arg "SOURCE_COMMIT=${SOURCE_COMMIT}" --build-arg "DOCKER_TAG=${DOCKER_TAG}" .

run:
	docker run ${IMAGE}

push:
	docker push ${IMAGE}

pull:
	docker pull ${IMAGE}

default:
	make test

update:
	make build
	make push

all:
	make test
	make build
	make push

.PHONY: all default test build push pull run update
