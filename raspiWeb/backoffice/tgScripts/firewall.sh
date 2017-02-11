#!/bin/bash

ufw disable
ufw --force reset
ufw default allow outgoing
ufw allow from 192.168.1.15 port 1:65535 proto tcp
ufw allow from 192.168.1.15 port 1:65535 proto udp
ufw allow from 192.168.1.20 port 1:65535 proto tcp
ufw allow from 192.168.1.20 port 1:65535 proto udp
ufw allow from 192.168.1.31 port 1:65535 proto tcp
ufw allow from 192.168.1.31 port 1:65535 proto udp
ufw allow from 192.168.1.32 port 1:65535 proto tcp
ufw allow from 192.168.1.32 port 1:65535 proto udp
ufw allow from 192.168.1.33 port 1:65535 proto tcp
ufw allow from 192.168.1.33 port 1:65535 proto udp
ufw allow from 192.168.1.34 port 1:65535 proto tcp
ufw allow from 192.168.1.34 port 1:65535 proto udp
ufw allow from 192.168.1.35 port 1:65535 proto tcp
ufw allow from 192.168.1.35 port 1:65535 proto udp
ufw allow from 192.168.1.40 port 1:65535 proto tcp
ufw allow from 192.168.1.40 port 1:65535 proto udp
ufw allow from 192.168.1.41 port 1:65535 proto tcp
ufw allow from 192.168.1.41 port 1:65535 proto udp
ufw allow from 192.168.1.42 port 1:65535 proto tcp
ufw allow from 192.168.1.42 port 1:65535 proto udp
ufw allow from 10.8.0.9 port 1:65535 proto tcp
ufw allow from 10.8.0.9 port 1:65535 proto udp
ufw allow from 10.8.0.10 port 1:65535 proto tcp
ufw allow from 10.8.0.10 port 1:65535 proto udp
ufw allow from 10.8.0.8 port 1:65535 proto tcp
ufw allow from 10.8.0.8 port 1:65535 proto udp
ufw allow from 10.8.0.12 port 1:65535 proto tcp
ufw allow from 10.8.0.12 port 1:65535 proto udp
ufw allow from 10.8.0.13 port 1:65535 proto tcp
ufw allow from 10.8.0.13 port 1:65535 proto udp
#host=$(</etc/hostname)
#if [ $host = "cubieSrv" ]; then
    ufw allow 49001/tcp  # Openvpn
#    ufw allow 49003/tcp  # SSH
#fi
ufw default deny incoming
ufw enable
#ufw status numbered
