FROM ubuntu:18.04

RUN apt-get update && apt-get install -y xinetd

RUN useradd -u 31337 -ms /bin/bash ctf
RUN useradd -u 31338 -ms /bin/bash chall

RUN chmod 755 /home/chall


COPY ./ro/xinetd.conf /etc/xinetd.d/backup
RUN chmod 644 /etc/xinetd.d/backup

WORKDIR /home/chall/service

USER chall

CMD ["/usr/sbin/xinetd", "-dontfork"]
