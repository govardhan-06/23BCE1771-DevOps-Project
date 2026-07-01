#!/usr/bin/env sh
set -eu
docker compose -f monitoring/docker-compose.yml down || true
docker compose -f jenkins/docker-compose.yml down || true
docker rm -f portfolio-local portfolio-jenkins-deployment 2>/dev/null || true
