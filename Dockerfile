FROM resin/raspberrypi3-debian

RUN apt-get update
RUN DEBIAN_FRONTEND=noninteractive apt-get install aria2 python3 python3-pip

WORKDIR /app

ADD . $WORKDIR

RUN pip3 install -r requirements.txt
