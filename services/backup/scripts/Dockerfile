
FROM python:3.8.16-alpine3.18
#RUN apt-get update && apt-get install -y python3 python3-pip
RUN pip3 install nclib

WORKDIR /ictf/

COPY . .

RUN chmod +x ./benign ./getflag ./setflag

ENV PATH="/ictf/:${PATH}"

CMD /bin/bash
