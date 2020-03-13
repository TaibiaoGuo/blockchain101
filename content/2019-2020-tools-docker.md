+++
title = "Docker使用帮助"
date = 2020-03-12T01:00:00Z
description = "Docker使用帮助"
categories = ["Docker使用帮助"]
type = "post"
+++

在本课程的实验课程代码和工具都使用docker进行了打包，以方便学习和复现。
> 为了使用docker，首先需要安装并配置docker，并开通阿里云镜像仓库并设置密码，见第下文`docker安装和配置`部分。
#### 名词解释
本文中出现的你可能不理解的名词的简单说明

| 名词 | 解释 |
| --- | --- |
| docker | 为我们课堂提供可重复实验的统一环境的一个软件 |
| 容器 | 类似于虚拟机的虚拟化技术 |
| 镜像 | 打包好的容器 |
| 镜像仓库 | 存放制作好的镜像的服务 |
| 仓库镜像 | 镜像仓库的镜像可以加速镜像的下载速度 |
| 终端 | 就是可以登陆你服务器后的黑框框 |

### docker命令备忘
下面列表中的命令囊括了你在课程中所需的所有命令：
```
docker pull [容器名]        # 从仓库拉取一个容器
docker run [镜像名称]       # 启动容器
docker ps                   # 列出正在运行的容器
docker ps -a                # 列出所有容器（包含已停止的） 
docker stop [容器ID]        # 停止一个容器
docker rm [容器ID]          # 删除一个容器（需要先停止容器）
docker images               # 列出所有镜像
docker login [账号] [仓库]    # 登陆阿里云镜像仓库
```

### docker安装和配置
-  安装docker(约3-10分钟)，复制以下命令到终端并按回车执行：
```
curl -sSL https://get.daocloud.io/docker | sh
```

若正确安装，则屏幕上会显示类似画面（若未正确安装，请直接联系老师）：
```
root@iZwz9h1p22ljpx2xd6b2byZ:~# curl -sSL https://get.daocloud.io/docker | sh
# Executing docker install script, commit: 442e66405c304fa92af8aadaa1d9b31bf4b0ad94
+ sh -c apt-get update -qq >/dev/null
+ sh -c DEBIAN_FRONTEND=noninteractive apt-get install -y -qq apt-transport-https ca-certificates curl >/dev/null
+ sh -c curl -fsSL "https://download.docker.com/linux/ubuntu/gpg" | apt-key add -qq - >/dev/null
Warning: apt-key output should not be parsed (stdout is not a terminal)
+ sh -c echo "deb [arch=amd64] https://download.docker.com/linux/ubuntu bionic stable" > /etc/apt/sources.list.d/docker.list
+ sh -c apt-get update -qq >/dev/null
+ [ -n  ]
+ sh -c apt-get install -y -qq --no-install-recommends docker-ce >/dev/null
+ sh -c docker version
Client: Docker Engine - Community
 Version:           19.03.8
 API version:       1.40
 Go version:        go1.12.17
 Git commit:        afacb8b7f0
 Built:             Wed Mar 11 01:25:46 2020
 OS/Arch:           linux/amd64
 Experimental:      false

Server: Docker Engine - Community
 Engine:
  Version:          19.03.8
  API version:      1.40 (minimum version 1.12)
  Go version:       go1.12.17
  Git commit:       afacb8b7f0
  Built:            Wed Mar 11 01:24:19 2020
  OS/Arch:          linux/amd64
  Experimental:     false
 containerd:
  Version:          1.2.13
  GitCommit:        7ad184331fa3e55e52b890ea95e65ba581ae3429
 runc:
  Version:          1.0.0-rc10
  GitCommit:        dc9208a3303feef5b3839f4323d9beb36df0a9dd
 docker-init:
  Version:          0.18.0
  GitCommit:        fec3683
If you would like to use Docker as a non-root user, you should now consider
adding your user to the "docker" group with something like:

  sudo usermod -aG docker your-user

Remember that you will have to log out and back in for this to take effect!

WARNING: Adding a user to the "docker" group will grant the ability to run
         containers which can be used to obtain root privileges on the
         docker host.
         Refer to https://docs.docker.com/engine/security/security/#docker-daemon-attack-surface
         for more information.
```

- 1.2 设置完成后，为了测试是否设置正确，下载我们课程的`hello_blockchain`镜像以测试,在终端中复制其提示的命令并回车:
```
docker run --rm registry.cn-shenzhen.aliyuncs.com/blockchain101/hello_blockchain
```
若成功，则在终端会显示`blockchain 101`的字符画并退出。至此，完全课程环境初始化工作，后续每次课程实验只需执行对应命令即可进入课程环境。

### 可选（不执行不影响本课程学习）
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
