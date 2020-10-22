## 简介
slogan: meet, catch.

实验二是一个主打校内快速交友的匿名去中心化聊天软件。

* 漂流瓶功能：用户可以随机发送一条消息，消息将随机传递给至多5个在线用户，
收到的用户可以通过一下个跳到接收到的下一个漂流瓶；
* 聊天功能：最先回复的用户将与漂流瓶的发起者建立私聊，彼此最多说10句话并最多聊3分钟。
每个用户每小时会拥有3个聊天延长器来延长聊天。


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