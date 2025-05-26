CLIENT_PEER = """
# {}
[Peer]
PublicKey = {}
AllowedIPs = {}/32"""

WG_CONF = """[Interface]
PrivateKey = {}
Address = 10.0.0.1/24
ListenPort = {}
PostUp = iptables -A FORWARD -i wg1 -j ACCEPT; iptables -t nat -A POSTROUTING -o {} -j MASQUERADE
PostDown = iptables -D FORWARD -i wg1 -j ACCEPT; iptables -t nat -D POSTROUTING -o {} -j MASQUERADE

{}
"""

CLIENT_CONF = """[Interface]
PrivateKey = {}
Address = {}/24
DNS = 8.8.8.8

[Peer]
PublicKey = {}
Endpoint = {}:{}
AllowedIPs = 0.0.0.0/0
"""
