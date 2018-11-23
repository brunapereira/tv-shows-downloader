FROM resin/raspberrypi3-debian

RUN apt-get update
RUN DEBIAN_FRONTEND=noninteractive apt-get install wget aria2 \
make build-essential libssl-dev zlib1g-dev libbz2-dev \
libreadline-dev libsqlite3-dev wget curl llvm libncurses5-dev libncursesw5-dev \
xz-utils tk-dev libffi-dev liblzma-dev

RUN wget https://www.python.org/ftp/python/3.7.1/Python-3.7.1.tgz
RUN tar xvf Python-3.7.1.tgz && cd Python-3.7.1/ && \
./configure --enable-optimizations && make -j8 && \
make altinstall

WORKDIR /app

ADD . $WORKDIR

RUN pip3 install -r requirements.txt
