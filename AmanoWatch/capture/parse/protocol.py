from capture.config.config import protocol_nums, tcp_service_ports, udp_service_ports

def parse_protocol(protocol_num, src_port, dst_port):
    protocol = protocol_nums[protocol_num]
    if protocol == "TCP":
        protocol = tcp_service_ports.get(dst_port, tcp_service_ports.get(src_port, "TCP"))
    elif protocol == "UDP":
        protocol = udp_service_ports.get(dst_port, udp_service_ports.get(src_port, "UDP"))
    elif protocol == "ARP":
        return protocol
    elif protocol == "ICMPV6":
        return protocol
    else:
        protocol = protocol_nums.get(protocol, "UNKNOWN")
        
    return protocol