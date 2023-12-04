#!/bin/bash

#chown -R chall /var/data
./ro/create_secret_key.sh
./ro/init_db.sh
#exec runuser -u chall "$@"
