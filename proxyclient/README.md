## 功能
加速访问github

使用了端口7000 70001 7002

## 运行方式
> 注意: 只支持有公网IP的云服务器，且本工具只在课程期间有效

```
sudo docker run -restart=always --network host -d --name proxyclient -e REDEMPTIONCODE=此处填你的云服务器兑换码  registry.cn-shenzhen.aliyuncs.com/blockchain101/proxyclient
```

