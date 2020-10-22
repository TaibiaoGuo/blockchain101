## 简介
openssl 实验
##  运行方法

> 首先需要在本机安装docker，可以试试在线docker环境[kdtakoda](https://www.katacoda.com/courses/docker/playground)

docker run --rm -it registry.cn-shenzhen.aliyuncs.com/blockchain101/openssl:latest

# 本地构建

您可以在本地构建本程序。

## 本地快速编译构建-Linux环境

```shell script
make
```

## 本地手动构建-Windows\Linux环境

Windows环境构建镜像需要先安装docker，然后：

编译本程序
```shell script
docker build -t openssl:latest .
```
运行本程序
```shell script
docker run --rm -it \
 openssl:latest
```

## 实验内容
### 1、哈希函数的性质

#### 1.1、哈希函数的确定性

相同的哈希函数算法对于相同的输入一定会得到相同的输出。

输出一定是 cd5b1e4947e304476c788cd474fb579a
```shell script
echo -n "bitcoin" | openssl md5
```

输出一定是 78b448038b9a59601f3d579c8d431526
```shell script
echo -n "bitcoins" | openssl md5
```

#### 1.2、哈希函数的雪崩性
若输入有一点点不同，输出也完全不同，类似雪崩，一点微小的改变会导致雪山崩塌。

输出是 cd5b1e4947e304476c788cd474fb579a
```shell script
echo -n "bitcoin" | openssl md5
```

添加一个s，输出为 78b448038b9a59601f3d579c8d431526

与bitcoin相比，输入完全不同
```shell script
echo -n "bitcoins" | openssl md5
```

### 2、数字签名
步骤如下：
* 准备证书

* 对`README.md`产生的数字摘要使用 sha256 进行签名；输出文件`README.sha256`

* 验证`README.sha256`的数字签名

* 稍稍修改`README.md`再一次验证数字签名

#### 2.1、证书的生成
通过openssl生成RSA公私钥证书。

生成rsa私钥 myrsaCA.pem。

需要手动输入私钥的访问密码两遍。
```shell script

openssl genrsa -des3 -out myrsaCA.pem 1024
```

利用rsa私钥 myrsaCA.pem 生成rsa公钥 myrsapubkey.pem

需要手动输入私钥的访问密码
```shell script
openssl rsa -in myrsaCA.pem -pubout -out myrsapubkey.pem
```

#### 2.2、查看README.md和信息的签名

查看README.md
```shell script
cat README.md
```

注释： 利用rsa私钥 myrsaCA.pem 对文件 README.md 进行签名。

生成签名信息 README.sha256。

需要手动输入私钥的访问密码。

```shell script
openssl dgst -sha256 -out README.sha256 -sign myrsaCA.pem README.md
```

#### 2.3、信息的验证
注释： 利用rsa公钥 myrsapubkey.pem和签名信息 README.sha256 验证

如果输出为 Verified OK ，则表示验证成功，
文件README.md未被从篡改且文件README.md由私钥拥有者签名

需要手动输入私钥的访问密码
```shell script
openssl dgst -sha256 -signature README.sha256 -verify myrsapubkey.pem README.md
```

#### 2.4、修改README.md并验证
在README.md 后面添加一行

<你的名字>修改为你的真实姓名

```shell script
echo "你的名字" >> RDADME.md
```

注释： 利用rsa公钥 myrsapubkey.pem和签名信息 README.sha256 验证

如果输出为 Verified OK ，则表示验证成功，
文件README.md未被从篡改且文件README.md由私钥拥有者签名

需要手动输入私钥的访问密码
```shell script
openssl dgst -sha256 -signature README.sha256 -verify myrsapubkey.pem README.md
```

此时，输出不为 Verified Ok。