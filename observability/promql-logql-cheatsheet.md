# PromQL / LogQL 速查表

日常 80% 的查询用这几个模板。不背语法，用的时候复制模板，改指标名/标签名。

## PromQL（数据源：Prometheus）

### 看速率：rate(指标[时间窗口])
```promql
rate(nginx_http_requests_total[1m])
