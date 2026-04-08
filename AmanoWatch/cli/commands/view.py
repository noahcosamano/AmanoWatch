from capture.config.config import tcp_service_ports, udp_service_ports
from capture.classes.PyPacket import PyPacket
from utils.ui_helpers import clear
from queue import Empty
import msvcrt
import time


# When the queue is this deep, drain+discard to catch up instead of printing
DRAIN_THRESHOLD = 2000

# Warn at most once per second
WARN_INTERVAL = 1.0

def execute(packet_queue, target, wait_ms, stop_event):
    clear()
    if isinstance(target, str):
        print(f"\nListening for {target} packets (delay={wait_ms}ms)...")
        matcher = _proto_matcher(target)
    else:
        print(f"\nListening on port {target} (delay={wait_ms}ms)...")
        matcher = _port_matcher(target)

    _view_loop(packet_queue, matcher, stop_event, wait_ms)


# ── Matchers ─────────────────────────────────────────────────────────────────
def _proto_matcher(proto):
    selected = proto.upper()
    udp_names = set(udp_service_ports.values())
    tcp_names = set(tcp_service_ports.values())

    def _match(pkt):
        if selected == "ALL":
            return True
        p = pkt.protocol
        if p == selected:
            return True
        if selected == "UDP" and p in udp_names:
            return True
        if selected == "TCP" and p in tcp_names:
            return True
        return False

    return _match


def _port_matcher(port):
    def _match(pkt):
        return pkt.src_port == port or pkt.dst_port == port
    return _match


# ── Main loop ────────────────────────────────────────────────────────────────
def _view_loop(packet_queue, matches, stop_event, wait_ms):
    wait_seconds = wait_ms / 1000

    # Flush stdin
    while msvcrt.kbhit():
        msvcrt.getch()

    print("\nPress ANY key to stop...\n")

    last_warn = 0.0
    dropped_since_warn = 0

    while not stop_event.is_set():
        if msvcrt.kbhit():
            msvcrt.getch()
            stop_event.set()
            clear()
            break

        qsize = packet_queue.qsize()

        # If we're falling behind, drain aggressively and drop what we can't print
        if qsize > DRAIN_THRESHOLD:
            discarded = 0
            while packet_queue.qsize() > DRAIN_THRESHOLD // 2:
                try:
                    packet_queue.get_nowait()
                    discarded += 1
                except Empty:
                    break
            dropped_since_warn += discarded

            now = time.time()
            if now - last_warn >= WARN_INTERVAL:
                print(f"--- BACKLOG: dropped {dropped_since_warn} packets to catch up "
                      f"(queue was {qsize}) ---")
                last_warn = now
                dropped_since_warn = 0
            continue

        try:
            packet = packet_queue.get(timeout=0.1)
        except Empty:
            continue

        if matches(packet):
            print(packet)
            if wait_seconds > 0:
                time.sleep(wait_seconds)