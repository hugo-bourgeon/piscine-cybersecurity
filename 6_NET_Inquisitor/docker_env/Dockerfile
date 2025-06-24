FROM debian:bookworm

RUN apt-get update && apt-get install -y \
    iproute2 \
    iputils-ping \
    net-tools \
    tcpdump \
    ethtool \
    iptables \
    curl \
    gcc \
    make \
    vim \
    nano \
    sudo \
    procps \
    valgrind \
    python3 \
    python3-pip \
    python3-netifaces \
    && rm -rf /var/lib/apt/lists/*

RUN pip3 install --break-system-packages scapy

WORKDIR /home

COPY inquisitor.py /home/inquisitor.py
COPY ftp_test.py /home/ftp_test.py

CMD ["/bin/bash"]
