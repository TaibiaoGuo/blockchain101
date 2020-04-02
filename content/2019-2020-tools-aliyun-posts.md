+++
title = "IPFS实验说明"
date = 2020-04-01T01:00:00Z
description = "IPFS实验说明"
categories = ["Aliyun","IPFS"]
type = "post"
+++

本指南用于在开放阿里云服务器的端口，以供其他用户访问。

因为安全策略，大部分端口默认是无法通过服务器的公网IP进行访问的，本实验课需要使用外网端口，因此需要同学们按照下面的设置打开你的外网端口。

访问地址 https://ecs.console.aliyun.com/ 进入阿里云ECS的控制台。在菜单找到`本实例安全组`
{{< figure src="/blockchain101/images/post/2019-2020-tools-aliyun-posts/01.png"  alt="" width="100%"  >}}

点击`本实例安全组`，点击右侧的`配置规则`
{{< figure src="/blockchain101/images/post/2019-2020-tools-aliyun-posts/02.png"  alt="" width="100%"  >}}

点击`本实例安全组`，点击右侧的`配置规则`
{{< figure src="/blockchain101/images/post/2019-2020-tools-aliyun-posts/03.png"  alt="" width="100%"  >}}

在跳转的新页面点击`添加安全组规则`，在弹框内输入以下配置：
{{< figure src="/blockchain101/images/post/2019-2020-tools-aliyun-posts/04.png"  alt="" width="100%"  >}}

文字版本参考：
```
规则方向：入网方向
授权策略：允许
协议类型：自定义TCP
端口范围：1/20000
优先级：1
授权类型：IPV4类型地址访问
授权对象：0.0.0.0/0
```

输入完成后，点击`确认`即完成设置。

---
<a rel="license" href="http://creativecommons.org/licenses/by-nc-sa/4.0/"><img alt="知识共享许可协议" style="border-width:0" src="https://i.creativecommons.org/l/by-nc-sa/4.0/88x31.png" /></a><br />本作品采用<a rel="license" href="http://creativecommons.org/licenses/by-nc-sa/4.0/">知识共享署名-非商业性使用-相同方式共享 4.0 国际许可协议</a>进行许可。
