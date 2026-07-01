import os
import socket
import time
from typing import Dict

import psutil
import requests

GRAPHITE_HOST = os.getenv("GRAPHITE_HOST", "graphite")
GRAPHITE_PORT = int(os.getenv("GRAPHITE_PORT", "2003"))
APP_URL = os.getenv("APP_URL", "http://app/health")
PREFIX = os.getenv("METRIC_PREFIX", "portfolio").strip(".")
INTERVAL = int(os.getenv("INTERVAL_SECONDS", "10"))
STARTED_AT = time.time()


def collect_metrics() -> Dict[str, float]:
    available = 0.0
    response_ms = 0.0
    started = time.perf_counter()
    try:
        response = requests.get(APP_URL, timeout=4)
        available = 1.0 if response.status_code == 200 else 0.0
        response_ms = (time.perf_counter() - started) * 1000
    except requests.RequestException:
        response_ms = (time.perf_counter() - started) * 1000

    memory = psutil.virtual_memory()
    disk = psutil.disk_usage("/")
    net = psutil.net_io_counters()

    return {
        "cpu_percent": psutil.cpu_percent(interval=1),
        "memory_percent": memory.percent,
        "disk_percent": disk.percent,
        "network.bytes_sent": float(net.bytes_sent),
        "network.bytes_received": float(net.bytes_recv),
        "http_availability": available,
        "http_response_ms": response_ms,
        "uptime_seconds": time.time() - STARTED_AT,
    }


def send(metrics: Dict[str, float]) -> None:
    timestamp = int(time.time())
    lines = [f"{PREFIX}.{name} {value:.4f} {timestamp}" for name, value in metrics.items()]
    payload = "\n".join(lines) + "\n"
    with socket.create_connection((GRAPHITE_HOST, GRAPHITE_PORT), timeout=5) as sock:
        sock.sendall(payload.encode("utf-8"))


print(f"Sending metrics to {GRAPHITE_HOST}:{GRAPHITE_PORT} every {INTERVAL}s")
while True:
    try:
        values = collect_metrics()
        send(values)
        print("metrics sent", values, flush=True)
    except (OSError, ValueError) as exc:
        print(f"metrics delivery failed: {exc}", flush=True)
    time.sleep(INTERVAL)
