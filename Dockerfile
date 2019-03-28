FROM node:10.15.3-alpine

ENV NODE_VERSION 10.15.3

RUN apk add bash bind-tools python g++ make --no-cache

ADD package-lock.json .
ADD package.json .
ADD generateprivatekey.js .

RUN npm install

