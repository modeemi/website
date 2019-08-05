RELEASE := $$(git show -s --format=%H)
IMAGE := modeemi/intternetvelho

test:
	@echo "Running tests and linters"
	python manage.py test

build:
	docker build --build-arg RELEASE=${RELEASE} -t ${IMAGE} .

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
