# vllm-omni Audio Inference Efficiency Tester

版本：V1.2

本项目用于评估 vllm-omni 音频推理服务在不同请求速率（QPS）下的吞吐、延迟与稳定性，支持问答音频与语音转写两类场景。

## 目录结构（核心）

- `models/`：推理模型权重与配置
- `datasets/`：测试数据集
- `simulator/`：压测模拟器代码与结果输出
- `start_vllm.sh`：服务启动脚本（可选）
- `vllm-omni/`：vllm-omni 源码目录

## 支持的数据集

### 1) llama_questions

- 场景：问答音频数据
- 来源目录：`datasets/llama_questions/LLAMA1-Test-Set`
- 标注文件：`llama_questions_300.tsv`
- 模拟器参数值：`--dataset llama_questions`

### 2) librispeech_test

- 场景：语音转写
- 来源目录：`datasets/LibriSpeech-test`
- 模拟器参数值：`--dataset librispeech_test`

## 推理服务启动流程（vllm-omni）

### 1. 每次启动前检查 GPU 显存

```bash
nvidia-smi
```

确认 GPU 0 和 GPU 1 的显存占用均为 4MiB 再继续。

### 2. 如有残留进程，先清理

```bash
pkill -f vllm
sleep 5
```

### 3. 确认进程已清理

```bash
ps aux | grep vllm | grep -v grep
```

### 4. 进入工作目录并激活环境

```bash
cd ~/hedongjun/vllm-omni
conda activate vllm-omni-env
```

### 5. 启动推理服务

```bash
# 可通过使用 CUDA_VISIBLE_DEVICES=2,3 命令指定占用的卡

nohup vllm-omni serve ~/hedongjun/models --omni --port 8091 --stage-configs-path ~/hedongjun/vllm-omni/vllm_omni/model_executor/stage_configs/qwen3_omni_moe_async_chunk.yaml --dtype bfloat16 --max-model-len 32768 > ~/hedongjun/vllm_serve.log 2>&1 &
```

### 6. 监控三阶段（Stage）启动状态

```bash
tail -f ~/hedongjun/vllm_serve.log | grep -E "Stage|startup|initialized|startup complete"
```

## 模拟器启动流程

```bash
cd simulator/
python main.py --dataset librispeech_test --qps 1 --total 20 --seed 42
```

## 模拟器命令行参数（main.py）

### --dataset

- 可选值：
  - `llama_questions`：使用 LLAMA1-Test-Set（问答音频数据）
  - `librispeech_test`：使用 LibriSpeech-test（语音转写场景）
- 默认值：`config.py` 中的 `DATASET_NAME`（当前通常为 `llama_questions`）

### --qps

- 类型：float
- 含义：每秒发送请求数（请求速率）
- 典型值：0.5 / 1 / 2 / 4 / 8 / 16
- 默认值：`config.py` 中的 `QPS`

### --total

- 类型：int
- 含义：本次模拟总请求数（从数据池中有放回采样）
- 典型值：20 / 50 / 120 / 240 / 480
- 默认值：`config.py` 中的 `TOTAL_REQUESTS`

### --seed

- 类型：int
- 含义：随机采样种子（用于复现实验）
- 默认值：42

## 结果输出路径规则（按数据集区分）

当 `dataset = llama_questions`：

- 结果目录：`simulator/llama-results`
- 明细文件：`simulator/llama-results/metrics.csv`
- 报告文件：`simulator/llama-results/report.txt`

当 `dataset = librispeech_test`：

- 结果目录：`simulator/librispeech-results`
- 明细文件：`simulator/librispeech-results/metrics.csv`
- 报告文件：`simulator/librispeech-results/report.txt`

## 常用启动示例

```bash
python simulator/main.py --dataset llama_questions --qps 1 --total 20 --seed 42
python simulator/main.py --dataset librispeech_test --qps 1 --total 20 --seed 42
```

## 结果文件命名补充说明

项目中也可能存在按实验参数归档的历史结果文件，例如：

- `metrics-QPS=16-Total=480.csv`
- `report-QPS=16-Total=480.txt`

用于区分不同批次实验。若你希望统一为固定文件名（`metrics.csv` / `report.txt`）或统一为参数化命名，可在 `simulator/metrics.py` 中进一步规范输出策略。
