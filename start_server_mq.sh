#!/usr/bin/env bash

python server_mq.py
celery -A server_mq.celery worker  -l INFO
