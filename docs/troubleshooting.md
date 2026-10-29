# 踩坑记录

每条按「现象 → 根因 → 修复 → 教训」记，教训那一行是面试时能直接说出口的。

---

## 1. Helm 报 nil pointer

**现象**：`helm template` 报 `nil pointer evaluating interface {}.statusPort`

**根因**：`values.yaml` 文件名写成了 `Values.yaml`（大写 V），Helm 不加载，所有 `.Values.xxx` 求值为 nil。

**修复**：改回小写 `values.yaml`。

**教训**：Helm 的默认 values 文件名必须是小写。报 nil pointer 时，排查顺序是：文件名大小写 → 模板路径和 values 层级是否一致 → key 名拼写是否一致。

---

## 2. Deployment 里 `templates` 写成了复数

**现象**：`kubectl apply` 报 `unknown field "spec.templates"`

**根因**：Deployment 的字段是 `template`（单数），手写时多加了一个 `s`。

**修复**：改成 `spec.template`。

**教训**：K8s 字段名大小写和单复数都敏感。`helm template` 渲染出来后，对照官方文档检查字段名，比 apply 到集群才发现快得多。

---

## 3. `volumeMounts` 缩进错位

**现象**：Deployment 创建失败，报字段不合法。

**根因**：`volumeMounts` 应该属于容器内部（和 `image`、`ports` 同级），写成了和 `containers` 同级；`volumes` 应该和 `containers` 同级，缩进也不对。另外 `mountPath` 写成了 `path`。

**修复**：按正确的层级重写缩进。

**教训**：YAML 的缩进就是结构。`volumeMounts` 在容器里，`volumes` 在 Pod spec 里。写完用 `helm template` 输出看层级，比对着源码猜快。

---

## 4. `ctr` 拉私有镜像报 HTTPS 错误

**现象**：`sudo k3s ctr images pull 172.20.211.10:5000/myapp:day1` 报 `server gave HTTP response to HTTPS client`

**根因**：`ctr` 不读 CRI 的 registry 配置（即 K3s 的 `registries.yaml`），默认走 HTTPS。你的仓库是 HTTP 的。

**修复**：改用 `sudo k3s crictl pull ...` 验证，`crictl` 走 CRI API，会读取 `registries.yaml`。

**教训**：验证 K3s 能不能拉私有镜像，用 `crictl`，不用 `ctr`。两个工具读的配置不同。

---

## 5. Grafana 连不上 Loki

**现象**：Grafana 数据源测试报 `Unable to connect with Loki`，但 Loki Pod 是 Running。

**根因**：Grafana 在 `default` 命名空间，Loki 在 `monitoring`。URL 写成了 `http://loki:3100`，集群 DNS 只在 `default` 里找 `loki`，找不到。

**修复**：URL 改成 `http://loki.monitoring:3100`。

**教训**：跨命名空间访问格式是 `http://<service>.<namespace>:<port>`。同一命名空间才能省略 namespace 部分。

---

## 6. `loki-stack` 健康检查误报

**现象**：URL 改对后，`wget http://loki.monitoring:3100/ready` 返回 `ready`，但 Grafana 数据源测试仍报 `Unable to connect with Loki`。

**根因**：`loki-stack` Chart 默认装的 Loki 版本旧，Grafana 的健康检查查询（`vector(1)+vector(1)`）在旧版 Loki 上解析失败，返回 400。但实际查询功能正常。

**修复**：升级 Loki 镜像到 `2.9.x`（`--set loki.image.tag=2.9.6`）。

**教训**：数据源测试报错不代表数据源不可用。去 Explore 里查一下，能查到日志就说明是健康检查接口的问题。`loki-stack` 已弃用，生产环境用官方 `loki` Chart 或 `loki-distributed`。

---

## 7. Grafana v13 找不到 `+ Add visualization`

**现象**：按旧教程在空白 Dashboard 里找 `+ Add visualization` 按钮，找不到。

**根因**：Grafana v13.3.0 界面改版，入口变成了 `+ Panel`。

**修复**：点 `+ Panel` → `Configure visualization`，进入面板编辑器。

**教训**：教程的界面截图可能和你用的版本不一致。找不到按钮时，先看版本号，再搜“Grafana vX 新建面板”。

---

## 8. `helm create` 的 NOTES.txt 引用不存在的字段

**现象**：`helm template` 报 `nil pointer evaluating interface {}.enabled`，路径是 `NOTES.txt`。

**根因**：`helm create` 生成的 `NOTES.txt` 默认引用 `.Values.httpRoute.enabled`，但你清空 `values.yaml` 重写后，这个字段不存在。

**修复**：删掉 `NOTES.txt`，或者用 `{{- if .Values.httpRoute }}` 包裹相关段落。

**教训**：`helm create` 的示例文件（`NOTES.txt`、`deployment.yaml`、`hpa.yaml` 等）引用了默认 values 的字段。清空 values 后，这些示例文件要么删掉，要么改成引用你实际有的字段。

---

## 9. Jaeger 里看不到任何 Trace

**现象**：Jaeger UI 打开是空的，Service 下拉框没有选项。

**根因**：nginx 和 exporter 没有埋点，不会产生 Trace 数据。Jaeger 只是接收和展示，数据必须由应用主动上报。

**修复**：部署一个带 OpenTelemetry SDK 的应用（demo-service），通过 OTLP 协议把 Span 发给 Jaeger。

**教训**：链路追踪和指标/日志不同，它需要应用主动埋点。没有埋点的应用，Jaeger 里永远看不到它。
