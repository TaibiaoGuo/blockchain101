## 简介
以太坊实验
##  运行方法

> 首先需要在本机安装docker和docker-compose，可以试试在线docker环境[kdtakoda](https://www.katacoda.com/courses/docker/playground)



## 搭建以太坊私有链

### 1、拉取实验源代码
分别执行下列命令拉取实验源代码
```bash
git clone --branch experiment https://github.com/TaibiaoGuo/blockchain101.git

cd blockchain101/ethereum/
```

以太坊实验代码目录结构如下:

```sh
.
├── docker-compose-standalone.yml # 单独启动一个eth节点
├── docker-compose.yml # 单独启动一个eth节点， 一个初始节点， 一个网络状态
├── eth-netstats # 网络状态
│   └── Dockerfile
├── genesis # 初始化配置
│   ├── genesis.json
│   ├── keystore # 初始化 配置账户
│   │   ├── UTC--2018-03-20T06-02-05.635648305Z--d6e2f555878f29ca190b8ef6bf7de334e1c47e51
├── geth-node # 以太坊节点+api
│   ├── app.json
│   ├── Dockerfile
│   └── start.sh
├── install-compose.sh
└── README.md

```

执行下列命令启动实验环境:
> 需要进行代码的编译，需要等待一些时间

```bash
docker-compose up -d
```

执行下列命令查看运行情况:
```bash
docker ps
```

可以看到类似的运行状态：
```
CONTAINER ID        IMAGE                      COMMAND                  CREATED             STATUS              PORTS                                                                                             NAMES
59380c23b730        ethereumdocker_eth         "/root/start.sh '--d…"   5 seconds ago       Up 3 seconds        8545-8546/tcp, 30303/tcp, 30303-30304/udp                                                         ethereumdocker_eth_1
fbe34c9110b1        ethereumdocker_bootstrap   "/root/start.sh '--d…"   5 seconds ago       Up 4 seconds        0.0.0.0:8545->8545/tcp, 0.0.0.0:30303->30303/tcp, 8546/tcp, 0.0.0.0:30303->30303/udp, 30304/udp   bootstrap
4d77ae7e987e        ethereumdocker_netstats    "npm start"              6 seconds ago       Up 4 seconds        0.0.0.0:3000->3000/tcp                                                                            netstats
```

这代码运行成功，我们可以打开区块链浏览器查看可视化的以太坊状态界面：

首先在katacoda 访问你的实验环境对应的3000端口对应的以太坊可视化界面。
> katacoda实验环境命令行界面顶端+按钮，选择 select port to view on HOST 1, 填入3000，访问以太坊可视化界面。

这代表就是运行成功了。 

![netstats.png](https://upload-images.jianshu.io/upload_images/6167081-25a3e4587dd2e81e.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

现在你就能看到两个节点:

- bootstrap  # 初始化节点
- e69fe54d216d # 新加入的节点

接下来添加多个节点

```sh
# docker-compose scale 作用是启动多个eth服务
docker-compose scale eth=3
```

出现了三个新的node节点:

- e69fe54d216d
- 55f0f83728db
- 1770aec8a167

![netstats.png](https://upload-images.jianshu.io/upload_images/6167081-d553072ba9fdce25.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

### 使用geth

使用docker exec进行与geth的交互

```sh
# 格式 docker exec -it ethereumdocker_eth_{第几个节点} geth attach ipc://root/.ethereum/devchain/geth.ipc
docker exec -it ethereumdocker_eth_1 geth attach ipc://root/.ethereum/devchain/geth.ipc
```

进入docker内部的geth就可以正常的使用geth的功能了.   
阅读geth文档: 
- [geth文档](https://www.ethereum.org/cli)

```sh
Welcome to the Geth JavaScript console!

instance: Geth/v1.8.3-unstable-faed47b3/linux-amd64/go1.10
coinbase: 0xd6e2f555878f29ca190b8ef6bf7de334e1c47e51
at block: 0 (Thu, 01 Jan 1970 00:00:00 UTC)
 datadir: /root/.ethereum/devchain
 modules: admin:1.0 debug:1.0 eth:1.0 miner:1.0 net:1.0 personal:1.0 rpc:1.0 txpool:1.0 web3:1.0

> admin.nodeInfo.enode
"enode://3732c434c5330205b12ef83e31e59dd36b6d04fc8392770057a05b678483524c2c5649932bc3cc8bced54d94befbd0fda6daae988243489ce0faecfa7a5b0914@[::]:30303"
> # geth cli
```

### 开始挖矿

节点是默认不挖矿的需要手动开启挖矿:

```sh
docker exec -it ethereumdocker_eth_1 geth attach ipc://root/.ethereum/devchain/geth.ipc
# 开始挖矿
miner.start()
```

等带一段时间后,就能重127.0.0.1:3000看到区块了.

```sh
# eth 查看用户
eth.accounts
```

```sh
# stop 停止挖矿
miner.stop()
```

到此以太坊的local本机就开发好了,但是会出现其他的问题

- 以太坊钱包冲突,因为以太坊钱包的端口也是30303,8545

解决方法:

- 你可以修改docker-compose里的端口映射

或者使用docker-machine进行docker隔离(强推)


文献参考:

- [Docker — 从入门到实践](https://www.gitbook.com/book/yeasy/docker_practice/details)
- [go-ethereum](https://github.com/ethereum/go-ethereum)