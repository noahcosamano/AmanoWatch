from dataclasses import dataclass
from typing import Optional

@dataclass
class Packet:
    dst_mac: Optional[str]
    src_mac: Optional[str]
    protocol: Optional[str]
    src_ip: Optional[str]
    dst_ip: Optional[str]
    src_port: Optional[int]
    dst_port: Optional[int]
    flags: Optional[str]