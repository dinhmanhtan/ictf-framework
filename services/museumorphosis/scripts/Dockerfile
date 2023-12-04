FROM python:3.8.16-alpine3.18

RUN pip install requests pyjwt
WORKDIR /ictf/

COPY . .
RUN chmod +x ./benign ./getflag ./setflag
ENV PATH="/ictf/:${PATH}"

CMD /bin/sh
