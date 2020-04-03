#!/bin/bash
# author:taibiaoguo
# github: github.com/taibiaoguo/blockchain101

# Setting variables
ip=""
localvar=""

getipFunc(){
arr[0]="ipecho.net/plain"
arr[1]="ifconfig.me"
arr[2]="www.pubyun.com/dyndns/getip"
arr[3]="members.3322.org/dyndns/getip"

for v in ${arr[@]}
do
        if [ "$ip" == "$localvar" ];then
          ip=$(curl -s --connect-timeout 2 $v)
        fi
done
}

# Getting your Public IP 
echo "-------------获取公网IP-------------"
getipFunc
echo "-------------IP获取成功------------"


echo "-------------启动ipfs中-------------"
docker rm -f ipfs >/dev/null 2>&1
sleep 5s
docker run -d --rm --name ipfs -p 4001:4001 -p 8080:8080 -p 5001:5001 registry.cn-shenzhen.aliyuncs.com/blockchain101/ipfs >/dev/null 2>&1
sleep 10s
echo "-------------启动ipfs成功-------------"


echo "-------------设置IPFS中-----------"
docker exec -it ipfs /bin/sh -c "ipfs config --json API.HTTPHeaders.Access-Control-Allow-Origin '[\"http://${ip}:5001\", \"http://127.0.0.1:5001\", \"https://webui.ipfs.io\"]'"

docker exec -it ipfs /bin/sh -c "ipfs config --json API.HTTPHeaders.Access-Control-Allow-Methods '[\"PUT\", \"GET\", \"POST\"]'"
sleep 2s
docker restart ipfs >/dev/null 2>&1
echo "-------------设置IPFS成功-----------"


echo "使用浏览器访问你的IPFS节点: http://${ip}:5001/webui"
echo "本实验的教程请参见: https://taibiaoguo.gitee.io/blockchain101/2019-2020-07-ipfs/"
echo "您可以关闭本窗口了,拜了个拜^o^"
