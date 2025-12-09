#!/usr/bin/env python3
import socket
import threading
from queue import Queue
from datetime import datetime

# ——————— SETTINGS ———————
target = input("\nEnter target IP or hostname (e.g. scanme.nmap.org): ").strip()
threads = 200          # Speed
timeout = 1.0
start_port = 1
end_port = 5000        # Number of ports to scan

# ——————— Common ports database ———————
common_ports = {
    21: "FTP",    22: "SSH",     23: "Telnet",  25: "SMTP",    53: "DNS",
    80: "HTTP",   110: "POP3",   143: "IMAP",   443: "HTTPS",  993: "IMAPS",
    995: "POP3S", 1723: "PPTP",  3389: "RDP",   3306: "MySQL", 5432: "PostgreSQL",
    5900: "VNC",  8080: "HTTP-Proxy", 8443: "HTTPS-alt", 25565: "Minecraft"
}

print_lock = threading.Lock()
open_ports = []

def grab_banner(ip, port):
    try:
        s = socket.socket()
        s.settimeout(2)
        s.connect((ip, port))
        banner = s.recv(1024).decode('utf-8', errors='ignore').strip()
        s.close()
        if banner:
            return banner.replace('\n', ' ').replace('\r', '')[:120]
    except:
        pass

    # Special handling for HTTP/HTTPS
    if port in [80, 443, 8080, 8443]:
        try:
            import ssl
            s = socket.socket()
            if port in [443, 8443]:
                ctx = ssl.create_default_context()
                s = ctx.wrap_socket(s, server_hostname=ip)
            s.settimeout(3)
            s.connect((ip, port))
            s.send(b"GET / HTTP/1.0\r\n\r\n")
            resp = s.recv(2048).decode('utf-8', errors='ignore')
            s.close()
            first_line = resp.split('\n')[0]
            server = ''
            for line in resp.split('\n'):
                if line.lower().startswith('server:'):
                    server = line.split(':', 1)[1].strip()
                    break
            title = resp.split('<title>')[1].split('</title>')[0] if '<title>' in resp else ''
            result = first_line.strip()
            if server:
                result += f" | Server: {server}"
            if title:
                result += f" | Title: {title[:50]}"
            return result
        except:
            pass
    return None

def scan_port(port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        result = sock.connect_ex((target, port))
        if result == 0:
            service_name = common_ports.get(port, "Unknown")
            banner = grab_banner(target, port)

            with print_lock:
                open_ports.append(port)
                print(f"[+] {port:<6} OPEN → {service_name.ljust(15)}", end="")
                if banner:
                    print(f" | {banner}")
                else:
                    print()
        sock.close()
    except:
        pass

# ——————— Start scanning ———————
print(f"\nScanning {target} | ports {start_port}-{end_port} | threads: {threads}")
print(f"Started: {datetime.now().strftime('%H:%M:%S')}")
print("-" * 80)

q = Queue()
for port in range(start_port, end_port + 1):
    q.put(port)

def worker():
    while True:
        try:
            port = q.get_nowait()
        except:
            break
        scan_port(port)
        q.task_done()

# Launch threads
for _ in range(threads):
    t = threading.Thread(target=worker, daemon=True)
    t.start()

q.join()

# ——————— Results ———————
print("-" * 80)
if open_ports:
    print(f"Open ports on {target}: {sorted(open_ports)}")
    print(f"Total open ports found: {len(open_ports)}")
else:
    print("No open ports found in the specified range.")
print(f"Scan finished: {datetime.now().strftime('%H:%M:%S')}")