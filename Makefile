
cli:
	docker run -it --name portfolio-manager -p 80:80 -v $(pwd)/app:/app portfolio-manager bash

# ---------------------------------------------------------------------------

build:
	docker build -t portfolio-manager . --no-cache



# ----------------------------------------------------------------------------

JOB ?= none
BUILD ?= none

# ----------------------------------------------------------------------------
docker-update-builder:
	docker pull $(BUILDER_NAME):$(IMAGE_TAG)

docker-update-vmuploader:
	docker pull $(VMUPLOADER_NAME):$(IMAGE_TAG)
	