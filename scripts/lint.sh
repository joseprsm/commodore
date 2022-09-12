#!/usr/bin/env bash

set -e
set -x

flake8 commodore tests
black commodore tests --check
isort commodore tests scripts --check-only