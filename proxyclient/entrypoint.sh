#!/bin/bash
###########################################
# @program: blockchain101
# @auther: TaibiaoGuo
# @github: https://github.com/taibiaoGuo/blockchain101
# @create: 2020/03/10 23:18 GMT+8
###########################################

# ${REDEMPTIONCODE} 需要docker运行时作为环境变量注入容器

# 执行proxyclient
/usr/local/blockchain101/proxyclient -r=${REDEMPTIONCODE}  &
# 添加兑换码
echo token=${REDEMPTIONCODE} >> /usr/local/blockchain101/frps.ini
# 运行frps
/usr/local/blockchain101/frps -c /usr/local/blockchain101/frps.ini
