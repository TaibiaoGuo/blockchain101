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
本文中出现的你可能不理解的名词的简单解释
|名词 |解释 |
| ---|--- |
|docker | 运行和维护容器的一个软件，可以为我们课堂提供可重复实验的统一环境|
|容器|类似于虚拟机的虚拟化技术|
|镜像|打包好的容器|
| 镜像仓库|存放制作好的镜像的服务 |
|仓库镜像|镜像仓库的镜像，可以加速镜像的下载速度|
|终端|就是可以登陆你服务器后的黑框框|

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
#### 1、docker安装和配置
- 安装docker(约3-10分钟)，复制以下命令到终端并按回车执行：
```
curl -sSL https://get.daocloud.io/docker | sh
```
- 检查docker是否正确安装，复制以下命令到终端并按回车执行：
```
docker version
```
若正确安装，则屏幕上会显示类似画面（若未正确安装，请直接联系老师）：
```
root@iZ2zej14gd1joysruzdtk8Z:~# docker version
Client: Docker Engine - Community
 Version:           19.03.7
 API version:       1.40
 Go version:        go1.12.17
 Git commit:        7141c199a2
 Built:             Wed Mar  4 01:22:36 2020
 OS/Arch:           linux/amd64
 Experimental:      false

Server: Docker Engine - Community
 Engine:
  Version:          19.03.7
  API version:      1.40 (minimum version 1.12)
  Go version:       go1.12.17
  Git commit:       7141c199a2
  Built:            Wed Mar  4 01:21:08 2020
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
```
- 因为众所周知的网络原因，我们需要为docker添加仓库镜像，分别复制以下命令到终端并按回车执行：
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
- 至此，docker的安装和配置完成，为了保险，你还可以尝试拉取一个镜像测试以下速度，复制以下命令到终端并按回车执行：
```
docker pull ubuntu
```
如果很快（5s-20s)下载完成（～60MB），则说明镜像配置成功，docker的安装和配置过程完成。

#### 2、阿里云镜像仓库注册和设置固定密码和登陆
完成了docker的安装和配置后，我们进行阿里云镜像仓库的注册和设置固定密码步骤。

打包好的实验容器存储在阿里云镜像仓库中，因此你先开通阿里云镜像仓库服务，具体为：

- 登陆阿里云官网，在最上方的搜索框输入 `容器镜像服务`进行搜索，选择立即开通进入容器镜像服务
{{< figure src="/blockchain101/images/post/2019-2020-tools-docker/tools-docker-search.png"  alt="" width="100%"  >}}

- 进入容器镜像服务页面后，选择菜单中的访问凭证，以获取凭证
{{< figure src="/blockchain101/images/post/2019-2020-tools-docker/tools-docker-mainpage.png"  alt="" width="100%"  >}}

- 点击设置固定密码，设置一个docker镜像仓库的登陆密码

- 设置完成固定密码后，按照访问凭证页面登陆实例中的提示，在终端中复制其提示的命令并回车：
> 注意1:$号无需复制！
>
> 注意2: 每个人账号不同，请复制你的访问凭证页面所给出的账号！
{{< figure src="/blockchain101/images/post/2019-2020-tools-docker/tools-docker-cmdlogin.png"  alt="" width="100%"  >}}

- 设置完成后，为了测试是否设置正确，下载我们课程的`hello_blockchain`镜像以测试,在终端中复制其提示的命令并回车:
```
docker run --rm registry.cn-shenzhen.aliyuncs.com/blockchain101/hello_blockchain
```
若成功，则在终端会显示`blockchain 101`的字符画并退出。

---
<a rel="license" href="http://creativecommons.org/licenses/by-nc-sa/4.0/"><img alt="知识共享许可协议" style="border-width:0" src="https://i.creativecommons.org/l/by-nc-sa/4.0/88x31.png" /></a><br />本作品采用<a rel="license" href="http://creativecommons.org/licenses/by-nc-sa/4.0/">知识共享署名-非商业性使用-相同方式共享 4.0 国际许可协议</a>进行许可。
