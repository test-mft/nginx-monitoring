# Day 1：多阶段构建对比

## 文件
- `app.py`：返回 "Hello from Docker!" 的 Flask 服务
- `Dockerfile.single`：单阶段，镜像约 900MB+
- `Dockerfile.multi`：多阶段，镜像约 60-90MB

## 对比实验
```bash
docker build -f Dockerfile.single -t myapp:single .
docker build -f Dockerfile.multi -t myapp:multi .
docker images | grep myapp
docker history myapp:single
docker history myapp:multi
