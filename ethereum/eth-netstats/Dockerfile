FROM node:9

RUN git clone https://github.com/cubedro/eth-netstats --depth 1

WORKDIR /eth-netstats

RUN npm install
RUN npm install -g grunt-cli
RUN grunt

EXPOSE 3000

CMD ["npm", "start"]
