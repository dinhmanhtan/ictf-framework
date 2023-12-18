#!/bin/bash

service mysql start
service nginx start
service prometheus-node-exporter start

# TO FIX, REGISTER AS SERVICE PLZ.
/usr/share/logstash/bin/logstash -f /etc/logstash/conf.d/syslog.conf  &


ICTF_DATABASE_SETTINGS=/opt/ictf/settings/database-api.py  /usr/bin/uwsgi -c uwsgi.ini
#ICTF_DATABASE_SETTINGS=/opt/ictf/settings/database-api.py python3 wsgi.py

#python3 ictf-db-export-s3.py
