#!/usr/bin/env python3
"""K8s 巡检脚本：检查 Pod 异常、节点状态、证书过期。"""

import argparse
import glob
import subprocess
from datetime import datetime, timezone

from kubernetes import client, config


# ========== 参数解析 ==========
def parse_args():
    parser = argparse.ArgumentParser(description="K8s 巡检脚本")
    parser.add_argument("--restart", type=int, default=3,
                        help="Pod 容器重启次数超过该值报警（默认 3）")
    parser.add_argument("--cert-days", type=int, default=30,
                        help="证书剩余天数少于该值报警（默认 30）")
    parser.add_argument("--namespace", type=str, default=None,
                        help="只检查指定命名空间（默认所有）")
    return parser.parse_args()


# ========== 检查 1：Pod ==========
def check_pods(v1, args):
    problems = []

    if args.namespace:
        pods = v1.list_namespaced_pod(namespace=args.namespace).items
    else:
        pods = v1.list_pod_for_all_namespaces().items

    for pod in pods:
        if pod.status.phase != "Running":
            problems.append(
                f"[Pod] {pod.metadata.namespace}/{pod.metadata.name}: Phase={pod.status.phase}"
            )
        else:
            for cs in pod.status.container_statuses or []:
                if cs.restart_count >= args.restart:
                    problems.append(
                        f"[Pod] {pod.metadata.namespace}/{pod.metadata.name}: "
                        f"容器 {cs.name} 重启 {cs.restart_count} 次"
                    )
    return problems


# ========== 检查 2：节点 ==========
def check_nodes(v1):
    problems = []
    nodes = v1.list_node().items

    for node in nodes:
        ready = False
        for cond in node.status.conditions:
            if cond.type == "Ready" and cond.status == "True":
                ready = True
                break
        if not ready:
            problems.append(f"[Node] {node.metadata.name}: NotReady")

    return problems


# ========== 检查 3：证书 ==========
def check_certs(args):
    problems = []
    cert_dir = "/var/lib/rancher/k3s/server/tls"
    cert_files = glob.glob(f"{cert_dir}/*.crt")

    for cert_file in cert_files:
        result = subprocess.run(
            ["openssl", "x509", "-enddate", "-noout", "-in", cert_file],
            capture_output=True,
            text=True,
        )
        if result.returncode != 0:
            continue

        date_str = result.stdout.strip().split("=", 1)[1]
        expire_date = datetime.strptime(
            date_str, "%b %d %H:%M:%S %Y %Z"
        ).replace(tzinfo=timezone.utc)
        days_left = (expire_date - datetime.now(timezone.utc)).days

        if days_left <= args.cert_days:
            problems.append(f"[Cert] {cert_file}: {days_left} 天后过期")

    return problems


# ========== 输出报告 ==========
def print_report(problems):
    print("=" * 60)
    print(f"巡检完成 | 异常 {len(problems)} 个")
    print("=" * 60)

    if not problems:
        print("✓ 所有资源正常")
        return

    for p in problems:
        print(f"✗ {p}")


# ========== 主流程 ==========
def main():
    args = parse_args()
    config.load_kube_config()
    v1 = client.CoreV1Api()

    problems = []
    problems.extend(check_pods(v1, args))
    problems.extend(check_nodes(v1))
    problems.extend(check_certs(args))

    print_report(problems)


if __name__ == "__main__":
    main()
