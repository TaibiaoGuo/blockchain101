FROM node:9

RUN npm install -g cnpm --registry=https://registry.npm.taobao.org
RUN git clone https://github.com/cubedro/eth-netstats --depth 1

WORKDIR /eth-netstats

RUN cnpm install
RUN cnpm install -g grunt-cli
RUN grunt

EXPOSE 3000

CMD ["npm", "start"]
