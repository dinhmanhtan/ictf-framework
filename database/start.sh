
#!/bin/bash

service mysql start
service nginx stop
service prometheus-node-exporter start

# TO FIX, REGISTER AS SERVICE PLZ.
#/usr/share/logstash/bin/logstash -f /etc/logstash/conf.d/syslog.conf  &


ICTF_DATABASE_SETTINGS=/opt/ictf/settings/database-api.py  /usr/bin/uwsgi -c uwsgi.ini
#python3 wsgi.py

#/opt/ictf/venv/database/bin/python ictf-db-export-s3.py
