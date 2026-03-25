# ============================================================
# sampler.py - 有放回随机采样器
# ============================================================

import random
from typing import List, Dict
from config import TOTAL_REQUESTS


def sample_requests(pool: List[Dict], n: int = None, seed: int = 42) -> List[Dict]:
    """
    有放回随机采样 n 个请求。
    - pool: 请求池（全部300条）
    - n: 采样数量，默认使用 config.TOTAL_REQUESTS
    - seed: 随机种子，保证可复现
    返回采样结果列表（可能包含重复请求）
    """
    if n is None:
        n = TOTAL_REQUESTS

    random.seed(seed)
    sampled = random.choices(pool, k=n)  # 有放回采样

    print(f"[Sampler] 从 {len(pool)} 条请求中有放回采样 {n} 条")
    # 统计重复情况
    ids = [r["id"] for r in sampled]
    unique = len(set(ids))
    print(f"[Sampler] 其中唯一请求数: {unique}，重复数: {n - unique}")

    return sampled


if __name__ == "__main__":
    from dataset import load_dataset
    pool = load_dataset()
    sampled = sample_requests(pool, n=10)
    for i, req in enumerate(sampled):
        print(f"  [{i+1}] {req['id']}.wav - {req['question'][:50]}")
