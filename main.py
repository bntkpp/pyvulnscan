import time
from rich.console import Console
from rich.table import Table
from scanner.ports import scan_ports, COMMON_PORTS
from scanner.services import scan_services
from scanner.cve import find_cves
from scanner.report import save_json, save_html

console = Console()

SEVERITY_ORDER = {"LOW": 1, "MEDIUM": 2, "HIGH": 3, "CRITICAL": 4}
SEVERITY_COLOR = {"CRITICAL": "red", "HIGH": "yellow", "MEDIUM": "cyan", "LOW": "green"}

def passes(cve, min_severity):
    return SEVERITY_ORDER.get(cve["severity"], 0) >= SEVERITY_ORDER.get(min_severity, 0)

def run_scan(target, ports, min_severity="MEDIUM"):
    console.print("[bold blue][*][/] Escaneando puertos...")
    try:
        open_ports = scan_ports(target, ports)
    except Exception as e:
        console.print(f"[bold red][!][/] Error al escanear puertos: {e}")
        return []

    if not open_ports:
        console.print("[bold yellow][!][/] No se encontraron puertos abiertos.")
        return []

    console.print(f"[bold green][+][/] Puertos abiertos: {open_ports}")

    console.print("[bold blue][*][/] Detectando servicios...")
    try:
        services = scan_services(target, open_ports)
    except Exception as e:
        console.print(f"[bold red][!][/] Error al detectar servicios: {e}")
        return []

    results = []
    for port, info in services.items():
        keyword = f"{info['product']} {info['version']}".strip()
        if not keyword:
            continue

        console.print(f"[bold blue][*][/] Buscando CVEs para: [italic]{keyword}[/]")
        try:
            cves = [c for c in find_cves(keyword) if passes(c, min_severity)]
        except Exception as e:
            console.print(f"[bold red][!][/] Error al consultar CVEs para puerto {port}: {e}")
            cves = []

        results.append({"port": port, "service": info, "cves": cves})
        time.sleep(1)

    return results

def print_results(data):
    for r in data:
        svc = r["service"]
        console.rule(f"[bold]Puerto {r['port']}[/] — {svc['product']} {svc['version']}")

        if not r["cves"]:
            console.print("  [green]Sin vulnerabilidades detectadas[/]\n")
            continue

        table = Table(show_header=True, header_style="bold white", box=None, padding=(0, 2))
        table.add_column("CVE", style="cyan", no_wrap=True)
        table.add_column("Severidad", no_wrap=True)
        table.add_column("Score", no_wrap=True)
        table.add_column("Descripción")

        for c in r["cves"]:
            color = SEVERITY_COLOR.get(c["severity"], "white")
            table.add_row(
                c["id"],
                f"[{color}]{c['severity']}[/]",
                f"[{color}]{c['score']}[/]",
                (c["desc"] or "")[:120] + "...",
            )

        console.print(table)
        console.print()

def main():
    console.print("[bold white]=== Scanner de Vulnerabilidades ===[/]\n")
    try:
        target = console.input("[bold]Ingresa la IP o dominio a escanear:[/] ").strip()
    except (KeyboardInterrupt, EOFError):
        console.print("\n[dim]Saliendo.[/]")
        return

    if not target:
        console.print("[bold red][!][/] No ingresaste ningún objetivo. Saliendo.")
        return

    console.print(f"\n[dim]Escaneando {target}... (esto puede tardar)[/]\n")
    data = run_scan(target, COMMON_PORTS, min_severity="MEDIUM")

    if not data:
        console.print("[bold red][!][/] No se obtuvieron resultados.")
        return

    print_results(data)

    try:
        save_json(data, target)
        save_html(data, target)
        console.print("[bold green][+][/] Listo. Revisa [underline]reporte.json[/] y [underline]reporte.html[/]")
    except Exception as e:
        console.print(f"[bold red][!][/] Error al guardar los reportes: {e}")

if __name__ == "__main__":
    main()
