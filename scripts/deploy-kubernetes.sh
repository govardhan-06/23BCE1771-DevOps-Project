#!/usr/bin/env sh
set -eu
IMAGE="23bce1771-devops-project:1.0"

docker build -t "$IMAGE" .

if command -v minikube >/dev/null 2>&1; then
  minikube image load "$IMAGE"
fi

kubectl apply -f k8s/deployment.yaml
kubectl rollout status deployment/portfolio-deployment --timeout=120s
kubectl get pods -l app=portfolio
kubectl get service portfolio-service

echo "Docker Desktop Kubernetes URL: http://localhost:30080"
if command -v minikube >/dev/null 2>&1; then
  echo "Minikube URL: $(minikube service portfolio-service --url 2>/dev/null || true)"
fi
