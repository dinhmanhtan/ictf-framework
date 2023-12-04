#!/bin/bash

chown -R chall /var/data
./create_secret_key.sh
./init_db.sh
exec runuser -u chall "$@"