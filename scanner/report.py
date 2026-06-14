import json
from datetime import datetime
from jinja2 import Environment, FileSystemLoader   # ← el import de jinja va arriba

def save_json(results, target, path="report.json"):
    payload = {
        "target": target,
        "scanned_at": datetime.now().isoformat(),
        "findings": results,
    }
    with open(path, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2, ensure_ascii=False)

def save_html(results, target, path="report.html"):
    env = Environment(loader=FileSystemLoader("templates"))
    template = env.get_template("report.html")
    html = template.render(
        target=target,
        scanned_at=datetime.now().strftime("%Y-%m-%d %H:%M"),
        findings=results,
    )
    with open(path, "w", encoding="utf-8") as f:
        f.write(html)