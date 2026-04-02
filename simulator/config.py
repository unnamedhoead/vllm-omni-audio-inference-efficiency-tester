# ============================================================
# config.py - 模拟器全局配置
# ============================================================

# vllm-omni 服务地址
VLLM_HOST = "localhost"
VLLM_PORT = 8091
MODEL_PATH = "/home/sheng-xiang/hedongjun/models"

# 数据集路径
DATASETS_ROOT = "/home/sheng-xiang/hedongjun/datasets"
DATASET_NAME = "llama_questions"

LLAMA_QUESTIONS_DIR = f"{DATASETS_ROOT}/llama_questions/LLAMA1-Test-Set"
LLAMA_QUESTIONS_TSV = f"{LLAMA_QUESTIONS_DIR}/llama_questions_300.tsv"

LIBRISPEECH_TEST_DIR = f"{DATASETS_ROOT}/LibriSpeech-test"

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
SIMULATOR_ROOT = "/home/sheng-xiang/hedongjun/simulator"


def get_results_paths(dataset_name: str):
    normalized = dataset_name.strip().lower()
    if normalized == "llama_questions":
        result_dir_name = "llama-results"
    elif normalized in {"librispeech_test", "librispeech-test"}:
        result_dir_name = "librispeech-results"
    else:
        result_dir_name = "results"

    results_dir = f"{SIMULATOR_ROOT}/{result_dir_name}"
    return {
        "results_dir": results_dir,
        "audio_output_dir": f"{results_dir}/audio",
        "metrics_csv": f"{results_dir}/metrics.csv",
        "report_file": f"{results_dir}/report.txt",
    }


_default_paths = get_results_paths(DATASET_NAME)
RESULTS_DIR = _default_paths["results_dir"]
AUDIO_OUTPUT_DIR = _default_paths["audio_output_dir"]
METRICS_CSV = _default_paths["metrics_csv"]
REPORT_FILE = _default_paths["report_file"]

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
