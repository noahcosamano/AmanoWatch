import subprocess

def block_ip(ip):
    print(f"Blocking IP: {ip}")
    
    result = subprocess.run(
        [
            "netsh",
            "advfirewall",
            "firewall",
            "add",
            "rule",
            f"name=Block_{ip}",
            "dir=in",
            "action=block",
            f"remoteip={ip}"
        ],
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        print("Failed:", result.stderr)
    else:
        print("Success")