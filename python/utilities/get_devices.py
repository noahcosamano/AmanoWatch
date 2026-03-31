from utilities.load_dll import get_dll_path
from utilities.ui_helpers import error
import ctypes

def get_devices():
    PCAP_ERRBUF_SIZE = 256 # Size of buffer in bytes
    # This is the error buffer passed into GetDevices to capture error messages
    errbuf = ctypes.create_string_buffer(PCAP_ERRBUF_SIZE)

    dll_path = get_dll_path()
    try:
        lib = ctypes.CDLL(dll_path, errbuf)
    except OSError as e:
        error(f"DLL not found at {dll_path}")
        
    lib.GetDevices.argtypes = [ctypes.c_char_p]
    lib.InitCapture.restype = ctypes.c_char_p

    devices = lib.GetDevices(errbuf)

    if not devices:
        error(errbuf)
        return
    
    print(devices)