from dataclasses import dataclass
from typing import Optional

"""
This is the python packet class that the C packet is parsed into, this is the actual packet class
that is used to view packets, and detect for intrusions throughout the whole system. At the root of it, 
the C packet is just for capturing purposes.
"""

@dataclass
class PyPacket:
    dst_mac: Optional[str]     # Primarily for logging purposes 
    src_mac: Optional[str]     # Used to check arp spoofing
    protocol: Optional[str]
    type: Optional[int]        # If applicable, will track ICMP request vs. reply
    src_ip: Optional[str]      # Used in synergy with dst_port to track traffic frequency
    dst_ip: Optional[str]      # Used to detect an ICMP sweep
    src_port: Optional[int]    
    dst_port: Optional[int]    # Used in synergy with src_ip to track traffic frequency
    flags: Optional[str]       # Used to detect different types of TCP scans (ie. SYN, XMAS, NULL, etc.)
    query: Optional[bytes]     # Used to detect DNS tunneling via string entropy
    query_len: Optional[int]
    timestamp: float           # For logging or tracking traffic frequency
     
    def __str__(self): # For printing packets to the terminal when using CLI version of the program
        parts = []

        # Protocol header
        parts.append(f"[{self.protocol}]")

        # IP layer with optional MACs
        if self.src_ip and self.dst_ip:
            src = self.src_ip
            dst = self.dst_ip
            if self.src_mac:
                src += f" - {self.src_mac}"
            if self.dst_mac:
                dst += f" - {self.dst_mac}"
            parts.append(f"{src} → {dst}")

        # Ports (for TCP/UDP)
        if self.src_port is not None and self.dst_port is not None:
            parts.append(f"{self.src_port} → {self.dst_port}")

        # TCP flags
        if self.flags:
            parts.append(f"{self.flags}")

        # ICMP type
        if self.protocol == "ICMP" and self.type is not None:
            parts.append(f"Type={self.type}")

        # [TCP] | 18.164.96.38 - 2c:21:31:4e:6b:78 → 129.21.102.104 - d4:f3:2d:96:4e:e3 | 443 → 8608 | PSH ACK
        return " | ".join(parts)