# Port Scanner with Banner Grabbing + Threading
import socket
import threading
from datetime import datetime

print("Port Scanner with Banner Grabbing (Threaded)")
target      = input("Enter target IP: ")
start_port  = int(input("Enter starting port: "))
end_port    = int(input("Enter ending port: "))
max_threads = int(input("Enter max threads (recommended 100-500): ") or 200)

print(f"\nScanning target : {target}")
print(f"Scan started at : {datetime.now()}")
print("-" * 50)

open_ports  = []          
print_lock  = threading.Lock()
port_lock   = threading.Lock()
semaphore   = threading.Semaphore(max_threads)


def scan_port(port: int) -> None:
    """Scan a single port, grab its banner if open, and record the result."""
    with semaphore:                         
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(0.3)

            if sock.connect_ex((target, port)) == 0:
                banner = ""
                try:
                    sock.send(b"Hello\r\n")
                    banner = sock.recv(1024).decode(errors="ignore").strip()
                except Exception:
                    pass

                # Thread-safe output + result collection
                with print_lock:
                    print(f"[+] Port {port} is OPEN")
                    if banner:
                        print(f"    Banner: {banner}")
                    else:
                        print("    No banner received")

                with port_lock:
                    open_ports.append(port)

            sock.close()

        except socket.error:
            pass          


# ── Launch one thread per port ────────────────────────────────────────────────
threads: list[threading.Thread] = []

try:
    for port in range(start_port, end_port + 1):
        t = threading.Thread(target=scan_port, args=(port,), daemon=True)
        threads.append(t)
        t.start()

    for t in threads:
        t.join()          

except KeyboardInterrupt:
    print("\nScan stopped by user.")

# ── Summary ───────────────────────────────────────────────────────────────────
print("-" * 50)
if open_ports:
    print(f"Open ports ({len(open_ports)}): {sorted(open_ports)}")
else:
    print("No open ports found.")
print("Scan completed at:", datetime.now())
