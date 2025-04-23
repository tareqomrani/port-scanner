import socket
from concurrent.futures import ThreadPoolExecutor

common_ports = {
    21: 'FTP',
    22: 'SSH',
    23: 'Telnet',
    25: 'SMTP',
    53: 'DNS',
    80: 'HTTP',
    110: 'POP3',
    143: 'IMAP',
    443: 'HTTPS',
    3389: 'RDP'
}

def scan_port(host, port):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(1)
            result = s.connect_ex((host, port))
            if result == 0:
                service = common_ports.get(port, 'Unknown')
                print(f"Port {port} is open ({service})")
    except Exception:
        pass

def scan_ports(host, ports):
    print(f"Scanning host: {host}")
    with ThreadPoolExecutor(max_workers=50) as executor:
        for port in ports:
            executor.submit(scan_port, host, port)

if __name__ == "__main__":
    target = input("Enter IP address or hostname to scan: ")
    port_range = range(1, 1025)
    scan_ports(target, port_range)