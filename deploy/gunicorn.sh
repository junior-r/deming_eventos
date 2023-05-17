#!/bin/bash

NAME="deming_events"
DJANGODIR=$(dirname $(cd `dirname $0` && pwd))
SOCKFILE=/tmp/gunicorn-deming-events.sock
LOGDIR=${DJANGODIR}/logs/gunicorn.log
USER=junior
GROUP=junior
NUM_WORKERS=5
DJANGO_WSGI_MODULE=eventos_deming.wsgi

rm -frv $SOCKFILE

echo $DJANGODIR

cd $DJANGODIR
GUNICORN_DIR=/home/junior/.local/bin/gunicorn
exec ${GUNICORN_DIR} ${DJANGO_WSGI_MODULE}:application \
  --name $NAME \
  --workers $NUM_WORKERS \
  --user=$USER --group=$GROUP \
  --bind=unix:$SOCKFILE \
  --log-level=debug \
  --log-file=$LOGDIR
