from cli.verify import verify_target

def parse_wait(parts):
    # Get "wait" argument, this is so terminal does not get clogged with many packets
    wait_ms = 0

    for part in parts:
        if part.startswith("-wait="):
            # Usual format is "-wait=100"
            value = part.split("=", 1)[1]

            if not value.isdigit():
                raise ValueError("wait must be an integer")

            wait_ms = int(value)
        else:
            # Any argument other than "wait" is invalid
            raise ValueError("unknown argument provided")

    return wait_ms


# Command helper
def parse_command(cmd: str):
    parts = cmd.strip().split()

    if not parts:
        raise ValueError("empty command")

    command = parts[0].lower()

    # I intend on adding other commands in the future, although I am not sure what
    if command != "view":
        raise ValueError(f"'{command}' is not a valid command")

    if len(parts) < 2:
        # If "view" comes alone
        raise ValueError("'view' requires a protocol or port")

    # ie. "tcp", "53", "arp"
    target = verify_target(parts[1])
    wait_ms = parse_wait(parts[2:])

    return {
        "command": "view",
        "target": target,
        "wait_ms": wait_ms,
    }