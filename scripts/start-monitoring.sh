#!/usr/bin/env sh
set -eu
docker compose -f monitoring/docker-compose.yml up --build -d
cat <<'EOF'
Monitoring stack started:
- Portfolio: http://localhost:8080
- Grafana:   http://localhost:3000  (admin / admin)
- Graphite:  http://localhost:8081
- Nagios:    http://localhost:8082/nagios/  (nagiosadmin / nagios)

Wait 1-3 minutes for metrics and Nagios checks to appear.
EOF
