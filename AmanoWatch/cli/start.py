from queue import Queue
from utils.welcome import welcome
from utils.ui_helpers import error, clear
from cli.output import view_port, view_proto
from cli.parse import parse_command
import threading

# CLI loop
def start_cli(packet_queue: Queue, system_stop_event):
    # system_stop_event is the stop event used to exit the entire program
    # Create new stop event for breaking packet stream on keyboard input
    stop_event = threading.Event()
    
    try:
        while not system_stop_event.is_set():
            welcome()
            cmd = input("NIDS> ")

            if cmd.lower() == "exit":
                stop_event.set()
                break

            try:
                parsed = parse_command(cmd)
            except ValueError as e:
                error(str(e))
                continue

            # Stop command listener if an error happens on input to reprompt
            if stop_event:
                stop_event.set()

            # Create new stop event for next input break
            stop_event = threading.Event()

            target = parsed["target"]
            wait_ms = parsed["wait_ms"]

            # If a string is passed, it must be protocol filtered and this will execute
            if isinstance(target, str):
                clear()
                print(f"\nListening for {target} packets (delay={wait_ms}ms)...")
                view_proto(packet_queue, target, stop_event, wait_ms)
            else:
                # Otherwise it must be port filtered and this will execute
                clear()
                print(f"\nListening on port {target} (delay={wait_ms}ms)...")
                view_port(packet_queue, target, stop_event, wait_ms)
                
    # IMPORTANT: This error occurs when all threads stop, this is to catch it and end runtime.
    except EOFError:
        return