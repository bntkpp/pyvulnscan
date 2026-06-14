import socket

def check_ports(ip, ports, timeout=1):
    open_ports = []
    for port in ports: 
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Crear un socket TCP
        sock.settimeout(timeout) 
        try:
            sock.connect((ip, port)) # Intentar conectar al puerto
            open_ports.append(port) # Si la conexión es exitosa, el puerto está abierto
        except:
            pass
        finally:
            sock.close()
    return open_ports

COMMON_PORTS = [21, 22, 23, 25, 53, 80, 110, 139, 143, 443, 445, 3306, 3389, 8080]

scan_ports = check_ports