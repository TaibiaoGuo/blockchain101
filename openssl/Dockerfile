FROM alpine:latest
RUN apk add openssl bash
COPY [".bashrc", "./root/"]
COPY ["motd", "/etc/motd"]

COPY . /app
WORKDIR /app
RUN rm motd .bashrc Dockerfile Makefile
CMD /root/helloworld