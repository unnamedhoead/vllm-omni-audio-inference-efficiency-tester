# ============================================================
# runner.py - QPS 控制器
# 按照设定的 QPS 速率发送请求
# ============================================================

import time
import threading
from typing import List, Dict
from client import send_request
from metrics import MetricsCollector
from config import QPS


def run(sampled_requests: List[Dict], metrics: MetricsCollector, qps: float = None):
    """
    按 QPS 控制速率依次发送请求。
    - sampled_requests: 已采样好的请求列表
    - metrics: 指标收集器
    - qps: 每秒请求数，默认使用 config.QPS
    """
    if qps is None:
        qps = QPS

    interval = 1.0 / qps  # 每个请求之间的间隔秒数
    total = len(sampled_requests)
    lock = threading.Lock()

    print(f"\n[Runner] 开始发送，QPS={qps}，间隔={interval}s，总请求={total}")
    print(f"[Runner] 预计总耗时: {total * interval:.1f} 秒\n")

    metrics.start()
    t_start = time.time()

    # 用线程池并发发送，避免单线程因等待响应而阻塞 QPS 控制
    threads = []
    results_buffer = [None] * total

    def worker(index, request):
        result = send_request(request, index + 1)
        with lock:
            results_buffer[index] = result
            metrics.record(result)

    for i, request in enumerate(sampled_requests):
        # 精确控制发送时间
        t_target = t_start + i * interval
        t_now = time.time()
        sleep_time = t_target - t_now
        if sleep_time > 0:
            time.sleep(sleep_time)

        t = threading.Thread(target=worker, args=(i, request))
        t.start()
        threads.append(t)
        print(f"[Runner] 已发送第 {i+1}/{total} 个请求 (id={request['id']})")

    # 等待所有请求完成
    print("\n[Runner] 等待所有请求完成...")
    for t in threads:
        t.join()

    metrics.finish()
    print(f"[Runner] 所有请求完成！")
