from capture_packets import capture, build_packet_list
import threading

def main():
    capture_thread = threading.Thread(target=capture, args=("Wi-Fi",), daemon=True)
    worker_thread = threading.Thread(target=build_packet_list, daemon=True)

    capture_thread.start()
    worker_thread.start()

    capture_thread.join()
    worker_thread.join()
    
main()