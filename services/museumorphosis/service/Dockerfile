# FROM golang:1.20

# RUN useradd -u 31337 -ms /bin/bash ctf
# RUN useradd -u 31338 -ms /bin/bash chall

# RUN chmod 755 /home/chall

# #RUN apk add --no-cache gcc musl-dev # for sqlite3 build
# #RUN apt-get install gcc musl-dev -y

# WORKDIR /home/chall/service/ro
# RUN mkdir ./jwt_secret && touch ./jwt_secret/secret
# RUN mkdir /database

# COPY ./ro/go.mod ./ro/go.sum ./
# RUN go mod download
# RUN go install github.com/codegangsta/gin@latest
# #USER chall
