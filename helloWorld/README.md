##  运行方法
> 需先登陆阿里云镜像服务

docker run --rm registry.cn-shenzhen.aliyuncs.com/blockchain101/hello_blockchain

## 本地构建

docker build -t hello_blockchain:latest .

docker run --rm hello_blockchain:latest
