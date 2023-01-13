#!/usr/bin/env bash
gunicorn --bind 0.0.0.0:8000 cookiecutter.wsgi --reload --workers="$WORKER_COUNT" --timeout="$WORKER_TIMEOUT"