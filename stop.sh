#!/bin/sh

NAME="Dpname=ThinkSocks"

for PROCESS in $NAME
do
	pid=`/bin/ps -edf | grep "$PROCESS" | grep -v grep | awk '{print $2}'`
	if [ "$pid" != "" ] ; then
		echo -e "\033[32mKilling $pid\033[0m"
		kill -9 $pid

		sleep 5
		echo "\033[32m$pid is killed\033[0m"
        else
		echo -e "\033[31mNo Process Found,Server have not been started.\033[0m"
	fi
done