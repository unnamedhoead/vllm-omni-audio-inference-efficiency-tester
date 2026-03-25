#!/bin/bash
pkill -f vllm 2>/dev/null
sleep 5

source ~/miniconda3/etc/profile.d/conda.sh
conda activate vllm-omni-env

nohup vllm-omni serve ~/hedongjun/models \
  --omni \
  --port 8091 \
  --stage-configs-path ~/hedongjun/vllm-omni/vllm_omni/model_executor/stage_configs/qwen3_omni_moe_async_chunk.yaml \
  --dtype bfloat16 \
  --max-model-len 32768 \
  > ~/hedongjun/vllm_serve.log 2>&1 &

echo "服务已启动，PID: $!"
echo "查看日志: tail -f ~/hedongjun/vllm_serve.log"
