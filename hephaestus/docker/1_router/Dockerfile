FROM ictf_base

RUN DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends iptraf python3 python3-pip python3-dev build-essential awscli iptables-persistent iftop libcurl4-openssl-dev libssl-dev python3-apt zip unzip openvpn python3-setuptools python3-wheel
RUN apt install -y openvpn tcpdump
RUN chmod u+s $(which tcpdump)
COPY ./router /opt/ictf/router
COPY ./ares/docker/vpnkeys/openvpn.zip /etc/openvpn/openvpn.zip

WORKDIR /opt/ictf/router

RUN pip install -r requirements3.txt

RUN ansible-playbook provisioning/hephaestus_provisioning/ansible-provisioning.yml --become 

RUN chmod +x ./start.sh

ENTRYPOINT ./start.sh
