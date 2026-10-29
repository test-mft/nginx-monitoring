# Grafana 面板查询模板

两个面板的查询，直接复制到 Grafana 面板编辑器。语法细节见 `promql-logql-cheatsheet.md`。

## 面板 1：请求速率（Prometheus）

| 项 | 值 |
|---|---|
| 数据源 | Prometheus |
| 查询 | `rate(nginx_http_requests_total[1m])` |
| 可视化 | Time series |
| 标题 | 请求速率 |

含义：nginx 过去 1 分钟平均每秒处理多少请求。

## 面板 2：日志速率（Loki）

| 项 | 值 |
|---|---|
| 数据源 | Loki |
| 查询 | `rate({app="nginx"}[1m])` |
| 可视化 | Time series |
| 标题 | 日志速率 |

含义：过去 1 分钟每秒产生多少条 nginx 日志。

## 联动实验

1. 两个面板放同一个 Dashboard，时间范围统一设为 Last 5 minutes。
2. 发 200 个请求制造尖峰：

```bash
kubectl run curl-load --image=curlimages/curl --restart=never --command -- \
  sh -c "for i in \$(seq 1 200); do curl -s -o /dev/null http://nginx-service; done"
