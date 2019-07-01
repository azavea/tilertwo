FROM alpine:3.10
LABEL maintainer="Azavea <systems@azavea.com>"

ENV TIPPECANOE_VERSION="1.34.3"

RUN apk add --no-cache --virtual .build-deps \
    sudo git g++ make sqlite-dev python3-dev zlib-dev && \
  apk add --no-cache libgcc libstdc++ sqlite-libs && \
  apk add --no-cache bash && \
  apk add --no-cache --update python3 && \
  pip3 install --upgrade pip && \
  addgroup sudo && adduser -G sudo -D -H tilertwo && \
  echo '%sudo ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers && \
  cd /root && \
  git clone https://github.com/mapbox/tippecanoe.git tippecanoe && \
  cd tippecanoe && \
  git checkout tags/$TIPPECANOE_VERSION && \
  cd /root/tippecanoe && \
  make && \
  make install && \
  cd /root && \
  rm -rf /root/tippecanoe && \
  apk del .build-deps

RUN pip3 install mbutil awscli

COPY . /usr/local/src

VOLUME /data
VOLUME /home/tilertwo/.aws

USER tilertwo
WORKDIR /data
ENTRYPOINT ["python3", "/usr/local/src/tilertwo.py"]
