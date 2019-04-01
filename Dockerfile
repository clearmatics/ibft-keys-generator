FROM node:10.15.3-alpine

ENV NODE_VERSION 10.15.3

RUN apk add --no-cache \
    bash \
    bind-tools \
    g++ \
    make \
    python \
    python-dev \
    py-pip \
    build-base \
  && pip install virtualenv

WORKDIR /generateprivatekey
ADD package-lock.json .
ADD package.json .
ADD generateprivatekey.js .

RUN npm install

WORKDIR /env/cm_writer
ADD ./cm_writer/requirements.txt .
RUN virtualenv ./ && source ./bin/activate && pip install -r ./requirements.txt
COPY ./cm_writer /cm_writer

ADD entrypoint.sh /

WORKDIR /
ENTRYPOINT ["./entrypoint.sh"]
CMD []
