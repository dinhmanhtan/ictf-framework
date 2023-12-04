#!/bin/bash

gunicorn \
    --bind 0.0.0.0:3131 \
    --workers 1 \
    --worker-connections 1024 \
    --reload \
    main:app
