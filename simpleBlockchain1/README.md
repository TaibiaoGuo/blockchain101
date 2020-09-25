## 简介
一个简单区块链，其中每个区块都指向上一个区块。
这是一个区块链的基本的实现，不包含工作证明或点对点等高级功能。
区块链功能的基本实现，可以通过动作集对区块链进行操作。
运行成功后按照提示进行操作即可。
##  运行方法

> 首先需要安装docker
>
> 如果拉取失败尝试注册并登陆一下阿里云的容器镜像服务（free）

docker run --rm -it registry.cn-shenzhen.aliyuncs.com/blockchain101/simpleblockchain1

# 本地构建

您可以在本地构建本程序。

## 本地快速构建-Linux环境

编译本程序
```shell script
make build
```

运行本程序
```shell script
make run
```

## 本地手动构建-Windows\Linux环境

Windows环境构建镜像需要先安装docker，然后：

编译本程序
```shell script
docker build -t simpleblockchain1:latest .
```
运行本程序
```shell script
docker run --rm -it simpleblockchain1:latest
```