import socket
import streamlit as st
from concurrent.futures import ThreadPoolExecutor

st.title("Port Scanner & Service Identifier")
st.write("Scan open ports on a target host and identify common services.")

host = st.text_input("Enter IP address or hostname", "127.0.0.1")
start_port = st.number_input("Start Port", min_value=1, max_value=65535, value=1)
end_port = st.number_input("End Port", min_value=1, max_value=65535, value=1024)

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

results = []

def scan_port(host, port):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(1)
            result = s.connect_ex((host, port))
            if result == 0:
                service = common_ports.get(port, 'Unknown')
                results.append((port, service))
    except Exception:
        pass

if st.button("Scan"):
    with ThreadPoolExecutor(max_workers=50) as executor:
        for port in range(start_port, end_port + 1):
            executor.submit(scan_port, host, port)

    if results:
        st.subheader("Open Ports")
        for port, service in sorted(results):
            st.write(f"Port {port} is open ({service})")
    else:
        st.warning("No open ports found in the selected range.")