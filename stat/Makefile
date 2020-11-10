#!/usr/bin/env bash

export GOPROXY?=https://proxy.golang.org/

# Get the currently used golang install path (in GOPATH/bin, unless GOBIN is set)
ifeq (,$(shell go env GOBIN))
GOBIN=$(shell go env GOPATH)/bin
else
GOBIN=$(shell go env GOBIN)
endif

APPName ?= blockchain101-IssueStatServer

##@ General

.PHONY: help
help:  ## 显示帮助信息
	@echo "使用本工具前请确保docker正常运行"
	@awk 'BEGIN {FS = ":.*##"; printf "\nUsage:\n  make \033[36m<target>\033[0m\n"} /^[a-zA-Z_0-9-]+:.*?##/ { printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2 } /^##@/ { printf "\n\033[1m%s\033[0m\n", substr($$0, 5) } ' $(MAKEFILE_LIST)
	@echo "\n\n2020 ©️ \033[32mTaibiaoGuo/Blockchain101\033[0m 版权所有"

##@ 编译
.PHONY: all
all: ## 测试、编译成镜像、运行镜像

.PHONY: build
build: ## 本地编译
	go build -o bin/$(APPName) ./cmd

.PHONY: install
install: ## 本地安装
	make build
	cp ./bin/$(APPName) $(shell go env GOPATH)/bin/$(APPName)

##@ 开发

.PHONY: lint
lint: golangci-lint ## Run golangci lint checks
	@$(GOLANGCI_LINT) run

lint-fix: golangci-lint ## Run golangci lint to automatically perform fixes
	@$(GOLANGCI_LINT) run --fix

golangci-lint:
ifeq (, $(shell which golangci-lint))
	@{ \
	set -e ;\
	curl -sSfL https://raw.githubusercontent.com/golangci/golangci-lint/master/install.sh | sh -s -- -b $(shell go env GOPATH)/bin v1.29.0 ;\
	}
GOLANGCI_LINT=$(shell go env GOPATH)/bin/golangci-lint
else
GOLANGCI_LINT=$(shell which golangci-lint)
endif

##@ 测试

.PHONY: go-test
go-test: ## 执行测试 ($ go test -v ./cmd/... ./pkg/...)
	go test -race -v ./cmd/... ./pkg/...

.PHONY: test-coverage
test-coverage:  ## Run coveralls
	# remove all coverage files if exists
	- rm -rf *.out
	# run the go tests and gen the file coverage-all used to do the integration with coverrals.io
	go test -race -failfast -tags=integration -coverprofile=coverage-all.out ./pkg/... ./cmd/...