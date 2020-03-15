### 功能
加速访问github

| 端口|描述 |
|---|---|
|7000|proxyclient 监听端口 |
|7001| proxyclient api 监听端口|
|7002| proxyclient 反向代理端口|

### 运行方式
将`xxxxxxxxxxxxxxx`更改为你的兑换码，在你的云服务器中执行此行命令
```
sudo docker rm -f proxyclient ; \
sudo docker run --restart=always --network host -d --name proxyclient --env REDEMPTIONCODE=xxxxxxxxxxxxxxx \
registry.cn-shenzhen.aliyuncs.com/blockchain101/proxyclient
```
> 注: 只支持在有公网IP的云服务器运行，且需要先安装好docker，且本工具只在课程期间有效

### 查看文档
下载源代码，在项目根目录运行

```
godoc -http=:9090 -index
```


在浏览器访问 `127.0.0.1:9000`