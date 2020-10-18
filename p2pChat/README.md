## 简介
点对点聊天
##  运行方法

> 首先需要安装docker
>
> 如果拉取失败尝试注册并登陆一下阿里云的容器镜像服务（free）

docker run --rm -it registry.cn-shenzhen.aliyuncs.com/blockchain101/p2pchat

# 本地构建

您可以在本地构建本程序。

## 本地快速编译构建-Linux环境

```shell script
make
```

## 本地手动构建-Windows\Linux环境

Windows环境构建镜像需要先安装docker，然后：

编译本程序
```shell script
docker build -t p2pchat:latest .
```
运行本程序
```shell script
docker run --rm -it p2pchat:latest
```

## 设计概要

### 路由寻址

[Kademlia DHT](https://en.wikipedia.org/wiki/Kademlia)进行去中心化的路由寻址，寻找在线用户。

### 通讯协议

socket通讯

