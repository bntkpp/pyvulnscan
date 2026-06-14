import nmap 

def scan_services(ip, ports):
    nm = nmap.PortScanner() 
    nm.scan(ip, arguments='-sV -p ' + ','.join(map(str, ports))) # Escanea los puertos especificados con detección de servicios
    services = {}
    for host in nm.all_hosts():
        for port in ports:
            if nm[host].has_tcp(port) and nm[host]['tcp'][port]['state'] == 'open': # Verifica si el puerto está abierto
                info = nm[host]['tcp'][port] # Obtiene la información del servicio
                services[port] = {
                    'name':     info['name'],
                    'product':  info['product'],
                    'version':  info['version']
                }
    return services
