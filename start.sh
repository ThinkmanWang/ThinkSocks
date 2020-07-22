#!/bin/sh

cd /var/services/homes/thinkman/Github-Thinkman/ThinkSocks
export PATH="$PATH:/opt/bin"

pipenv run python main.py -Dpname=ThinkSocks > /dev/null 2>&1 &

