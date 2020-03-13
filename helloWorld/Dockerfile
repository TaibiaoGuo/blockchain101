FROM golang:1.13.6 AS build
WORKDIR /root
COPY helloworld.go .
RUN go build helloworld.go
FROM alpine:latest AS prod
COPY --from=build /root/helloworld /root/helloworld
CMD /root/helloworld