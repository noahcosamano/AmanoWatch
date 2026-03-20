from packet import Packet
from block import block_ip
from gateway import get_gateway
import time

def detect_scan(packet_queue, stop_event, interval=10, quantity=20):
    gateway = get_gateway()
    activity = {}

    while not stop_event.is_set():
        packet: Packet = packet_queue.get()
 
        now = time.time()
        src_ip = packet.src_ip
        dst_port = packet.dst_port
        flags = packet.flags
        
        print(flags)

        if not src_ip or not dst_port:
            packet_queue.task_done()
            continue

        if src_ip not in activity:
            activity[src_ip] = []

        activity[src_ip].append((now, dst_port, flags))

        cutoff = now - interval
        activity[src_ip] = [
            (t, p, f) for (t, p, f) in activity[src_ip]
            if t >= cutoff
        ]

        unique_ports = {p for (_, p, f) in activity[src_ip]}
        
        syn_count = sum(
            1 for (_, _, f) in activity[src_ip]
            if f and "SYN" in f
        )
        
        rst_count = sum(
            1 for (_, _, f) in activity[src_ip]
            if f and "RST" in f
        )
        
        total_packets = len(activity[src_ip])
        
        print(f"Activity: {activity}")
        print(f"Total Packets: {total_packets} | Unique Ports: {unique_ports}")
        print(f"SYN count: {syn_count} | RST count: {rst_count}")

        if gateway is not None and packet.src_ip == gateway:
            packet_queue.task_done()
            continue
        
        elif packet.src_ip is not None and packet.src_ip.startswith("127."):
            packet_queue.task_done()
            continue
        
        elif len(unique_ports) >= quantity and total_packets > 0:
            syn_ratio = syn_count / total_packets
            rst_ratio = rst_count / total_packets
            
            print(f"SYN Ratio: {syn_ratio} | RST Ratio: {rst_ratio}")

            if syn_ratio > 0.5 and rst_ratio > 0.3:
                print("\n🚨 PORT SCAN DETECTED 🚨")
                print(f"Source IP: {src_ip}")
                print(f"{len(unique_ports)}+ ports hit in {interval} seconds")

                block = input(f"Would you like to block {src_ip}? ('Y' or 'N'): ").lower().strip()
                if block == "y":
                    block_ip(src_ip)
                
                stop_event.set()

        packet_queue.task_done()