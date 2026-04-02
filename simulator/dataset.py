# ============================================================
# dataset.py - 数据集加载器
# 支持 llama_questions 与 LibriSpeech-test 两种数据集
# ============================================================

import base64
import csv
import os
from typing import List, Dict
from config import (
    DATASET_NAME,
    LLAMA_QUESTIONS_DIR,
    LLAMA_QUESTIONS_TSV,
    LIBRISPEECH_TEST_DIR,
)


MIME_BY_EXT = {
    ".wav": "audio/wav",
    ".flac": "audio/flac",
    ".mp3": "audio/mpeg",
    ".m4a": "audio/mp4",
    ".ogg": "audio/ogg",
}


def _build_request(
    request_id: str,
    question: str,
    answer: str,
    audio_path: str,
) -> Dict:
    ext = os.path.splitext(audio_path)[1].lower()
    audio_mime = MIME_BY_EXT.get(ext, "application/octet-stream")

    with open(audio_path, "rb") as af:
        audio_b64 = base64.b64encode(af.read()).decode("utf-8")

    return {
        "id": request_id,
        "question": question,
        "answer": answer,
        "audio_filename": os.path.basename(audio_path),
        "audio_path": audio_path,
        "audio_mime": audio_mime,
        "audio_b64": audio_b64,
    }


def _load_llama_questions() -> List[Dict]:
    requests_pool = []

    with open(LLAMA_QUESTIONS_TSV, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f, delimiter="\t")
        for row in reader:
            audio_filename = row["Wav Filename"].strip()
            audio_path = os.path.join(LLAMA_QUESTIONS_DIR, audio_filename)

            if not os.path.exists(audio_path):
                print(f"[WARN] 文件不存在，跳过: {audio_path}")
                continue

            request = _build_request(
                request_id=os.path.splitext(audio_filename)[0],
                question=row["Questions"].strip(),
                answer=row["Answer"].strip(),
                audio_path=audio_path,
            )
            requests_pool.append(request)

    return requests_pool


def _load_librispeech_test() -> List[Dict]:
    requests_pool = []

    if not os.path.isdir(LIBRISPEECH_TEST_DIR):
        raise FileNotFoundError(f"LibriSpeech-test 目录不存在: {LIBRISPEECH_TEST_DIR}")

    audio_files = []
    for name in os.listdir(LIBRISPEECH_TEST_DIR):
        audio_path = os.path.join(LIBRISPEECH_TEST_DIR, name)
        if not os.path.isfile(audio_path):
            continue
        ext = os.path.splitext(name)[1].lower()
        if ext in MIME_BY_EXT:
            audio_files.append(audio_path)

    audio_files.sort()

    for audio_path in audio_files:
        audio_filename = os.path.basename(audio_path)
        request_id = os.path.splitext(audio_filename)[0]

        request = _build_request(
            request_id=request_id,
            question="Please transcribe the speech content in this audio.",
            answer="",
            audio_path=audio_path,
        )
        requests_pool.append(request)

    return requests_pool


def load_dataset(dataset_name: str = DATASET_NAME) -> List[Dict]:
    """
    根据数据集名称加载请求池。
    每个元素格式：
    {
        "id": "1",
        "question": "What is the capital of France?",
        "answer": "Paris",
        "audio_filename": "1.wav",
        "audio_path": "/full/path/to/1.wav",
        "audio_mime": "audio/wav",
        "audio_b64": "<base64编码的音频>",
    }
    """
    normalized = dataset_name.strip().lower()

    if normalized == "llama_questions":
        requests_pool = _load_llama_questions()
    elif normalized in {"librispeech_test", "librispeech-test"}:
        requests_pool = _load_librispeech_test()
    else:
        raise ValueError(
            f"不支持的数据集: {dataset_name}. 可选值: llama_questions, librispeech_test"
        )

    print(f"[Dataset] 数据集={normalized}，成功加载 {len(requests_pool)} 条请求")
    return requests_pool


if __name__ == "__main__":
    pool = load_dataset()
    print(f"示例请求: {pool[0]['question']} -> 答案: {pool[0]['answer']}")
