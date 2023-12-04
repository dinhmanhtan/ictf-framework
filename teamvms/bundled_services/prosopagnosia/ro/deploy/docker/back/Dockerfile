FROM ubuntu:20.04

RUN apt update \
    && apt install -y \
        libboost-dev \
        libboost-thread-dev \
        libboost-log-dev \
        libboost-program-options-dev \
        libpq-dev

#RUN useradd --no-create-home --shell /bin/false --uid 1000 --user-group prosopagnosia

RUN useradd -u 31337 -ms /bin/bash ctf
RUN useradd -u 31338 -ms /bin/bash chall

RUN chmod 755 /home/chall
RUN mkdir /var/prosopagnosia && chown chall:chall /var/prosopagnosia

#COPY prosopagnosia /

#RUN chmod +x /prosopagnosia

USER chall

CMD ["/home/chall/service/ro/prosopagnosia", "--address", "0.0.0.0", "--port", "31337"]
