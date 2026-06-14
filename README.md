# Vulnerability Scanner

Herramienta de línea de comandos que escanea puertos abiertos en un objetivo, detecta los servicios que corren en ellos y busca CVEs conocidos en la base de datos NVD (NIST).

## Requisitos

- Python 3.10+
- Nmap instalado en el sistema ([nmap.org](https://nmap.org/download.html))
- API key de NVD (gratuita en [nvd.nist.gov/developers/request-an-api-key](https://nvd.nist.gov/developers/request-an-api-key))

## Instalación

```bash
git clone <repo>
cd vuln-scanner
python -m venv venv
venv\Scripts\activate        # Windows
pip install -r requirements.txt
```

Crear el archivo `.env` en la raíz del proyecto:

```
NVD_API_KEY=tu_api_key_aqui
```

## Uso

```bash
python main.py
```

```
=== Scanner de Vulnerabilidades ===
Ingresa la IP o dominio a escanear: scanme.nmap.org

[*] Escaneando puertos...
[+] Puertos abiertos: [22, 80]
[*] Detectando servicios...
[*] Buscando CVEs para: OpenSSH 6.6.1p1
...
[+] Listo. Revisa reporte.json y reporte.html
```

## Estructura

```
vuln-scanner/
├── main.py              # Punto de entrada
├── requirements.txt
├── .env                 # API key (no subir al repo)
├── scanner/
│   ├── ports.py         # Escaneo TCP de puertos
│   ├── services.py      # Detección de servicios con nmap -sV
│   ├── cve.py           # Consulta a la API de NVD
│   └── report.py        # Generación de reporte JSON y HTML
└── templates/
    └── report.html      # Template Jinja2 del reporte
```

## Salida

Al finalizar el escaneo se generan dos archivos:

| Archivo | Descripción |
|---|---|
| `reporte.json` | Datos crudos del escaneo en formato JSON |
| `reporte.html` | Reporte visual con tabla de CVEs por puerto |

## Dependencias

| Librería | Uso |
|---|---|
| `python-nmap` | Detección de servicios vía nmap |
| `requests` | Consultas a la API de NVD |
| `jinja2` | Renderizado del reporte HTML |
| `python-dotenv` | Carga de variables de entorno |
| `rich` | Colores y formato en la terminal |
