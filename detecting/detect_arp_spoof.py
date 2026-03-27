from configurations.packet import Packet

class ArpSpoof:
    def __init__(self, packet_queue, cooldown):
        self.packet_queue = packet_queue
        self.cooldown = cooldown
        self.arp_table = {}
        
    def process_packet(self, packet: Packet):
        now = packet.timestamp
        src_ip = packet.src_ip
        src_mac = packet.src_mac
        
        if not src_ip or not src_mac:
            return
        
        if src_ip not in self.arp_table and src_mac not in self.arp_table:
            self.arp_table[src_mac] = src_ip
            
        
        