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
docker run --rm -it \
 -p 12476:12476 \
 -p 12476:12476/udp \
 -p 12478:12478 \
 -p 12478:12478/udp \
 p2pchat:latest
```

## 设计概要

### 架构
p2pChat包括GUI模块、消息处理模块、P2P通讯模块。

```
+------------------------------------------------+
|                                                |
|                                                |
|                                                |
|                                                |
|                                                |
|                                                |
|                                                |
|                                                |
|                                                |
|                                                |
|                                                |
|                                                |
|                                                |
|                                                |
|                                                |
|                                                |
|                                                |
|                                                |
|                                                |
+------------------------------------------------+
```

### 通讯

#### 身份认证
p2pChat使用RSA密钥生成RSA公钥，使用RSA公钥和SHA256算法生成节点id。

#### 通讯协议

p2pChat使用socket作为基础的通讯协议。

#### 通讯格式

p2pChat的消息使用JSON格式进行组织，并使用base64进行编码。

#### 通讯认证

p2pChat的消息使用RSA数字签名和Hash来确保消息的完整性和确认消息发送者。

#### 加密方式

p2pChat的消息使用RSA非对称加密协商通讯密钥，使用对称加密加密消息。RSA密钥在p2pChat启动时生成。

#### 路由寻址

p2pChat使用[Kademlia DHT](https://en.wikipedia.org/wiki/Kademlia)进行去中心化的路由寻址，寻找在线节点。


### 漂流瓶

#### 生命周期

* **创建端创建漂流瓶**：

    * 初始化漂流瓶对象

    * **创建端创建漂流瓶响应队列**：创建漂流瓶响应队列`bottle_{bottle.id}_FIFO_queque`用于接收最近节点的响应

    * **创建端生成漂流瓶id**： `bottle.id = SHA256(bottle.timestamp + bottle.body)`

* **漂流瓶流浪**：漂流瓶通过异或算法经过最多5轮迭代寻找与`bottle.id` "距离"最近的3个节点的`peer.id`

* **响应漂流瓶**： 每轮迭代，收到漂流瓶的节点从`beach_queue`中取出收到的漂流瓶，抛弃过期的漂流瓶，
将迭代未完成的漂流瓶重新丢入大海迭代。对于新鲜的漂流瓶，
发送消息至漂流瓶发送者的漂流瓶响应队列`bottle_{bottle.id}_FIFO_queque`。

* **创建端回复**： 漂流瓶创建端


其中，漂流瓶对象为：

```json
{
"timestamp" : "",
"bottleId" : "",
"gas" : 5,
"sender" : "",
"receiver" : "",
"sign" : "",
"body" : "",
"nearestPeerIdList" : [
{"peerId":"","peerIP" : "","peerPort":""},
{"peerId":"","peerIP" : "","peerPort":""},
{"peerId":"","peerIP" : "","peerPort":""},
{"peerId":"","peerIP" : "","peerPort":""},
{"peerId":"","peerIP" : "","peerPort":""}
]
}
```

### 沙滩

#### 待读的漂流瓶

#### 中转的漂流瓶

### 聊天

#### 开始聊天

从漂流瓶队列中取一个漂流瓶

### 消息

#### 消息格式

```json
{
"timestamp":"",
"sender":"",
"receiver":"",
"sign":"",
"body":""
}
```

### 可视化
p2pChat使用Python模块`tkinter`构建了程序GUI前端。

### 持久化

#### 日志信息

p2pChat使用了Python模块`logging`将日志信息记录在文件`./log`中，日志可以被docker获取到，

#### 数据库
p2pChat使用Python模块`sqlite3`持久化存储了聊天记录、节点信息等信息在文件`./`；

### 性能优化
Python有全局解释锁GIL，程序GUI前端有渲染任务，为了确保程序GUI前端和服务后端不发生锁的抢占导致程序出现卡顿，
本程序使用了Python的多进程模块`multiprocessing`和队列模块`queue`让GUI前端和服务后端在两个进程里并行运行，使用队列进行异步通讯，
确保Python的全局解释锁不会影响程序的性能。