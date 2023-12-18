#!/bin/bash

gunicorn \
    --bind 0.0.0.0:3131 \
    --workers 2 \
    --worker-connections 1024 \
    --reload \
    main:app
