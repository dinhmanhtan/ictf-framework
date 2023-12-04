FROM teamvmbase:latest

COPY ./game_config.json /root/game_config.json
COPY ./teamvms/provisioning /root/provisioning
COPY ./teamvms/bundled_services /opt/ictf/services
COPY ./common/hephaestus_provisioning/teamhosts /root/teamhosts
COPY ./teamvms/start.sh /root/start.sh

ARG services

# RUN ansible-playbook /root/provisioning/hephaestus_provisioning/ansible/ansible-provisioning.yml --extra-vars="$services" && chmod +x /root/start.sh
RUN echo "localhost ansible_connection=local" > /etc/ansible/hosts && \
    ansible-playbook /root/provisioning/hephaestus_provisioning/ansible/ansible-provisioning.yml \
        --extra-vars="$services" \
        --extra-vars="BASE=1" \
        --extra-vars="PRIMER=1" \
        --extra-vars="LOCAL=False" \
        --extra-vars="GAME_CONFIG_PATH=/root/game_config.json" \
        && \
    chmod +x /root/start.sh 
