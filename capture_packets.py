import pyshark
from queue import Queue
from packet import Packet
import time

packet_queue = Queue()
packet_list = []

import asyncio
import pyshark

def capture(interface: str):
    print("capturing packets")

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    capture = pyshark.LiveCapture(interface=interface)

    for pkt in capture.sniff_continuously():
        packet_queue.put(pkt)
        
def parse_packet(packet) -> Packet:
    dst_mac = src_mac = None
    dst_ip = src_ip = None
    dst_port = src_port = None
    flags = protocol = None

    try:
        dst_mac = packet.eth.dst
        src_mac = packet.eth.src
    except:
        pass

    try:
        if hasattr(packet, 'ip'):  # IPv4
            src_ip = packet.ip.src
            dst_ip = packet.ip.dst
            protocol = packet.transport_layer

        elif hasattr(packet, 'ipv6'):  # IPv6
            src_ip = packet.ipv6.src
            dst_ip = packet.ipv6.dst
            protocol = packet.transport_layer

    except:
        pass

    try:
        if packet.transport_layer == 'TCP':
            src_port = int(packet.tcp.srcport)
            dst_port = int(packet.tcp.dstport)

            flag_list = []
            if packet.tcp.flags_syn == '1': flag_list.append("SYN")
            if packet.tcp.flags_ack == '1': flag_list.append("ACK")
            if packet.tcp.flags_fin == '1': flag_list.append("FIN")
            if packet.tcp.flags_reset == '1': flag_list.append("RST")
            if packet.tcp.flags_push == '1': flag_list.append("PSH")
            if packet.tcp.flags_urg == '1': flag_list.append("URG")

            flags = ",".join(flag_list) if flag_list else None

        elif packet.transport_layer == 'UDP':
            src_port = int(packet.udp.srcport)
            dst_port = int(packet.udp.dstport)

    except:
        pass

    pkt = Packet(
        dst_mac, src_mac, protocol,
        src_ip, dst_ip,
        src_port, dst_port,
        flags
    )
    
    print(pkt)
    
    return pkt

def build_packet_list() -> list[Packet]:
    while True:
        packet = packet_queue.get()

        parsed = parse_packet(packet)
        packet_list.append(parsed)