###########################################
# @program: blockchain101
# @auther: TaibiaoGuo
# @github: https://github.com/taibiaoGuo/blockchain101
# @create: 2020/03/10 23:18 GMT+8
###########################################

# 构建proxyclient镜像
FROM golang:1.13.6 AS buildproxyclient
WORKDIR /root/proxyclient
COPY . .
RUN go build -tags netgo proxyclient.go \
    && mkdir  /root/copy\
    && cp  proxyclient /root/copy \
    && cp  bin/client.zip /root/copy

# 构建frps镜像
FROM alpine:3.10 AS buildfrps
ENV FRP_VERSION 0.31.2
RUN cd /root \
    &&  wget --no-check-certificate -c https://github.com/fatedier/frp/releases/download/v${FRP_VERSION}/frp_${FRP_VERSION}_linux_amd64.tar.gz \
    &&  tar zxvf frp_${FRP_VERSION}_linux_amd64.tar.gz  \
    &&  cd frp_${FRP_VERSION}_linux_amd64/ \
     && mkdir  /root/copy\
    &&  cp  frps /root/copy \
    &&  cp  frps.ini /root/copy

# 合并为最终镜像
FROM alpine:3.10 as prod
WORKDIR /usr/local/blockchain101
COPY --from=buildproxyclient /root/copy/proxyclient  /usr/local/blockchain101/
COPY --from=buildproxyclient /root/copy/client.zip  /usr/local/blockchain101/
COPY --from=buildfrps /root/copy/frps /usr/local/blockchain101/
COPY --from=buildfrps /root/copy/frps.ini /usr/local/blockchain101/
COPY entrypoint.sh /usr/local/blockchain101/
EXPOSE 7000 7001 7002
RUN apk add --no-cache bash

HEALTHCHECK --interval=10s --timeout=3s --retries=5 \
  CMD curl -fs http://127.0.0.1:7001 || exit 1

ENTRYPOINT "/usr/local/blockchain101/entrypoint.sh"

