#!/usr/bin/env bash

set -o errexit
set -o pipefail
set -o nounset
set -o xtrace

JUPYTER_CONFIG_DIR="." cd notebooks && python ../manage.py shell_plus --notebook
