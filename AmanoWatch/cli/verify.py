from capture.config.config import protocol_nums, udp_service_ports, tcp_service_ports

def verify_target(arg: str):
    """Validate protocol or port."""
    arg = arg.upper()

    if arg in protocol_nums.values() or arg == "ALL" or arg in \
    udp_service_ports.values() or arg in tcp_service_ports.values():
        return arg

    if arg.isdigit():
        port = int(arg)
        if 1 <= port <= 65535:
            return port

    # Arg must either be protocol or port, I intend on adding IP filtering and multifiltering
    raise ValueError(f"'{arg}' is not a supported protocol or port")