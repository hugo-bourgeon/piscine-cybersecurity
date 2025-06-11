#!/bin/bash

service tor start

# Wait for hostname file to be created
while [ ! -f /var/lib/tor/hidden_service/hostname ]; do
    sleep 1
done

ONION_ADDR=$(cat /var/lib/tor/hidden_service/hostname)

# replace in index.html
sed -i "s|ONION_ADDRESS|${ONION_ADDR}|" /var/www/html/index.html

service ssh start
nginx -g "daemon off;"