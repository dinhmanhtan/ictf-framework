#!/bin/bash

cat /root/teamhosts >> /etc/hosts

service openvpn start
service ssh start

tail -f /dev/null
