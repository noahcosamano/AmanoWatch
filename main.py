import threading
import queue
import time
from utilities.capture import capture
from detecting.detect_scan import detect_scan
from detecting.detect_sweep import detect_sweep
from cli.cli import start_cli
                                                                            
loopback = r'\Device\NPF_Loopback'
wifi = "Wi-Fi"

stop_event = threading.Event()
  
def main():
    cli_packet_queue = queue.Queue()
    fast_scan_packet_queue = queue.Queue()
    slow_scan_packet_queue = queue.Queue()
    sweep_packet_queue = queue.Queue()
    
    cli_thread = threading.Thread(
        target=start_cli,
        args=(cli_packet_queue, stop_event),
        name="CLI",
        daemon=True
    )

    capture_thread = threading.Thread(
        target=capture,
        args=(wifi, [cli_packet_queue, fast_scan_packet_queue, slow_scan_packet_queue, sweep_packet_queue], stop_event),
        name="CAPTURE",
        daemon=True
    )

    fast_scan_thread = threading.Thread(
        target=detect_scan,
        args=(fast_scan_packet_queue, 10, 20, 30),
        name="FAST-SCAN",
        daemon=True
    )
    
    slow_scan_thread = threading.Thread(
        target=detect_scan,
        args=(slow_scan_packet_queue, 60, 50, 30),
        name="SLOW-SCAN",
        daemon=True
    )
    
    sweep_thread = threading.Thread(
        target=detect_sweep,
        args=(sweep_packet_queue, 5, 10, 300, stop_event),
        name="SWEEP",
        daemon=True
    )

    cli_thread.start()
    capture_thread.start()
    fast_scan_thread.start()
    slow_scan_thread.start()
    sweep_thread.start()
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Shutting down...")
        stop_event.set()
        
    cli_thread.join()
    capture_thread.join()
    fast_scan_thread.join()
    slow_scan_thread.join()
    sweep_thread.join()

main()