# ============================================================
# main.py - 模拟器入口
# 用法：python main.py [--qps 1.0] [--total 20] [--seed 42]
# ============================================================

import argparse
import os
import sys

# 将 simulator 目录加入 Python 路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config import QPS, TOTAL_REQUESTS, DATASET_NAME, get_results_paths
from dataset import load_dataset
from sampler import sample_requests
from runner import run
from metrics import MetricsCollector


def parse_args():
    parser = argparse.ArgumentParser(description="vllm-omni 推理模拟器")
    parser.add_argument(
        "--dataset",
        type=str,
        default=DATASET_NAME,
        choices=["llama_questions", "librispeech_test"],
        help=f"选择数据集 (默认: {DATASET_NAME})",
    )
    parser.add_argument("--qps", type=float, default=QPS,
                        help=f"每秒请求数 (默认: {QPS})")
    parser.add_argument("--total", type=int, default=TOTAL_REQUESTS,
                        help=f"总请求数 (默认: {TOTAL_REQUESTS})")
    parser.add_argument("--seed", type=int, default=42,
                        help="随机种子 (默认: 42)")
    return parser.parse_args()


def main():
    args = parse_args()

    print("=" * 60)
    print("       vllm-omni 语音推理模拟器")
    print("=" * 60)
    print(f"  数据集:    {args.dataset}")
    print(f"  QPS:       {args.qps}")
    print(f"  总请求数:  {args.total}")
    print(f"  随机种子:  {args.seed}")
    print("=" * 60)

    output_paths = get_results_paths(args.dataset)

    # 创建输出目录
    os.makedirs(output_paths["results_dir"], exist_ok=True)
    os.makedirs(output_paths["audio_output_dir"], exist_ok=True)

    # Step 1: 加载数据集
    print("\n[Step 1] 加载数据集...")
    pool = load_dataset(args.dataset)

    # Step 2: 有放回采样
    print("\n[Step 2] 有放回随机采样...")
    sampled = sample_requests(pool, n=args.total, seed=args.seed)

    # Step 3: 初始化指标收集器
    metrics = MetricsCollector(
        results_dir=output_paths["results_dir"],
        metrics_csv=output_paths["metrics_csv"],
        report_file=output_paths["report_file"],
    )

    # Step 4: 启动 QPS 控制器发送请求
    print("\n[Step 3] 启动推理模拟...")
    run(sampled, metrics, qps=args.qps)

    # Step 5: 输出报告
    print("\n[Step 4] 生成报告...")
    metrics.save_csv()
    metrics.print_report()

    print("\n模拟完成！")
    print(f"详细结果: {output_paths['metrics_csv']}")
    print(f"汇总报告: {output_paths['report_file']}")


if __name__ == "__main__":
    main()
