+++
title = "Docker安装指南"
date = 2020-03-17T01:00:00Z
description = "Docker安装指南"
categories = ["Docker"]
type = "post"
+++

本指南用于在阿里云服务器上安装Docker

> 判断是否成功安装docker的方法，在SSH中输入下面的命令
> 并按`回车`或`return`执行命令，如果出现`blockchain 101`的字符画（手机显示可能会错位），则表示docker安装成功。若未成功，则根据你使用的设备，按照 `一、PC端安装步骤总览` 或 `二、手机端安装步骤总览` 中任意一个来完成docker的安装。

```
docker run --rm registry.cn-shenzhen.aliyuncs.com/blockchain101 hello_blockchain
```

### 一、PC端安装步骤总览
> 手机端和网页端访问的是同一台服务器，两种安装方式只需要按照流程执行一种即可。

#### 1、安装前检查清单

 已经兑换了阿里云服务器

#### 2、重装阿里云服务器操作系统

> 为了避免不必要的错误，因此这里直接让大家重装阿里云的操作系统

**2.1 登陆阿里云官网**

访问阿里云官方网站 https://www.aliyun.com/ 并登陆阿里云官网

{{< figure src="/blockchain101/images/post/2019-2020-tools-install-docker/2-1-1.png"  alt="" width="100%"  >}}

{{< figure src="/blockchain101/images/post/2019-2020-tools-install-docker/2-1-2.png"  alt="" width="100%"  >}}

**2.2 进入阿里云控制面板** 

点击`控制台`进入控制台页面

{{< figure src="/blockchain101/images/post/2019-2020-tools-install-docker/2-2-1.png"  alt="" width="100%"  >}}

在控制台页面的`已开通的云产品`中找到`云服务器ECS`，点击进入云服务器页面

{{< figure src="/blockchain101/images/post/2019-2020-tools-install-docker/2-2-2.png"  alt="" width="100%"  >}}

在云服务器页面中找到`实例ID`列表,点击你的实例的ID进入云服务器的实例详情页

{{< figure src="/blockchain101/images/post/2019-2020-tools-install-docker/2-2-3.png"  alt="" width="100%"  >}}

**2.3 停止实例**
在实例详情页面中找到`停止`按钮，点击

{{< figure src="/blockchain101/images/post/2019-2020-tools-install-docker/2-3-1.png"  alt="" width="100%"  >}}

在弹出的选择框中分别选择`强制停止`、`确定要强制停止`、`确定`

{{< figure src="/blockchain101/images/post/2019-2020-tools-install-docker/2-3-2.png"  alt="" width="100%"  >}}

等待实例停止

**2.4 更换操作系统**

实例停止后，找到实例详情页面中的`配置信息`，点击，在下拉列表中点击`更换操作系统`

{{< figure src="/blockchain101/images/post/2019-2020-tools-install-docker/2-4-1.png"  alt="" width="100%"  >}}

在弹框中选择 `确定，更换操作系统`

{{< figure src="/blockchain101/images/post/2019-2020-tools-install-docker/2-4-2.png"  alt="" width="100%"  >}}

在新的页面中在`公共镜像`下拉菜单中选择`Ubuntu`和`18.04 64位`

在`安全设置`中选择`自定义密码`

在`登陆密码`设置一个服务器密码

点击`确认`

在弹出框中获取`手机验证码`、输入得到的手机验证码、`确认`

{{< figure src="/blockchain101/images/post/2019-2020-tools-install-docker/2-4-3.png"  alt="" width="100%"  >}}

在弹出的框中选择`返回实例列表`并等待服务器启动完成

{{< figure src="/blockchain101/images/post/2019-2020-tools-install-docker/2-4-5.png"  alt="" width="100%"  >}}

#### 3、通过网页版SSH连接服务器

在服务器自动启动完成后，在`实例列表`中选择你的服务器的`远程连接`

**3.1 远程连接服务器**

{{< figure src="/blockchain101/images/post/2019-2020-tools-install-docker/3-1-1.png"  alt="" width="100%"  >}}

确定`连接协议`是`SSH`

在`用户名`处输入`root`

在`密码`处输入你在步骤`2.4`设置的密码

点击 `确定`

{{< figure src="/blockchain101/images/post/2019-2020-tools-install-docker/3-1-2.png"  alt="" width="100%"  >}}

#### 4、执行安装docker命令

**4.1 执行安装docker命令**

粘贴下面的命令到SSH中，按回车键执行
> 网页版中可以使用组合键 `ctrl`+`v`进行粘贴

```
curl -sSL https://get.daocloud.io/docker -o d.sh && chmod +x d.sh && ./d.sh --mirror Aliyun && rm d.sh
```

{{< figure src="/blockchain101/images/post/2019-2020-tools-install-docker/4-1-1.png"  alt="" width="100%"  >}}

**4.2 等待命令执行完毕**

命令执行时间大约为2-5分钟，当出现如图所示的标志时表示命令执行结束了
> 如果命令长时间不结束，则可能是你的安装命令输入错误了，按组合键`ctrl`+`c`终止命令的执行

{{< figure src="/blockchain101/images/post/2019-2020-tools-install-docker/4-1-2.png"  alt="" width="100%"  >}}

#### 5、检查Docker是否安装成功

**5.1 执行测试命令**

粘贴下面的命令到SSH中，按回车键执行
> 网页版中可以使用组合键 `ctrl`+`v`进行粘贴

```
docker run --rm registry.cn-shenzhen.aliyuncs.com/blockchain101/hello_blockchain
```

{{< figure src="/blockchain101/images/post/2019-2020-tools-install-docker/4-2-1.png"  alt="" width="100%"  >}}

**5.2 通过运行结果判断是否成功**

运行成功时，会出现blockchain 101 的字符画，否则表示安装失败

若安装失败，关闭所有网页，重新打开，从步骤`1.1`重新走整个流程

若多次安装失败，请联系老师。

{{< figure src="/blockchain101/images/post/2019-2020-tools-install-docker/4-2-2.png"  alt="" width="100%"  >}}

#### 6、关闭网页
`5.2`成功后，即可关闭网页离开。

> docker安装完成后无需在每次访问服务器时执行 `4.1 docker安装`，只需要安装一次，除非docker损坏（可通过`5.1`进行判断）。
>
> 手机端和网页端访问的是同一台服务器，两种安装方式只需要按照流程执行一种即可。


### 二、手机端安装步骤总览
> 手机端和网页端访问的是同一台服务器，两种安装方式只需要按照流程执行一种即可。

#### 1、安装前检查清单

 - 已经兑换了阿里云服务器
 - 手机下载了阿里云APP
 - 手机下载了支付宝APP
 - 使用手机自带的浏览器打开本页面（不要使用QQ内置浏览器等打开本页面，因为QQ屏蔽了支付宝）

 #### 2、访问阿里云官网和登陆

 **2.1 访问阿里云官网**
 粘贴下面的网址到手机浏览器地址栏访问阿里云ECS服务器控制台，进行阿里云的登陆界面

 ```
 https://ecs.console.aliyun.com/#/home
 ```

{{< figure src="/blockchain101/images/post/2019-2020-tools-install-docker/IMG_3723.png"  alt="" width="100%"  >}}

{{< figure src="/blockchain101/images/post/2019-2020-tools-install-docker/IMG_3724.png"  alt="" width="100%"  >}}

 **2.2 使用支付宝登陆阿里云**

在支付宝中`确认登陆`后，支付宝会跳转到`云服务器管理控制台`

{{< figure src="/blockchain101/images/post/2019-2020-tools-install-docker/IMG_3725.png"  alt="" width="100%"  >}}

 #### 3、重装阿里云服务器操作系统

  在支付宝跳转的`云服务器管理控制台`中执行`一、PC端安装步骤总览`的步骤`2.3 停止实例` 和 `2.4 更换操作系统`

  执行完后就可以关闭支付宝了

 #### 4、访问服务器

 **4.1 打开阿里云APP**

 打开阿里云APP，切换到`产品控制台`

 {{< figure src="/blockchain101/images/post/2019-2020-tools-install-docker/IMG_3726.png"  alt="" width="100%"  >}}

 {{< figure src="/blockchain101/images/post/2019-2020-tools-install-docker/IMG_3727.png"  alt="" width="100%"  >}}

 **4.2 删除之前的SSH连接**
将之前的SSH配置删除，如果没有请直接跳到步骤`4.3`

{{< figure src="/blockchain101/images/post/2019-2020-tools-install-docker/IMG_3734.png"  alt="" width="100%"  >}}

{{< figure src="/blockchain101/images/post/2019-2020-tools-install-docker/IMG_3735.png"  alt="" width="100%"  >}}

{{< figure src="/blockchain101/images/post/2019-2020-tools-install-docker/IMG_3736.png"  alt="" width="100%"  >}}

**4.3 打开SSH工具**
依次点击右上方`+`、`从我的ECS中选择`

{{< figure src="/blockchain101/images/post/2019-2020-tools-install-docker/IMG_3728.png"  alt="" width="100%"  >}}

点击列表以弹出下拉框

{{< figure src="/blockchain101/images/post/2019-2020-tools-install-docker/IMG_3729.png"  alt="" width="100%"  >}}

根据你主机所在的地域在地域列表里寻找一下主机（比如截图中在深圳）

{{< figure src="/blockchain101/images/post/2019-2020-tools-install-docker/IMG_3730.png"  alt="" width="100%"  >}}

找到后，`选中主机`并点击`确定`

{{< figure src="/blockchain101/images/post/2019-2020-tools-install-docker/IMG_3731.png"  alt="" width="100%"  >}}

**4.4 添加主机并连接**

在`登陆名`处输入`root`,在`密码`处输入之前步骤设置的密码，点击`确认连接`

{{< figure src="/blockchain101/images/post/2019-2020-tools-install-docker/IMG_3732.png"  alt="" width="100%"  >}}

{{< figure src="/blockchain101/images/post/2019-2020-tools-install-docker/IMG_3733.png"  alt="" width="100%"  >}}

 #### 5、执行安装命令

 **5.1 执行安装命令**

连上服务器后，复制下面的命令，`粘贴`到SSH中，按`换行`键或`return`键执行

```
curl -sSL https://get.daocloud.io/docker -o d.sh && chmod +x d.sh && ./d.sh --mirror Aliyun && rm d.sh
```

{{< figure src="/blockchain101/images/post/2019-2020-tools-install-docker/IMG_3737.png"  alt="" width="100%"  >}}

执行完成后，重新出现类似`root@sdhkshdfksh:~#`的输出，表示可以继续执行下一行命令


{{< figure src="/blockchain101/images/post/2019-2020-tools-install-docker/IMG_3738.png"  alt="" width="100%"  >}}

**5.2 等待命令执行完毕**

命令执行时间大约为2-5分钟，当出现如图所示的标志时表示命令执行结束了

> 如果命令长时间（5分钟以上）不结束，则可能是你的安装命令输入错误了，按组合键`ctrl`+`c`终止命令的执行（先按`ctrl`,然后按`c`即可）

 #### 6、执行测试命令

 **6.1 执行命令**
复制下面的命令，`粘贴`到SSH中，按`换行`键或`return`键执行，时间大概5-10s

```
docker run --rm registry.cn-shenzhen.aliyuncs.com/blockchain101/hello_blockchain
```

**6.2 执行成功的截图**
如果执行成功，显示blockchain101（手机端因为屏幕过窄因此可能显示得很乱）

{{< figure src="/blockchain101/images/post/2019-2020-tools-install-docker/IMG_3739.png"  alt="" width="100%"  >}}

{{< figure src="/blockchain101/images/post/2019-2020-tools-install-docker/IMG_3740.png"  alt="" width="100%"  >}}


 #### 7、退出阿里云APP

 成功后，直接退出阿里云APP即可。


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
