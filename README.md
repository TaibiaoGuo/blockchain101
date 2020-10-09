# 实验源代码

所有实验使用docker进行打包，可以直接下载打包好的docker镜像进行学习。

## 在自己计算机上构建实验环境
上课使用的所有软件都已经打包成docker镜像，拉取下来后可以直接启动实验环境。不过在这之间你先需要在你的计算机上安装Docker和Chrome。

> 如果你想从源码开始编译，你需要先阅读一下Docker的[教程](https://docs.docker.com/get-started/)。


docker是一个类似虚拟机的软件运行环境，用于运行实验。

chrome是google推出的现代浏览器，使用chrome浏览器可以确保实验环境的显示不会出现错误。


### 常见问题及解决方案
> 本小节介绍了实验中的常见问题及解决方案，可能会出现一些引起不适的专业名词。

1、docker安装失败：
docker支持Linux、MacOS、Windows等主流操作系统，其中Windows上的安装过程步骤比较多。Win10建议使用WSL2（[教程链接](https://docs.docker.com/docker-for-windows/install-windows-home/)）/Hyper-V的方式安装，Win10以下推荐使用Virtualbox/VMware运行Linux虚拟机来安装docker。

2、docker镜像拉取失败：
docker若出现镜像拉取失败往往是因为网络故障，可以选择拉取本实验环境的国内镜像，也可以选择使用代理访问网络。

3、网络故障：
如果按照教程出现故障，首先需要考虑网络故障。网络故障时，请选择使用相应软件的国内镜像源或者使用代理访问网络。一个简单的网络故障判断方法是看是否可以访问google的页面。

