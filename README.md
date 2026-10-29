# 私有镜像仓库配置

## 这两个文件是什么

| 文件 | 放哪 | 作用 |
|---|---|---|
| `daemon.json.example` | Docker 客户端机器上的 `/etc/docker/daemon.json` | 让 Docker 信任 HTTP 私有仓库（用于推镜像） |
| `registries.yaml.example` | K3s 节点上的 `/etc/rancher/k3s/registries.yaml` | 让 containerd 信任 HTTP 私有仓库（用于拉镜像） |

**推镜像走 Docker 客户端，拉镜像走 K3s 节点的 containerd。两个程序、两份配置、互不相干。**

## 使用步骤

1. 复制 `.example` 为正式文件，去掉 `.example` 后缀。
2. 把 `<your-registry-ip>` 替换成你的仓库 IP。
3. Docker 客户端机器：改 `/etc/docker/daemon.json`，然后 `sudo systemctl restart docker`。
4. K3s 节点：改 `/etc/rancher/k3s/registries.yaml`，然后 `sudo systemctl restart k3s`。
5. 验证推：`docker push <your-registry-ip>:5000/myapp:tag`。
6. 验证拉：`sudo k3s crictl pull <your-registry-ip>:5000/myapp:tag`。

## 踩过的坑

- **验证拉取用 `crictl`，不用 `ctr`**：`ctr` 不读 CRI 的 registry 配置，默认走 HTTPS，会误报 `server gave HTTP response to HTTPS client`。
- **推成功 ≠ 拉得下来**：Docker 配了 `insecure-registries` 只影响推；K3s 节点必须单独配 `registries.yaml` 才能拉。
- **改完必须重启**：两份配置都不热加载。

## 真实配置文件不进 Git

`daemon.json` 和 `registries.yaml` 里有内网 IP，已在 `.gitignore` 中排除。仓库里只放 `.example` 模板。
