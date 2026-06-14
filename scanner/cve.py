import requests, os
from dotenv import load_dotenv

load_dotenv()
BASE = "https://services.nvd.nist.gov/rest/json/cves/2.0"
HEADERS = {"apiKey": os.getenv("NVD_API_KEY")}   # la key va en el header

def query_nvd(keyword, max_results=10):
    params = {"keywordSearch": keyword, "resultsPerPage": max_results}
    r = requests.get(BASE, headers=HEADERS, params=params, timeout=30) 
    r.raise_for_status()
    data = r.json() 
    results = []
    for item in data.get("vulnerabilities", []): # Itera sobre las vulnerabilidades obtenidas
        cve = item["cve"]
        metrics = cve.get("metrics", {}) # Obtiene las métricas CVSS disponibles
        cvss = (
            metrics.get("cvssMetricV31", metrics.get("cvssMetricV30", metrics.get("cvssMetricV2", [{}]))) 
        )
        score = cvss[0]["cvssData"]["baseScore"] if cvss else None # Obtiene el score CVSS si está disponible
        severity = cvss[0]["cvssData"]["baseSeverity"] if cvss else None # Obtiene la severidad CVSS si está disponible
        descriptions = cve.get("descriptions", []) # Obtiene las descripciones disponibles
        desc = next((d["value"] for d in descriptions if d["lang"] == "en"), None)
        results.append({"id": cve["id"], "score": score, "severity": severity, "desc": desc})
    return results

find_cves = query_nvd

if __name__ == "__main__":
    for cve in query_nvd("Apache httpd 2.4.7"):
        print(cve['id'], cve['score'], cve['severity'], cve['desc'][:100] + "...")