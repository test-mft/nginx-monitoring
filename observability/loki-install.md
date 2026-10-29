# Loki + Promtail 安装笔记

## 安装命令

```bash
helm repo add grafana https://grafana.github.io/helm-charts
helm repo update
helm install loki grafana/loki-stack -n monitoring --create-namespace \
  --set grafana.enabled=false \
  --set prometheus.enabled=false \
  --set loki.image.tag=2.9.6
