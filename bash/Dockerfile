#FROM bash:4.4
#RUN apk update
#RUN apk add ffmpeg
#RUN apk add sox
#RUN apk add rubberband-cli

FROM ubuntu:20.04
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get -y install \
    build-essential wget rubberband-cli sox ffmpeg

WORKDIR /home
COPY app .

#COPY script.sh /
#CMD ["bash", "/script.sh"]
