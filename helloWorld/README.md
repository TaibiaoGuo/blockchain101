##  运行方法
> 如果拉取失败尝试注册并登陆一下阿里云的容器镜像服务（free）

docker run --rm registry.cn-shenzhen.aliyuncs.com/blockchain101/hello_blockchain

## 本地构建

docker build -t hello_blockchain:latest .

docker run --rm hello_blockchain:latest
