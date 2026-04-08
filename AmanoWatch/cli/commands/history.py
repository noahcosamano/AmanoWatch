from utils.ui_helpers import clear, error
import ipaddress
import re
from datetime import datetime

valid_filters = ("-n", "-ip", "-severity", "-detector", "-since", "-date")
valid_severity = ("info", "warning", "medium", "high", "critical")
valid_detectors = ("arp-spoof", "dns-tunnel", "port-scan", "honeyport")

TIME_MULTIPLIERS = {
    "h": 3600,
    "m": 60,
    "s": 1,
}

def execute(command: str):
    #input("DEBUG: Execute called")
    command = command.lower()
    
    filters = {
        "n": None,
        "ip": None,
        "severity": None,
        "detector": None,
        "since": None,
        "date": None
    }
    
    tokens = parse_command(command)
    #input(f"DEBUG: Command parsed | Length: {len(tokens)}")
    
    if len(tokens) > 1:
        for token in tokens[1:]:
            if not parse_filter(token, filters):
                #input("DEBUG: Command invalid — stopping")
                return
        
    query(filters)
    
def parse_filter(token: str, filters):
    #input("DEBUG: Parsing filter")
    
    parts = token.split("=")
    #input(f"DEBUG: filter: {parts[0]}")
    if parts[0] == "help":
        help()
        return False
    elif parts[0] not in valid_filters:
        clear()
        error(f"'{parts[0]}' is not a valid filter")
        return False
    elif len(parts) == 1:
        clear()
        error(f"'{parts[0]} is missing a value")
        return False
    elif len(parts) > 2:
        clear()
        error(f"'{parts[0]} only takes one argument")
        return False
        
    filter, value = parts[0], parts[1]
    
    #input(f"DEBUG: value: {parts[1]}")
    
    if filter == "-n":
        if parse_number(value) is False:
            clear()
            error("value must be a positive integer. Use 'history help' for more information")
            return False
        filters["n"] = value
    if filter == "-ip":
        if parse_ip(value) is False:
            clear()
            error("invalid ip address. Use 'history help' for more information")
            return False
        filters["ip"] = value
    if filter == "-severity":
        if parse_severity(value) is False:
            clear()
            error("invalid severity value. Use 'history help' for more information")
            return False
        filters["severity"] = value
    if filter == "-detector":
        if parse_detector(value) is False:
            clear()
            error("invalid detector value. Use 'history help' for more information")
            return False
        filters["detector"] = value
    if filter == "-since":
        total_seconds = parse_since(value)
        if total_seconds is None or total_seconds == 0:
            clear()
            error("invalid time value. Use 'history help' for more information")
            return False
        filters["since"] = total_seconds
    if filter == "-date":
        date = parse_date(value)
        if date is None:
            clear()
            error("invalid date value. Use 'history help' for more information")
            return False
        filters["date"] = date
        
    return True
        
def parse_number(number):
    try:
        return int(number) > 0
    except ValueError:
        return False

def parse_ip(ip):
    try:
        ipaddress.ip_address(ip)
        return True
    except ValueError:
        return False
    
def parse_severity(severity):
    return severity in valid_severity

def parse_detector(detector):
    return detector in valid_detectors

def parse_since(time: str):
    pattern = r"(\d+)([hms])"
    matches = re.findall(pattern, time)
    
    if not matches:
        return None
    
    total_seconds = 0
    
    for amount, unit in matches:
        total_seconds += int(amount) * TIME_MULTIPLIERS[unit]

    return total_seconds

def parse_date(date: str):
    try:
        return datetime.strptime(date, "%Y-%m-%d")
    except ValueError:
        return None
    
def parse_command(command: str):
    #input(f"DEBUG: Parsing {command}")
    command = command.split()
    #input(f"DEBUG: Parsed: {command}")
    return command

def help():
    clear()

    print(" " + "═"*85)
    print("  HISTORY COMMAND HELP")
    print(" " + "═"*85)

    print("\n\033[1mUSAGE:\033[0m")
    print("  history [filters]\n")

    print("\033[1mFILTERS:\033[0m")

    print("\n  \033[94m-n=N\033[0m")
    print("  └─ Limit number of results returned.")
    print("     Example: history -n=25")

    print("\n  \033[94m-ip=ADDR\033[0m")
    print("  └─ Filter detections by IPv4 or IPv6 address.")
    print("     Example: history -ip=192.168.1.10")

    print("\n  \033[94m-severity=LEVEL\033[0m")
    print("  └─ Filter by alert severity.")
    print(f"     Valid values: {', '.join(valid_severity)}")
    print("     Example: history -severity=high")

    print("\n  \033[94m-detector=TYPE\033[0m")
    print("  └─ Filter by detection module.")
    print(f"     Valid values: {', '.join(valid_detectors)}")
    print("     Example: history -detector=port-scan")

    print("\n  \033[94m-since=TIME\033[0m")
    print("  └─ Show alerts within a relative time window.")
    print("     Format: <number>[h|m|s]")
    print("     Examples:")
    print("       history -since=1h")
    print("       history -since=30m")
    print("       history -since=10m30s")

    print("\n  \033[94m-date=YYYY-MM-DD\033[0m")
    print("  └─ Show alerts from a specific date.")
    print("     Example: history -date=2026-04-07")

    print("\n\033[1mEXAMPLES:\033[0m")
    print("  history -n=10")
    print("  history -severity=critical")
    print("  history -ip=10.0.0.5 -since=2h")
    print("  history -detector=arp-spoof -date=2026-04-01")

    print("\n" + "─"*87)
    input("\nPress ENTER to return...")
    clear()

# Query database after command has been returned from execute if command is valid
def query(filters):
    input("DEBUG: Valid command")
    ...