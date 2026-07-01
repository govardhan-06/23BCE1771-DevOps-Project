#!/usr/bin/env sh
set -eu
IMAGE="23bce1771-devops-project:1.0"
CONTAINER="portfolio-local"

docker build -t "$IMAGE" .
docker rm -f "$CONTAINER" 2>/dev/null || true
docker run -d --name "$CONTAINER" -p 8080:80 "$IMAGE"

echo "Portfolio started at http://localhost:8080"
echo "Health endpoint: http://localhost:8080/health"
