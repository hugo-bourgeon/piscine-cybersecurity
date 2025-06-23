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
    && rm -rf /var/lib/apt/lists/*

WORKDIR /home

COPY inquisitor.py /home/inquisitor.py

CMD ["/bin/bash"]
