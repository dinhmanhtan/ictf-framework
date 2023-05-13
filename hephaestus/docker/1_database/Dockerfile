FROM ictf_base

RUN DEBIAN_FRONTEND=noninteractive apt-get install -y nginx uwsgi uwsgi-plugin-python3 mysql-server python3-pip python3-virtualenv python3-mysqldb python3-dev python3-setuptools python3-wheel cron daemon
RUN pip install --upgrade pip

COPY ./database /opt/ictf/database
COPY ./scoring_ictf /opt/ictf/scoring_ictf
RUN mkdir -p /opt/ictf/settings
COPY ./secrets /opt/ictf/secrets

WORKDIR /opt/ictf/database
RUN cp ./settings.py /opt/ictf/settings/database-api.py

RUN chmod +x ./start.sh && ansible-playbook ./provisioning/hephaestus_provisioning/ansible-provisioning.yml

ENTRYPOINT ./start.sh
