# ============================================================
# metrics.py - 指标收集和统计
# ============================================================

import csv
import os
import time
from typing import List, Dict
import statistics
from config import METRICS_CSV, REPORT_FILE, RESULTS_DIR


class MetricsCollector:
    def __init__(self):
        self.results: List[Dict] = []
        self.start_time: float = None
        self.end_time: float = None
        os.makedirs(RESULTS_DIR, exist_ok=True)

    def start(self):
        self.start_time = time.time()
        print(f"[Metrics] 开始记录，时间: {time.strftime('%Y-%m-%d %H:%M:%S')}")

    def record(self, result: Dict):
        self.results.append(result)

    def finish(self):
        self.end_time = time.time()

    def _percentile(self, data: List[float], p: int) -> float:
        if not data:
            return 0.0
        sorted_data = sorted(data)
        idx = int(len(sorted_data) * p / 100)
        idx = min(idx, len(sorted_data) - 1)
        return round(sorted_data[idx], 4)

    def summarize(self) -> Dict:
        total = len(self.results)
        success = [r for r in self.results if r["status"] == "success"]
        failed = [r for r in self.results if r["status"] == "error"]

        ttfts = [r["ttft"] for r in success if r["ttft"] is not None]
        latencies = [r["latency"] for r in success if r["latency"] is not None]

        total_time = self.end_time - self.start_time if self.end_time else 0
        throughput = len(success) / total_time if total_time > 0 else 0

        summary = {
            "total_requests": total,
            "success_requests": len(success),
            "failed_requests": len(failed),
            "total_time_sec": round(total_time, 2),
            "throughput_req_per_sec": round(throughput, 4),

            # TTFT 统计
            "ttft_mean": round(statistics.mean(ttfts), 4) if ttfts else 0,
            "ttft_p50": self._percentile(ttfts, 50),
            "ttft_p90": self._percentile(ttfts, 90),
            "ttft_p99": self._percentile(ttfts, 99),
            "ttft_min": round(min(ttfts), 4) if ttfts else 0,
            "ttft_max": round(max(ttfts), 4) if ttfts else 0,

            # Latency 统计
            "latency_mean": round(statistics.mean(latencies), 4) if latencies else 0,
            "latency_p50": self._percentile(latencies, 50),
            "latency_p90": self._percentile(latencies, 90),
            "latency_p99": self._percentile(latencies, 99),
            "latency_min": round(min(latencies), 4) if latencies else 0,
            "latency_max": round(max(latencies), 4) if latencies else 0,
        }
        return summary

    def save_csv(self):
        if not self.results:
            return
        fieldnames = list(self.results[0].keys())
        with open(METRICS_CSV, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(self.results)
        print(f"[Metrics] 详细结果已保存: {METRICS_CSV}")

    def print_report(self):
        summary = self.summarize()
        report = f"""
╔══════════════════════════════════════════════════════╗
║           vllm-omni 推理模拟器测试报告               ║
╠══════════════════════════════════════════════════════╣
║ 总请求数:        {summary['total_requests']:<6}                          ║
║ 成功请求数:      {summary['success_requests']:<6}                          ║
║ 失败请求数:      {summary['failed_requests']:<6}                          ║
║ 总耗时:          {summary['total_time_sec']:<8.2f} 秒                    ║
║ 实际吞吐量:      {summary['throughput_req_per_sec']:<8.4f} 请求/秒              ║
╠══════════════════════════════════════════════════════╣
║ TTFT（首Token延迟）                                  ║
║   平均值:        {summary['ttft_mean']:<8.4f} 秒                    ║
║   P50:           {summary['ttft_p50']:<8.4f} 秒                    ║
║   P90:           {summary['ttft_p90']:<8.4f} 秒                    ║
║   P99:           {summary['ttft_p99']:<8.4f} 秒                    ║
║   最小值:        {summary['ttft_min']:<8.4f} 秒                    ║
║   最大值:        {summary['ttft_max']:<8.4f} 秒                    ║
╠══════════════════════════════════════════════════════╣
║ Latency（端到端延迟）                                ║
║   平均值:        {summary['latency_mean']:<8.4f} 秒                    ║
║   P50:           {summary['latency_p50']:<8.4f} 秒                    ║
║   P90:           {summary['latency_p90']:<8.4f} 秒                    ║
║   P99:           {summary['latency_p99']:<8.4f} 秒                    ║
║   最小值:        {summary['latency_min']:<8.4f} 秒                    ║
║   最大值:        {summary['latency_max']:<8.4f} 秒                    ║
╚══════════════════════════════════════════════════════╝
"""
        print(report)
        with open(REPORT_FILE, "w", encoding="utf-8") as f:
            f.write(report)
        print(f"[Metrics] 报告已保存: {REPORT_FILE}")
