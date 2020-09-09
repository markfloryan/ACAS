#!/usr/bin/env sh
set -eu

envsubst '${DOMAIN}' < /etc/nginx/conf.d/app.conf.template > /etc/nginx/conf.d/app.conf

exec "$@"