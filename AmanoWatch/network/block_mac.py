import time
import subprocess

blocked_macs = {}

def block_mac(mac, timeout=300):
    now = time.time()
    mac = mac.upper()
    
    if mac in blocked_macs and blocked_macs[mac] > now:
        print(f"{mac} already blocked")
        return
    
    rule_name = f"Block_MAC_{mac}"
    
    # Add MAC filter using netsh
    result = subprocess.run(
        [
            "netsh", "wlan", "add", "filter",
            "permission=deny",
            f"mac={mac}",
            f"name={rule_name}"
        ],
        capture_output=True,
        text=True
    )
    
    if result.returncode != 0:
        print("Failed:", result.stderr)
        return
    
    print(f"Blocked MAC {mac} for {timeout} seconds")
    blocked_macs[mac] = now + timeout

def unblock_mac():
    """
    Unblocks MACs whose timeout has expired.
    """
    now = time.time()
    for mac in list(blocked_macs.keys()):
        if blocked_macs[mac] <= now:
            rule_name = f"Block_MAC_{mac}"
            
            subprocess.run(
                [
                    "netsh", "wlan", "delete", "filter",
                    f"mac={mac}",
                    "permission=deny"
                ],
                capture_output=True,
                text=True
            )
            
            print(f"Unblocked MAC {mac}")
            del blocked_macs[mac]