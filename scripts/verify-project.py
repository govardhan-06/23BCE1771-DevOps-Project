from pathlib import Path
import json
import sys
import xml.etree.ElementTree as ET

root = Path(__file__).resolve().parents[1]
required = [
    "pom.xml", "Dockerfile", "Jenkinsfile", "k8s/deployment.yaml",
    "monitoring/docker-compose.yml",
    "monitoring/grafana/dashboards/portfolio-dashboard.json",
    "src/main/resources/static/index.html",
]
missing = [item for item in required if not (root / item).exists()]
if missing:
    raise SystemExit(f"Missing files: {missing}")

ET.parse(root / "pom.xml")
json.loads((root / "monitoring/grafana/dashboards/portfolio-dashboard.json").read_text())
html = (root / "src/main/resources/static/index.html").read_text()
for marker in ["Govardhan A R", "Projects", "Contact"]:
    if marker not in html:
        raise SystemExit(f"HTML marker missing: {marker}")

print("Project structure, pom.xml, dashboard JSON, and website markers are valid.")
