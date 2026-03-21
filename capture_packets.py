import pyshark
import asyncio
from packet import Packet
from queue import Queue

packet_list = []

def capture(interface, output_queue):
    print("Capture Starting")
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    cap = pyshark.LiveCapture(interface=interface)

    try:
        for pkt in cap.sniff_continuously():
            output_queue.put(pkt)

    finally:
        cap.close()
        loop.close()
        
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

            flags_int = int(packet.tcp.flags, 16)

            flag_list = []
            if flags_int & 0x02: flag_list.append("SYN")
            if flags_int & 0x10: flag_list.append("ACK")
            if flags_int & 0x01: flag_list.append("FIN")
            if flags_int & 0x04: flag_list.append("RST")
            if flags_int & 0x08: flag_list.append("PSH")
            if flags_int & 0x20: flag_list.append("URG")
            
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
    
    return pkt

def build_packet_list(input_queue, output_queues: list[Queue]):
    while True:
        raw_packet = input_queue.get()

        try:
            pkt = parse_packet(raw_packet)
            for queue in output_queues:
                queue.put(pkt)
        except Exception as e:
            print(e)

        input_queue.task_done()
        
        