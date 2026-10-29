# CI/CD 配置模板

两个平台二选一，用哪个就把对应的 `.example` 复制成正式文件。

| 文件 | 复制到 | 触发平台 |
|---|---|---|
| `github-actions-ci.yaml.example` | `.github/workflows/ci.yaml` | GitHub Actions |
| `gitlab-ci.yaml.example` | `.gitlab-ci.yml` | GitLab CI |

## 流水线做什么

1. **helm-validate**：`helm lint` + `helm template`，检查 Chart 语法和渲染。
2. **build-and-push**：构建 Docker 镜像，推送到私有仓库，tag 用 commit SHA。

`build-and-push` 有 `needs: helm-validate`（GitHub）或 `stage: build`（GitLab），Chart 校验失败时不会浪费时间去构建镜像。

## 关键因果链

- **先 lint 后 build**：Chart 语法错了，构建镜像没意义。
- **tag 用 commit SHA 不用 latest**：SHA 唯一对应一次提交，可追溯、可回滚；latest 每次覆盖，无法知道线上跑的是哪个 commit。
- **密码放 Secrets**：配置文件会进 Git，密码明文进 Git 等于泄露。Secrets 运行时注入，日志里自动打码。
- **CI 和 CD 分开**：CI 只负责构建可信产物，CD 负责部署。分开后 CI 不需要集群凭证，权限最小化。

## 不用背的东西

- 具体 `uses` 哪个 action、`run` 什么命令 → 从 GitHub Actions 市场或 GitLab 文档复制。
- 变量名（`REGISTRY_URL`、`IMAGE_NAME`）→ 项目自己定的，跟着项目走。
- YAML 语法 → 用的时候查，记“触发 → 任务 → 步骤”三层结构即可。

## 下一步（未做）

- Push 模式 CD：在流水线末尾加 `helm upgrade`，把新版本推到集群。
- GitOps（Pull 模式）：引入 ArgoCD，CI 只更新 Git 里的镜像 tag，ArgoCD 自动同步集群。
