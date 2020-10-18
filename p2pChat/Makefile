IMAGE_NAME ?= p2pchat
VERSION ?= latest
CONTAINER_NAME ?= $(IMAGE_NAME)

build_run_clean: build run
.PHONY: build_run

.PHONY: build
build:
	@echo 'start build image $(IMAGE_NAME):$(VERSION)'
	docker build -t $(IMAGE_NAME):$(VERSION) .

.PHONY: run
run:
	@echo 'start run image $(IMAGE_NAME):$(VERSION)'
	docker run --rm --name $(CONTAINER_NAME) -it \
	 -p 12476:12476 \
	 -p 12476:12476/udp \
	 -p 12478:12478 \
	 -p 12478:12478/udp \
	$(IMAGE_NAME):$(VERSION)

.PHONY: bash
bash:
	docker run --rm --name $(CONTAINER_NAME) -it \
	 -p 12476:12476 \
	 -p 12476:12476/udp \
	 -p 12478:12478 \
	 -p 12478:12478/udp \
	$(IMAGE_NAME):$(VERSION) bash

.PHONY: clean
clean:
	@echo 'stop container $(CONTAINER_NAME) and delete image $(IMAGE_NAME):$(VERSION)'
	docker stop $(CONTAINER_NAME) || true && docker rm -f $(CONTAINER_NAME) || true && docker rmi $(IMAGE_NAME):$(VERSION) || true

.PHONY: aliyun
aliyun:
	@echo 'pull image from  aliyun  and run image $(IMAGE_NAME):$(VERSION)'
	docker run --rm --name $(CONTAINER_NAME) -it \
	 -p 12476:12476 \
	 -p 12476:12476/udp \
	 -p 12478:12478 \
	 -p 12478:12478/udp \
	registry.cn-shenzhen.aliyuncs.com/blockchain101/$(IMAGE_NAME):$(VERSION)