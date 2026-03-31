from scapy.all import conf

for iface in conf.ifaces.values():
    print(f"Name: {iface.name}")
    print(f"Description: {iface.description}")
    print(f"GUID: {iface.guid}")
    print(f"MAC: {iface.mac}")
    print("-" * 20)