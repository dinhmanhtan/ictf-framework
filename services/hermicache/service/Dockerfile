FROM julia:1.8.5-alpine3.17

RUN adduser --disabled-password -u 31337 -s /bin/sh ctf
RUN adduser --disabled-password -u 31338 -s /bin/sh chall

RUN chmod 755 /home/chall


#COPY ./ro/install.jl /tmp/
#RUN julia /tmp/install.jl

USER chall
WORKDIR /home/chall/service/ro


ENTRYPOINT ["/usr/local/julia/bin/julia", "Server.jl"]
