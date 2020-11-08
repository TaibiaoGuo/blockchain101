#!/usr/bin/env bash


##@ 帮助

.PHONY: help
help:  ## 显示帮助信息
	@echo "Blockchain101-以太坊实验"
	@awk 'BEGIN {FS = ":.*##"; printf "\n用法:\n  make \033[36m<target>\033[0m\n"} /^[a-zA-Z_0-9-]+:.*?##/ { printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2 } /^##@/ { printf "\n\033[1m%s\033[0m\n", substr($$0, 5) } ' $(MAKEFILE_LIST)
	@echo "\n2020 \033[32mBlockchain101\033[0m"

##@ 运行
.PHONY: run
run: ## 启动实验环境
	docker-compose up -d

.PHONY: stop
stop: ## 停止实验环境
	docker-compose stop

##@ 监控
.PHONY: log
log: ## 查看运行日志
	docker-compose logs

.PHONY: ps
ps: ## 列出运行的容器
	docker-compose ps

.PHONY: top
top: ## 显示运行的进程
	docker-compose top