#!/bin/bash
echo "real_ip_header CF-Connecting-IP;" > "/etc/nginx/conf.d/real_ip.conf"
for ip in $(curl -s https://www.cloudflare.com/ips-v4)
do
        echo "set_real_ip_from $ip;" >> "/etc/nginx/conf.d/real_ip.conf"
done
for ipv6 in $(curl -s https://www.cloudflare.com/ips-v6)
do
        echo "set_real_ip_from $ipv6;" >> "/etc/nginx/conf.d/real_ip.conf"
done