#!/usr/bin/env python3

import fcntl, struct, os
from scapy.all import *
from shared.create_tun import create_tun
from shared.crypto.encrypt import split_into_blocks_encrypt, load_public_key
from shared.crypto.decrypt import split_into_blocks_decrypt, load_private_key

# Logging setup
logging.basicConfig(
    filename='/volumes/server.log',
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s'
)
logger = logging.getLogger(__name__)

# Create the tun interface
TUNSETIFF = 0x400454ca
IFF_TUN   = 0x0001
IFF_TAP   = 0x0002
IFF_NO_PI = 0x1000
TUN_IP = "192.168.53.98"
ip = "8.8.8.8"

# Create the tun interface
ifname, tun = create_tun(TUNSETIFF, IFF_TUN, IFF_NO_PI)

# Set up the tun interface
os.system("ip addr add {}/24 dev {}".format(TUN_IP, ifname))
os.system("ip link set dev {} up".format(ifname))

IP_A = "10.9.0.11"
PORT = 9090

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((IP_A, PORT))

# Set default ip to avoid error
ip = "10.0.0.1"

# Get RSA keys
server_private_key = load_private_key("/keys/server_private.pem")
client_public_key = load_public_key("/keys/client_public.pem")

while True:
    # this will block until at least one interface is ready
    ready, _, _ = select.select([sock, tun], [], [])
    for fd in ready:
        if fd is sock:
            try:
                data, (ip, port) = sock.recvfrom(2048)
                decrypted_data = split_into_blocks_decrypt(data, server_private_key) # RSA
                pkt = IP(decrypted_data)
                logger.info("From socket <==: {} --> {}".format(pkt.src, pkt.dst))
                os.write(tun, decrypted_data)
            except Exception as e:
                logging.exception(f"Error decrypting from sock: {e}")

        if fd is tun:
            try:
                packet = os.read(tun, 2048)
                pkt = IP(packet)
                logger.info("From tun ==>: {} --> {}".format(pkt.src, pkt.dst))
                encrypted_data = split_into_blocks_encrypt(packet, client_public_key)
                sock.sendto(encrypted_data, (ip, port))
            except Exception as e:
                logging.exception(f"Error encrypting from tun: {e}")
