#!/bin/bash

#chown -R chall /var/data
#chmod +x *.sh
./create_secret_key.sh
./init_db.sh
#exec runuser -u chall "$@"

./run.sh
