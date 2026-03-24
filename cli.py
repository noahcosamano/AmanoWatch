from queue import Queue
import threading
from view_packets import view_proto
from log import add_to_log
import os

VALID_PROTOCOLS = {"TCP", "UDP", "ICMP", "IGMP", "ALL"}

def welcome():
    print("\n=== NIDS CLI ===")
    print("Commands:")
    print("  view [protocol] -wait=[seconds]")
    print("    example: view tcp -wait=1")
    print("    'all' prints all protocols")
    print("  exit\n")
    
def parse_command(cmd: str):
    parts = cmd.strip().split()

    if len(parts) < 2:
        return None, None

    if parts[0].lower() != "view":
        return None, None

    protocol = parts[1].upper()

    wait_ms = 0

    for part in parts[2:]:
        if part.startswith("-wait="):
            try:
                wait_ms = int(part.split("=")[1])
            except ValueError:
                return None, None

    return protocol, wait_ms


def start_cli(packet_queue: Queue):
    stop_event = None

    while True:
        welcome()
        cmd = input("NIDS> ")
        add_to_log(f"{cmd}\n", "command_log.txt")

        if cmd.lower() == "exit":
            print("Exiting CLI...")
            if stop_event:
                stop_event.set()
            break

        protocol, wait_ms = parse_command(cmd)

        if protocol not in VALID_PROTOCOLS:
            os.system("cls")
            print("Invalid command or protocol.")
            continue

        if stop_event:
            stop_event.set()

        stop_event = threading.Event()

        print(f"\nListening for {protocol} packets (delay={wait_ms} seconds)...")

        view_proto(packet_queue, protocol, stop_event, wait_ms)