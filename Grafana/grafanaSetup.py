import requests
import subprocess
import time

# Docker setup commands
docker_commands = [
    "docker network create monitoring",
    "docker run -d --name prometheus --network monitoring -p 9090:9090 prom/prometheus",
    "docker run -d --name grafana --network monitoring -p 3000:3000 grafana/grafana",
    "docker run -d --name loki --network monitoring -p 3100:3100 grafana/loki:2.8.2"
]

print("Starting Docker containers...")
for cmd in docker_commands:
    subprocess.run(cmd, shell=True)

# Wait for Grafana to start
time.sleep(15)

# Grafana API details
grafana_url = "http://localhost:3000"
grafana_user = "admin"
grafana_pass = "admin"
auth = (grafana_user, grafana_pass)

# Step 1: Add Prometheus as data source
prometheus_ds = {
    "name": "Prometheus",
    "type": "prometheus",
    "url": "http://prometheus:9090",
    "access": "proxy",
    "isDefault": True
}
requests.post(f"{grafana_url}/api/datasources", auth=auth, json=prometheus_ds)

# Step 2: Add Loki as data source
loki_ds = {
    "name": "Loki",
    "type": "loki",
    "url": "http://loki:3100",
    "access": "proxy"
}
requests.post(f"{grafana_url}/api/datasources", auth=auth, json=loki_ds)

# Step 3: Create Dashboard
dashboard = {
    "dashboard": {
        "id": None,
        "title": "Monitoring Lab Dashboard",
        "panels": [
            {
                "title": "CPU Usage",
                "type": "graph",
                "datasource": "Prometheus",
                "targets": [{"expr": "rate(node_cpu_seconds_total[1m])"}],
                "gridPos": {"x": 0, "y": 0, "w": 12, "h": 8}
            },
            {
                "title": "Memory Usage",
                "type": "graph",
                "datasource": "Prometheus",
                "targets": [{"expr": "node_memory_MemAvailable_bytes"}],
                "gridPos": {"x": 12, "y": 0, "w": 12, "h": 8}
            },
            {
                "title": "Disk I/O",
                "type": "graph",
                "datasource": "Prometheus",
                "targets": [{"expr": "rate(node_disk_io_time_seconds_total[1m])"}],
                "gridPos": {"x": 0, "y": 8, "w": 12, "h": 8}
            },
            {
                "title": "Application Errors",
                "type": "logs",
                "datasource": "Loki",
                "targets": [{"expr": '{app="myapp"} |= "ERROR"'}],
                "gridPos": {"x": 12, "y": 8, "w": 12, "h": 8}
            }
        ]
    },
    "overwrite": True
}
resp = requests.post(f"{grafana_url}/api/dashboards/db", auth=auth, json=dashboard)
print ("Dashboard created:", resp.status_code, resp.text)

