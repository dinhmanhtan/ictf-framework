FROM python:3.10.5-slim

RUN useradd -M -s /bin/sh chall


WORKDIR /home/chall

COPY requirements.txt ./
RUN pip install -r requirements.txt

COPY src/ .
COPY scripts/ .

RUN mkdir -p /var/data
RUN chmod +x ./*.sh
RUN chown -R chall:chall /home/chall/

ENTRYPOINT ["./entrypoint.sh"]
CMD [ "./run.sh"]