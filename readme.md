# K8s 可观测性实验仓库

记录从 Docker 基础到 K8s 可观测性（指标 + 日志 + 链路）再到 CI/CD 的学习过程。
既是笔记，也是环境重建包。

## 目录说明

| 目录 | 内容 |
|---|---|
| `docs/` | 概念笔记和踩坑记录 |
| `docker/` | Dockerfile 和 demo 应用源码 |
| `helm/` | nginx-monitoring Chart |
| `registry/` | 私有仓库配置模板（不含真实 IP/密码） |
| `k8s/` | 纯 K8s 部署 YAML |
| `observability/` | Loki / Grafana / Jaeger 相关笔记和查询模板 |
| `cicd/` | GitHub Actions / GitLab CI 配置模板 |
| `scripts/` | 环境重建脚本 |

## 快速开始

1. 读 `docs/troubleshooting.md`，了解踩过的坑和修复方法
2. 按 `scripts/rebuild.sh` 重建实验环境
3. 查 `observability/promql-logql-cheatsheet.md` 找查询语法模板

## 技术栈

- 容器：Docker（多阶段构建）
- 编排：K3s（单节点）
- 应用交付：Helm
- 指标：Prometheus + Grafana
- 日志：Loki + Promtail
- 链路：Jaeger + OpenTelemetry
- CI/CD：GitHub Actions
