# ============================================================
# client.py - vllm-omni 请求客户端
# 发送音频请求，记录 TTFT 和 Latency
# ============================================================

import base64
import os
import time
from typing import Dict
from openai import OpenAI
from config import (
    VLLM_HOST, VLLM_PORT, MODEL_PATH, SYSTEM_PROMPT,
    OUTPUT_MODALITIES, AUDIO_OUTPUT_DIR,
    THINKER_SAMPLING_PARAMS, TALKER_SAMPLING_PARAMS, CODE2WAV_SAMPLING_PARAMS
)

# 初始化 OpenAI 客户端
client = OpenAI(
    api_key="EMPTY",
    base_url=f"http://{VLLM_HOST}:{VLLM_PORT}/v1"
)

SAMPLING_PARAMS = {
    "sampling_params_list": [
        THINKER_SAMPLING_PARAMS,
        TALKER_SAMPLING_PARAMS,
        CODE2WAV_SAMPLING_PARAMS,
    ]
}


def send_request(request: Dict, request_index: int) -> Dict:
    """
    发送单个音频请求到 vllm-omni，返回指标字典。
    返回格式：
    {
        "request_id": "1",
        "question": "...",
        "expected_answer": "...",
        "text_response": "...",
        "ttft": 1.23,       # Time To First Token (秒)
        "latency": 5.67,    # 端到端延迟 (秒)
        "output_tokens": 42,
        "audio_saved": True,
        "audio_path": "...",
        "status": "success" or "error",
        "error_msg": "",
        "send_time": 1234567890.0,
    }
    """
    result = {
        "request_id": request["id"],
        "question": request["question"],
        "expected_answer": request["answer"],
        "text_response": "",
        "ttft": None,
        "latency": None,
        "output_tokens": 0,
        "audio_saved": False,
        "audio_path": "",
        "status": "error",
        "error_msg": "",
        "send_time": time.time(),
    }

    try:
        messages = [
            {
                "role": "system",
                "content": [{"type": "text", "text": SYSTEM_PROMPT}]
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "audio_url",
                        "audio_url": {
                            "url": f"data:audio/wav;base64,{request['audio_b64']}"
                        }
                    }
                ]
            }
        ]

        t_send = time.time()
        ttft_recorded = False
        first_token_time = None
        collected_text = []

        # 使用流式请求以记录 TTFT
        stream = client.chat.completions.create(
            model=MODEL_PATH,
            messages=messages,
            modalities=OUTPUT_MODALITIES,
            extra_body=SAMPLING_PARAMS,
            stream=True,
        )

        for chunk in stream:
            if not ttft_recorded:
                first_token_time = time.time()
                ttft_recorded = True

            for choice in chunk.choices:
                if hasattr(choice, "delta") and choice.delta:
                    content = getattr(choice.delta, "content", None)
                    if content:
                        collected_text.append(content)

        t_end = time.time()

        result["ttft"] = round(first_token_time - t_send, 4) if first_token_time else None
        result["latency"] = round(t_end - t_send, 4)
        result["text_response"] = "".join(collected_text)
        result["output_tokens"] = len(result["text_response"].split())
        result["status"] = "success"

        print(f"  [Request {request_index}] id={request['id']} "
              f"TTFT={result['ttft']}s Latency={result['latency']}s")

    except Exception as e:
        result["error_msg"] = str(e)
        result["status"] = "error"
        print(f"  [Request {request_index}] id={request['id']} ERROR: {e}")

    return result
