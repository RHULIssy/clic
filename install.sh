#!/bin/sh
set -ex

# This script will create a systemd unit for running CLiC uWSGI, and
# an nginx config.
#
# It is tested on Debian, but should hopefully work on anything systemd-based.
#
# See each part for detail on what happens

. schema/deploy/deploy.sh
. server/deploy/deploy.sh
. client/deploy/deploy.sh
