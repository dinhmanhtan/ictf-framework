FROM ubuntu:20.04

RUN apt-get update
RUN DEBIAN_FRONTEND=noninteractive apt-get -y --no-install-recommends -o Dpkg::Options::="--force-confdef" -o Dpkg::Options::="--force-confold" upgrade && \
    apt-get update -y && \
    apt-get -y install software-properties-common && \
    apt-add-repository ppa:ansible/ansible && \
    apt-get -y update && apt-get -y install ansible

RUN useradd -m --uid 31337 ctf
RUN apt-get -y install zip tmux screen vim emacs nano curl wget python2.7 python3 python3-pip ruby perl gcc binutils build-essential tcpdump docker.io ansible socat openvpn net-tools iputils-ping openssh-server
RUN apt-get -y install libboost-dev libboost-thread-dev libboost-log-dev libboost-program-options-dev libpq-dev clang 
