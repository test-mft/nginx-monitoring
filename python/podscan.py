#!/usr/bin/env python3
from kubernetes import client,config
config.load_kube_config()
v1 = client.CoreV1Api()
pods = v1.list_pod_for_all_namespaces().items

problems = []

nodes = v1.list_node().items
for node in nodes:
    ready = False
    for cond in node.status.conditions:
        if cond.type == "Ready" and cond.status == "True":
           ready = True
           break
        if not ready:
            problems.append(f"节点{node.metadata.name}:Notready")

for pod in pods:
    if pod.status.phase != "Running":
      problems.append(f"{pod.metadata.namespace}/{pod.metadata.name}:Phase={pod.status.phase}")
    else:
      for cs in pod.status.container_statuses or []:
          if cs.restart_count >= 3:
               problems.append(f"{pod.metadata.namespace}/{pod.metadata.name}:容器{cs.name}重启{cs.restart_count}次")

# 输出节点资源
print("\n节点资源：")
for node in nodes:
    cpu = node.status.capacity.get("cpu", "?")
    mem = node.status.capacity.get("memory", "?")
    print(f"  {node.metadata.name}: CPU={cpu}, 内存={mem}")
print("=" * 50)
print(f"巡检完成 | 异常{len(problems)}个")
print("=" * 50)

if not problems:
    print("所有pod正常")
else:
    for p in problems:
        print(f"{p}")


