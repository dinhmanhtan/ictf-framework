FROM julia:1.8.5-alpine3.17

COPY . /app

WORKDIR /app

ENV ENV=PROD

RUN julia install.jl

ENTRYPOINT ["/usr/local/julia/bin/julia", "Server.jl"]

