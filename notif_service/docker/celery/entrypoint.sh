#!/bin/sh

until cd /app/
do
    echo "Waiting for server volume..."
done

export DJANGO_SETTINGS_MODULE='notif_service.settings'

# run a worker :)
celery -A notif_service worker --loglevel=info --concurrency 1 -E