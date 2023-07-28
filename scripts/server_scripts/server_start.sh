#!/bin/sh
while getopts :up flag
do
	case "${flag}" in
		u) SERVER_USER=${OPTARG};;
		p) PORT=${OPTARG};;
	esac
done

if [ -z "$SERVER_USER" ];
then
	echo "\$SERVER_USER not defined, defaulting to guinicorn-user"
	export SERVER_USER=gunicorn-user
fi

if [ -z "$PORT" ];
then
	echo "\$PORT not defined, defaulting to 5000"
	export PORT=5000
fi

export PATH=$PATH:/usr/local/bin
gunicorn -b 0.0.0.0:$PORT -u $SERVER_USER --chdir /orodha-user-service/application wsgi:app
