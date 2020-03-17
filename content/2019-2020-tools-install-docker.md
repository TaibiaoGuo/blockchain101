+++
title = "Docker安装指南"
date = 2020-03-17T01:00:00Z
description = "Docker安装指南"
categories = ["Docker"]
type = "post"
+++

本指南用于在阿里云服务器上安装Docker

## 一、PC端安装步骤总览

#### 1、安装前检查清单

 已经兑换了阿里云服务器

#### 2、重装阿里云服务器操作系统

> 为了避免不必要的错误，因此这里直接让大家重装阿里云的操作系统

**2.1 登陆阿里云官网**

访问阿里云官方网站 https://www.aliyun.com/ 并登陆阿里云官网

{{< figure src="/blockchain101/images/post/2019-2020-tools-install-docker/2-1-1.png"  alt="" width="100%"  >}}

{{< figure src="/blockchain101/images/post/2019-2020-tools-install-docker/2-1-2.png"  alt="" width="100%"  >}}

**2.2 进入阿里云控制面板** 

{{< figure src="/blockchain101/images/post/2019-2020-tools-install-docker/2-2-1.png"  alt="" width="100%"  >}}

{{< figure src="/blockchain101/images/post/2019-2020-tools-install-docker/2-2-2.png"  alt="" width="100%"  >}}

{{< figure src="/blockchain101/images/post/2019-2020-tools-install-docker/2-2-3.png"  alt="" width="100%"  >}}

**2.3 停止实例**

{{< figure src="/blockchain101/images/post/2019-2020-tools-install-docker/2-3-1.png"  alt="" width="100%"  >}}

{{< figure src="/blockchain101/images/post/2019-2020-tools-install-docker/2-3-2.png"  alt="" width="100%"  >}}

**2.4 更换操作系统**

{{< figure src="/blockchain101/images/post/2019-2020-tools-install-docker/2-4-1.png"  alt="" width="100%"  >}}

{{< figure src="/blockchain101/images/post/2019-2020-tools-install-docker/2-4-2.png"  alt="" width="100%"  >}}

{{< figure src="/blockchain101/images/post/2019-2020-tools-install-docker/2-4-3.png"  alt="" width="100%"  >}}

{{< figure src="/blockchain101/images/post/2019-2020-tools-install-docker/2-4-5.png"  alt="" width="100%"  >}}

#### 3、通过网页版SSH连接服务器

**3.1 远程连接服务器**

{{< figure src="/blockchain101/images/post/2019-2020-tools-install-docker/3-1-1.png"  alt="" width="100%"  >}}

{{< figure src="/blockchain101/images/post/2019-2020-tools-install-docker/3-1-2.png"  alt="" width="100%"  >}}

#### 4、执行安装docker命令

**4.1 执行安装docker命令**

```
curl -sSL https://get.daocloud.io/docker -o d.sh && chmod +x d.sh && ./d.sh --mirror Aliyun && rm d.sh
```

{{< figure src="/blockchain101/images/post/2019-2020-tools-install-docker/4-1-1.png"  alt="" width="100%"  >}}

**4.2 等待命令执行完毕**

{{< figure src="/blockchain101/images/post/2019-2020-tools-install-docker/4-1-2.png"  alt="" width="100%"  >}}

#### 5、检查Docker是否安装成功

**5.1 执行测试命令**
```
curl -sSL https://get.daocloud.io/docker -o d.sh && chmod +x d.sh && ./d.sh --mirror Aliyun && rm d.sh
```
{{< figure src="/blockchain101/images/post/2019-2020-tools-install-docker/4-2-1.png"  alt="" width="100%"  >}}

**5.2 通过运行结果判断是否成功**

{{< figure src="/blockchain101/images/post/2019-2020-tools-install-docker/4-2-2.png"  alt="" width="100%"  >}}

#### 6、关闭网页
`5.2`成功后，即可关闭网页离开。

> docker安装完成后无需在每次访问服务器时执行 `4.1 docker安装`，只需要安装一次，除非docker损坏（可通过`5.1`进行判断）。
>
> 手机端和网页端访问的是同一台服务器，两种安装方式只需要按照流程执行一种即可。

## 二、手机端安装步骤总览

#### 1、安装前检查清单

 - 已经兑换了阿里云服务器
 - 已经下载了阿里云APP

 #### 2、重装操作系统

 #### 3、在手机端访问服务器

 #### 4、执行安装命令

 #### 5、执行测试命令

 #### 6、退出阿里云APP


### 三、可选（不执行不影响本课程学习）
因为众所周知的网络原因，我在从 hub.docker.com 中拉取镜像时常会因为网络故障出现失败，这时我们需要为docker添加仓库镜像，分别复制以下命令到终端并按回车执行：
```
sudo mkdir -p /etc/docker
```
```
sudo tee /etc/docker/daemon.json <<-'EOF'
{
  "registry-mirrors": [
    "https://dockerhub.azk8s.cn",
    "https://hub-mirror.c.163.com"
  ]
}
EOF
```
```
sudo systemctl daemon-reload
```
```
sudo systemctl restart docker
```

---
<a rel="license" href="http://creativecommons.org/licenses/by-nc-sa/4.0/"><img alt="知识共享许可协议" style="border-width:0" src="https://i.creativecommons.org/l/by-nc-sa/4.0/88x31.png" /></a><br />本作品采用<a rel="license" href="http://creativecommons.org/licenses/by-nc-sa/4.0/">知识共享署名-非商业性使用-相同方式共享 4.0 国际许可协议</a>进行许可。
