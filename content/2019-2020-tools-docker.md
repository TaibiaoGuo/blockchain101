+++
title = "Docker使用帮助"
date = 2020-03-12T01:00:00Z
description = "Docker使用帮助"
categories = ["Docker"]
type = "post"
+++

在本课程的实验课程代码和工具都使用docker进行了打包，以方便学习和复现。

#### 名词解释
本文中出现的你可能不理解的名词的简单说明

| 名词 | 解释 |
| --- | --- |
| docker | 为我们课堂提供可重复实验的统一环境的一个软件 |
| 容器 | 类似于虚拟机的虚拟化技术 |
| 镜像 | 打包好的容器 |
| 镜像仓库 | 存放制作好的镜像的服务 |
| 仓库镜像 | 镜像仓库的镜像可以加速镜像的下载速度 |

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

### docker按照方法

请访问 [Docker安装指南]({{< ref "content/2019-2020-tools-install-docker.md" >}})。
---
<a rel="license" href="http://creativecommons.org/licenses/by-nc-sa/4.0/"><img alt="知识共享许可协议" style="border-width:0" src="https://i.creativecommons.org/l/by-nc-sa/4.0/88x31.png" /></a><br />本作品采用<a rel="license" href="http://creativecommons.org/licenses/by-nc-sa/4.0/">知识共享署名-非商业性使用-相同方式共享 4.0 国际许可协议</a>进行许可。
