# ============================================================
# config.py - 模拟器全局配置
# ============================================================

# vllm-omni 服务地址
VLLM_HOST = "localhost"
VLLM_PORT = 8091
MODEL_PATH = "/home/sheng-xiang/hedongjun/models"

# 数据集路径
DATASET_DIR = "/home/sheng-xiang/hedongjun/datasets/llama_questions/LLAMA1-Test-Set"
TSV_FILE = f"{DATASET_DIR}/llama_questions_300.tsv"

# 模拟器参数
QPS = 1.0            # 每秒请求数
TOTAL_REQUESTS = 20  # 总共发送多少个请求
OUTPUT_MODALITIES = ["text", "audio"]  # 输出模态

# System prompt
SYSTEM_PROMPT = (
    "You are Qwen, a virtual assistant capable of understanding audio input "
    "and generating text and speech responses. Please answer the question in the audio concisely."
)

# 结果保存路径
RESULTS_DIR = "/home/sheng-xiang/hedongjun/simulator/results"
AUDIO_OUTPUT_DIR = "/home/sheng-xiang/hedongjun/simulator/results/audio"
METRICS_CSV = f"{RESULTS_DIR}/metrics.csv"
REPORT_FILE = f"{RESULTS_DIR}/report.txt"

# 采样参数
THINKER_SAMPLING_PARAMS = {
    "temperature": 0.4,
    "top_p": 0.9,
    "top_k": 1,
    "max_tokens": 1024,
    "repetition_penalty": 1.05,
    "stop_token_ids": [151645],
    "seed": 42,
}
TALKER_SAMPLING_PARAMS = {
    "temperature": 0.9,
    "top_k": 50,
    "max_tokens": 4096,
    "seed": 42,
    "detokenize": False,
    "repetition_penalty": 1.05,
    "stop_token_ids": [2150],
}
CODE2WAV_SAMPLING_PARAMS = {
    "temperature": 0.0,
    "top_p": 1.0,
    "top_k": -1,
    "max_tokens": 65536,
    "seed": 42,
    "detokenize": True,
    "repetition_penalty": 1.1,
}
