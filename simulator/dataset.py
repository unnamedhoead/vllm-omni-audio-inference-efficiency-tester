# ============================================================
# dataset.py - 数据集加载器
# 读取 llama_questions TSV 文件，构建请求池
# ============================================================

import base64
import csv
import os
from typing import List, Dict
from config import DATASET_DIR, TSV_FILE


def load_dataset() -> List[Dict]:
    """
    读取 TSV 文件和对应 wav 文件，构建请求池。
    每个元素格式：
    {
        "id": "1",
        "question": "What is the capital of France?",
        "answer": "Paris",
        "wav_filename": "1.wav",
        "audio_path": "/full/path/to/1.wav",
        "audio_b64": "<base64编码的音频>",
    }
    """
    requests_pool = []

    with open(TSV_FILE, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f, delimiter="\t")
        for row in reader:
            wav_filename = row["Wav Filename"].strip()
            audio_path = os.path.join(DATASET_DIR, wav_filename)

            if not os.path.exists(audio_path):
                print(f"[WARN] 文件不存在，跳过: {audio_path}")
                continue

            with open(audio_path, "rb") as af:
                audio_b64 = base64.b64encode(af.read()).decode("utf-8")

            requests_pool.append({
                "id": wav_filename.replace(".wav", ""),
                "question": row["Questions"].strip(),
                "answer": row["Answer"].strip(),
                "wav_filename": wav_filename,
                "audio_path": audio_path,
                "audio_b64": audio_b64,
            })

    print(f"[Dataset] 成功加载 {len(requests_pool)} 条请求")
    return requests_pool


if __name__ == "__main__":
    pool = load_dataset()
    print(f"示例请求: {pool[0]['question']} -> 答案: {pool[0]['answer']}")
