# 纯 K8s 部署 YAML

这两个文件不依赖 Helm，直接用 `kubectl apply` 部署。用于快速验证 Jaeger 链路追踪。

| 文件 | 内容 | 端口 |
|---|---|---|
| `jaeger.yaml` | Jaeger all-in-one（Deployment + Service） | UI 30086，OTLP HTTP 4318 |
| `demo.yaml` | 带 OpenTelemetry 埋点的 Flask demo | 5000 |

## 部署
```bash
kubectl apply -f k8s/jaeger.yaml
kubectl apply -f k8s/demo.yaml
