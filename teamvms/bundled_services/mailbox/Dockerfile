FROM python:3.10.5-slim

RUN useradd -u 31337 -ms /bin/bash ctf
RUN useradd -u 31338 -ms /bin/bash chall

RUN chmod 755 /home/chall


COPY requirements.txt /tmp/
RUN pip install -r /tmp/requirements.txt
RUN mkdir -p /var/data
RUN chown -R chall /var/data

USER chall
WORKDIR /home/chall/service/ro


ENTRYPOINT ["./entrypoint.sh"]
#CMD [ "./run.sh"]
