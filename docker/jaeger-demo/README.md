# Jaeger Demo：带 OpenTelemetry 埋点的 Flask 应用

## 作用
验证链路追踪链路：应用埋点 → OTLP → Jaeger → UI 看 Trace/Span。

## 埋点的 6 步因果链
1. 我要上报 Span → 需要 `TracerProvider`
2. Provider 要知道发到哪 → 需要 `OTLPSpanExporter(endpoint=...)`
3. 不能每个 Span 都发一次网络请求 → 套 `BatchSpanProcessor`
4. Provider 配好了要让业务代码拿到 → `trace.set_tracer_provider(provider)`
5. Jaeger 要知道我是哪个服务 → `Resource.create({"service.name": ...})`
6. Flask 请求想自动记 Span → `FlaskInstrumentor().instrument_app(app)`

手动 Span 的形状：
```python
with tracer.start_as_current_span("Span名字"):
    # 要追踪的代码
