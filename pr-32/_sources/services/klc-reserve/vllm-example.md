# vLLM Inference on KLC Reserve GPUs

Serve an open-source model with [vLLM](https://docs.vllm.ai/) inside a Singularity container on a KLC Reserve GPU node, then query the server from a login node with the OpenAI Python client. The job exposes an OpenAI-compatible HTTP API for chat, streaming, and batch inference.

## Prerequisites

- KLC access and permission to submit to the `kellogg` partition
- Familiarity with [GPU Jobs](gpu-jobs) — GPUs are available only through KLC Reserve, not on login nodes
- Write access to a project or scratch directory for the Singularity image (`.sif`) and HuggingFace model cache

## Overview

1. Configure and submit a SLURM batch script that starts `vllm serve` in a container.
2. Tail the job log until the server reports ready; note the node hostname and port.
3. From a login node, install the `openai` client and run a test query against the server.

## Configure the Job

Save the script below as `run_vllm.slurm`. Edit the `#SBATCH` directives and user configuration variables before submitting. The highlighted section handles image pull, container launch, and health checks — you do not need to change it.

| Variable | Purpose |
|---|---|
| `MODEL` | HuggingFace model ID or local path inside the container |
| `SIF_IMAGE` | Path to the Singularity image (`.sif`); must be in a directory you can write to |
| `HF_HOME` | HuggingFace cache directory for downloaded weights |
| `HF_TOKEN` | Required for gated models; export before submit or leave empty for public models |
| `#SBATCH --gres` | Number of GPUs; tensor parallel size follows automatically via `$SLURM_GPUS_ON_NODE` |

Set `SIF_IMAGE` to a path under your project or scratch space — for example `/kellogg/proj/<your-netid>/containers/vllm-openai.sif` or `/scratch/$USER/containers/vllm-openai.sif`. If the file does not exist, the script pulls `docker://vllm/vllm-openai:v0.27.1` on first run. The initial pull can take several minutes.

```{code-block} bash
:emphasize-lines: 42-129
:linenos:

#!/bin/bash
# =============================================================================
# Slurm submission script for running vLLM via Singularity
# Serves an OpenAI-compatible HTTP API on the allocated node(s).
#
# Usage:
#   sbatch run_vllm.slurm
#
# After the job starts, query the server from a login node or another job:
#   curl http://<NODE_HOSTNAME>:${PORT}/v1/models
# =============================================================================

#SBATCH --job-name=vllm-serve
#SBATCH --output=logs/vllm-%j.out
#SBATCH --partition=kellogg
#SBATCH --account=kellogg
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=1
#SBATCH --gres=gpu:1
#SBATCH --mem=32G
#SBATCH --time=02:00:00
#SBATCH --signal=B:SIGTERM@60

module purge
module load singularityce/4.3.1-gcc-8.5.0

# =============================================================================
# User configuration — set these before submitting
# =============================================================================

MODEL="microsoft/Phi-4-mini-instruct"
TENSOR_PARALLEL_SIZE=$SLURM_GPUS_ON_NODE
PORT=8001
SIF_IMAGE="/kellogg/proj/<your-netid>/containers/vllm-openai.sif"
DOCKER_IMAGE="docker://vllm/vllm-openai:v0.27.1"
HF_HOME="/scratch/$USER/hf_home"
HF_TOKEN="$HF_TOKEN"
LOCAL_MODELS_DIR=""
EXTRA_VLLM_ARGS=""

# =============================================================================
# Do not edit below — environment setup and server launch
# =============================================================================

set -euo pipefail

mkdir -p "$(dirname "${SLURM_SUBMIT_DIR:-$(pwd)}/logs")" logs

echo "=========================================="
echo "Job ID      : ${SLURM_JOB_ID}"
echo "Node        : ${SLURMD_NODENAME}"
echo "GPUs        : ${SLURM_GPUS_ON_NODE:-${SLURM_JOB_GPUS:-N/A}}"
echo "Model       : ${MODEL}"
echo "TP size     : ${TENSOR_PARALLEL_SIZE}"
echo "Port        : ${PORT}"
echo "SIF image   : ${SIF_IMAGE}"
echo "Start time  : $(date)"
echo "=========================================="

if [[ ! -f "${SIF_IMAGE}" ]]; then
    echo "[INFO] SIF image not found. Pulling ${DOCKER_IMAGE} ..."
    mkdir -p "$(dirname "${SIF_IMAGE}")"
    singularity pull --disable-cache "${SIF_IMAGE}" "${DOCKER_IMAGE}"
    echo "[INFO] Pull complete: ${SIF_IMAGE}"
else
    echo "[INFO] Using cached SIF image: ${SIF_IMAGE}"
fi

mkdir -p "${HF_HOME}"
BINDS="${HF_HOME}:/hf_home"

if [[ -n "${LOCAL_MODELS_DIR}" && -d "${LOCAL_MODELS_DIR}" ]]; then
    BINDS="${BINDS},${LOCAL_MODELS_DIR}:/models:ro"
fi

SINGULARITY_ENV_ARGS=""

if [[ -n "${HF_TOKEN}" ]]; then
    SINGULARITY_ENV_ARGS="${SINGULARITY_ENV_ARGS} --env HF_TOKEN=${HF_TOKEN}"
fi

SINGULARITY_ENV_ARGS="${SINGULARITY_ENV_ARGS} --env VLLM_PORT=${PORT}"
SINGULARITY_ENV_ARGS="${SINGULARITY_ENV_ARGS} --env NCCL_SOCKET_IFNAME=^lo,docker0"
SINGULARITY_ENV_ARGS="${SINGULARITY_ENV_ARGS} --env HF_HOME=/hf_home"

cleanup() {
    echo "[INFO] Caught shutdown signal — stopping vLLM server (PID ${VLLM_PID:-unknown})"
    [[ -n "${VLLM_PID:-}" ]] && kill -SIGTERM "${VLLM_PID}" 2>/dev/null || true
    wait "${VLLM_PID:-}" 2>/dev/null || true
    echo "[INFO] vLLM server stopped."
}
trap cleanup SIGTERM SIGINT

echo "[INFO] Starting vLLM server..."

singularity exec \
    --nv \
    --bind "${BINDS}" \
    ${SINGULARITY_ENV_ARGS} \
    "${SIF_IMAGE}" \
    vllm serve "${MODEL}" \
        --host 0.0.0.0 \
        --port "${PORT}" \
        --tensor-parallel-size "${TENSOR_PARALLEL_SIZE}" \
        ${EXTRA_VLLM_ARGS} &

VLLM_PID=$!
echo "[INFO] vLLM PID: ${VLLM_PID}"

echo "[INFO] Waiting for server to become ready on port ${PORT}..."
MAX_WAIT=300
ELAPSED=0
until curl -sf "http://localhost:${PORT}/health" > /dev/null 2>&1; do
    sleep 5
    ELAPSED=$(( ELAPSED + 5 ))
    if [[ ${ELAPSED} -ge ${MAX_WAIT} ]]; then
        echo "[ERROR] Server did not become ready within ${MAX_WAIT}s — aborting."
        kill -SIGTERM "${VLLM_PID}" 2>/dev/null || true
        exit 1
    fi
done

echo "[INFO] vLLM server is ready."
echo "[INFO] OpenAI-compatible API: http://${SLURMD_NODENAME}:${PORT}/v1"
echo "[INFO] Available models     : http://${SLURMD_NODENAME}:${PORT}/v1/models"

wait "${VLLM_PID}"
echo "[INFO] vLLM server exited. Job finishing."
```

```{tip}
To reduce GPU memory use, set `EXTRA_VLLM_ARGS` — for example `--gpu-memory-utilization 0.85 --max-model-len 8192`. For larger models on fewer GPUs, consider quantization flags such as `--quantization awq` or `--quantization gptq`.
```

For multi-GPU jobs, increase `#SBATCH --gres` (for example `--gres=gpu:2` or `--gres=gpu:h100:4`). `TENSOR_PARALLEL_SIZE` tracks the allocated GPU count automatically.

## Submit and Wait for Ready

```bash
mkdir -p logs
sbatch run_vllm.slurm
```

Monitor the job and tail the log:

```bash
squeue -u $USER
tail -f logs/vllm-<job-id>.out
```

Wait until the log shows:

```text
[INFO] vLLM server is ready.
[INFO] OpenAI-compatible API: http://qgpu0202:8001/v1
[INFO] Available models     : http://qgpu0202:8001/v1/models
```

Use the hostname and port from your log (here, `qgpu0202` and `8001`) when connecting from a login node.

## Query From a Login Node

Install the OpenAI Python client in a local environment:

```bash
module purge
module load mamba/24.3.0
mamba create --prefix=./env openai python=3.13
eval "$('/hpc/software/mamba/24.3.0/bin/conda' 'shell.bash' 'hook' 2> /dev/null)"
conda activate ./env
```

Save the client script below as `query_vllm.py`, then run a chat test using the hostname and port from the job log:

```bash
python query_vllm.py --host qgpu0202 --port 8001 --example chat
```

```python
import argparse
import os

from openai import OpenAI


def make_client(host: str, port: int, api_key: str = "EMPTY") -> OpenAI:
    return OpenAI(
        base_url=f"http://{host}:{port}/v1",
        api_key=api_key,
    )


def get_model(client: OpenAI) -> str:
    models = client.models.list()
    return models.data[0].id


def chat_example(client: OpenAI, model: str) -> None:
    print("\n=== Chat Completion ===")

    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Explain what vLLM is in two sentences."},
    ]

    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=0.7,
        max_tokens=256,
    )

    print("Model :", response.model)
    print("Reply :", response.choices[0].message.content)
    print("Usage :", response.usage)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Query a vLLM OpenAI-compatible server")
    parser.add_argument(
        "--host",
        default=os.environ.get("VLLM_HOST", "localhost"),
        help="Hostname or IP of the vLLM server",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=int(os.environ.get("VLLM_PORT", 8000)),
        help="Port the vLLM server is listening on",
    )
    parser.add_argument(
        "--example",
        choices=["chat"],
        default="chat",
        help="Which example to run",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    client = make_client(args.host, args.port)
    model = get_model(client)
    print(f"[INFO] Connected to http://{args.host}:{args.port}/v1  |  model: {model}")
    chat_example(client, model)


if __name__ == "__main__":
    main()
```

The full client in the source example also supports streaming, text completion, and batch requests via `--example stream`, `completion`, or `batch`.

## Gated Models

For models that require HuggingFace authentication (for example Llama 3), export your token before submitting:

```bash
export HF_TOKEN=<your-huggingface-token>
sbatch run_vllm.slurm
```

## Related Pages

- [GPU Jobs](gpu-jobs) — request and monitor GPU nodes on the `kellogg` partition
- [Ollama Inference on KLC Reserve GPUs](ollama-example) — submit the shared Ollama launcher with `sbatch` and query from a login node
- [GPU Concepts and Options](gpu-concepts) — when GPU acceleration helps
- [Open Source LLMs on KLC](/services/klc/user-guide/llm-klc) — CPU-based inference with the same Ollama launcher on KLC main
- [When to Use KLC Reserve](when-to-use) — interactive vs. scheduled workloads
