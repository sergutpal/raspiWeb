#!/bin/bash

ufw disable
ufw --force reset
ufw default allow outgoing
ufw allow from 192.168.1.15 port 1:65535 proto tcp
ufw allow from 192.168.1.15 port 1:65535 proto udp
ufw allow from 192.168.1.17 port 1:65535 proto tcp
ufw allow from 192.168.1.17 port 1:65535 proto udp
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
ufw allow from 192.168.1.43 port 1:65535 proto tcp
ufw allow from 192.168.1.43 port 1:65535 proto udp
ufw allow from 192.168.1.44 port 1:65535 proto tcp
ufw allow from 192.168.1.44 port 1:65535 proto udp
ufw allow from 192.168.1.45 port 1:65535 proto tcp
ufw allow from 192.168.1.45 port 1:65535 proto udp
ufw allow from 192.168.1.46 port 1:65535 proto tcp
ufw allow from 192.168.1.46 port 1:65535 proto udp
ufw allow from 192.168.1.47 port 1:65535 proto tcp
ufw allow from 192.168.1.47 port 1:65535 proto udp
ufw allow from 192.168.1.50 port 1:65535 proto tcp
ufw allow from 192.168.1.50 port 1:65535 proto udp
ufw allow from 192.168.1.51 port 1:65535 proto tcp
ufw allow from 192.168.1.51 port 1:65535 proto udp
ufw allow from 192.168.1.216 port 1:65535 proto tcp
ufw allow from 192.168.1.216 port 1:65535 proto udp
ufw allow from 192.168.1.217 port 1:65535 proto tcp
ufw allow from 192.168.1.217 port 1:65535 proto udp
ufw allow from 192.168.1.218 port 1:65535 proto tcp
ufw allow from 192.168.1.218 port 1:65535 proto udp
ufw allow from 192.168.1.219 port 1:65535 proto tcp
ufw allow from 192.168.1.219 port 1:65535 proto udp

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
ufw allow from 157.97.65.88 port 1:65535 proto tcp
ufw allow from 157.97.65.88 port 1:65535 proto udp
ufw allow from 188.87.153.100 port 1:65535 proto tcp
ufw allow from 188.87.153.100 port 1:65535 proto udp

# IPs Alexa Amazon
ufw allow from 54.171.139.177 port 80:443 proto tcp


# ufw allow 49001/tcp  # Openvpn
# ufw allow 49003/tcp  # SSH



ufw default deny incoming
ufw --force enable
ufw logging off
#ufw status numbered
