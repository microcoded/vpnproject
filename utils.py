import fcntl
import os
import socket
import struct

# VPN Configuration
TUN_INTERFACE = "/dev/net/tun"
UDP_PORT = 9400
BUFFER_SIZE = 2048

def setup_tun(ip_address):
    tun = os.open("/dev/net/tun", os.O_RDWR)
    tunsetiff = 0x400454CA
    iff_tun = 0x0001 | 0x1000
    ifr = struct.pack("16sH", b"tun0", iff_tun)
    fcntl.ioctl(tun, tunsetiff, ifr)
    os.system(f"ip addr add {ip_address}/24 dev tun0")
    os.system("ip link set dev tun0 up")
    return tun


def create_udp_socket(bind_ip=None):
    """Create a UDP socket"""
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    if bind_ip:
        sock.bind((bind_ip, UDP_PORT))
    return sock

def send_packet(sock, data, target_ip):
    sock.sendto(data, (target_ip, UDP_PORT))

def receive_packet(sock):
    return sock.recvfrom(BUFFER_SIZE)
