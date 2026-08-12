#!/bin/sh
set -e

flask --app wsgi db upgrade

if [ "${SEED_ON_START:-0}" = "1" ]; then
  flask --app wsgi seed
fi

exec "$@"
