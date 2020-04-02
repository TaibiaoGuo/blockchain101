##  运行方法
> 如果拉取失败尝试注册并登陆一下阿里云的容器镜像服务（free）

docker run --rm registry.cn-shenzhen.aliyuncs.com/blockchain101/ipfs

## 本地构建

docker build -t ipfs:latest .

docker run --rm ipfs:latest
