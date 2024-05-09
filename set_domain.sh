#!/usr/bin/env bash
sed -i "s/DOMAIN.*/DOMAIN=$1/g" ./*/.env
sed -i "s#DATA_PATH.*#DATA_PATH=$2#g" ./*/.env

echo "DOMAIN=$1">loki/.env
echo "DOMAIN=$1">prometheus/.env

echo "DATA_PATH=$2">>loki/.env
echo "DATA_PATH=$2">syslogng/.env
echo "DATA_PATH=$2">>prometheus/.env