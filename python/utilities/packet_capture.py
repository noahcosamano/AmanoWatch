import ctypes
import os
import sys
from configurations.packet import PyPacket, Packet
from configurations.proto_nums import protocol_nums, service_ports
from utilities.format_fields import format_flags, format_ip, format_mac
from queue import Queue

def get_dll_path():
    # If running as a PyInstaller EXE
    if getattr(sys, 'frozen', False):
        # Look in the folder where the EXE is
        base_path = os.path.dirname(sys.executable)
    else:
        # Look in the project root (dev mode)
        base_path = os.path.dirname(os.path.abspath(__file__))

    return os.path.join(base_path, "packet-capture.dll")

def get_protocol(protocol_num, src_port, dst_port):
    protocol = protocol_nums[protocol_num]
    if protocol == "TCP":
        protocol = service_ports.get(dst_port, service_ports.get(src_port, "TCP"))
    elif protocol == "UDP":
        protocol = service_ports.get(dst_port, service_ports.get(src_port, "UDP"))
    elif protocol == "ARP" or protocol == "DNS":
        return protocol
    else:
        protocol = protocol_nums.get(protocol, "UNKNOWN")
        
    return protocol
    
def convert_to_pypacket(protocol, type, flags, src_mac, dst_mac, src_ip, dst_ip,
                        src_port, dst_port, query, timestamp):
    
    pkt = PyPacket(dst_mac, src_mac, protocol, type, src_ip, dst_ip, 
                   src_port, dst_port, flags, query, timestamp)
    
    return pkt

def capture(device, packet_queues: list[Queue[PyPacket]], stop_event):
    dll_path = get_dll_path()
    try:
        lib = ctypes.CDLL(dll_path)
    except OSError as e:
        print(f"CRITICAL: DLL not found at {dll_path}")
        return

    # 3. Define function signatures for the DLL exports
    lib.InitCapture.argtypes = [ctypes.c_char_p]
    lib.InitCapture.restype = ctypes.c_int
    
    lib.GetNextPacket.argtypes = [ctypes.POINTER(Packet)]
    lib.GetNextPacket.restype = ctypes.c_int
    
    lib.CloseCapture.argtypes = []
    lib.CloseCapture.restype = None

    # 4. Initialize Capture
    if not lib.InitCapture(device):
        print("Failed to initialize capture. Check device path or Admin privileges.")
        return

    CPacket = Packet()

    try:
        while not stop_event.is_set():
            # 5. Pull the next packet from the C DLL
            result = lib.GetNextPacket(ctypes.byref(CPacket))
            
            if result == 1:
                src_ip = format_ip(CPacket.src_ip, CPacket.is_ipv6)
                dst_ip = format_ip(CPacket.dst_ip, CPacket.is_ipv6)
                flags = format_flags(CPacket.tcp_flags)
                src_mac = format_mac(CPacket.src_mac)
                dst_mac = format_mac(CPacket.dst_mac)
                protocol = get_protocol(CPacket.protocol, CPacket.src_port, CPacket.dst_port)
                raw_payload = None
                
                if CPacket.payload_len > 0:
                    raw_payload = ctypes.string_at(CPacket.payload, CPacket.payload_len)
            
                pypacket = convert_to_pypacket(protocol, CPacket.type, flags, src_mac, 
                                               dst_mac,src_ip, dst_ip, CPacket.src_port,
                                               CPacket.dst_port, raw_payload,CPacket.tv_sec)
                
                for q in packet_queues:
                    q.put(pypacket)

            elif result == 0:
                # Timeout - just loop again
                continue
            else:
                print("An error occurred in the capture handle.")
                break

    except KeyboardInterrupt:
        print("\nStopping capture...")
    finally:
        lib.CloseCapture()