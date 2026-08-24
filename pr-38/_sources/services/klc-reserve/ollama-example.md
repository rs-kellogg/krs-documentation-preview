# Ollama Inference on KLC Reserve GPUs

Serve an open-source model with [Ollama](https://ollama.com/) inside a Singularity container on a KLC Reserve GPU node, then query the server from a login node with the Ollama Python client. The server job and the API calls are separate steps: submit the shared launcher script with `sbatch`; send requests from elsewhere while that job is active.

```{note}
See [Open Source LLMs](/guides/llm/llm) for an overview of every open-source LLM workflow on KLC — interactive, GPU, and tutorial.
```

## Prerequisites

- KLC access and permission to submit to the `kellogg` partition
- Familiarity with [GPU Jobs](gpu-jobs) — GPUs are available only through KLC Reserve, not on login nodes
- Write access to scratch space for downloaded model weights

For CPU-based Ollama on KLC main, see [Open Source LLMs on KLC](/services/klc/user-guide/llm-klc).

## Overview

1. Change to a writable folder and submit the launcher script with `sbatch`.
2. Tail the job log until the server reports ready; note the **node hostname** and **port**.
3. From a login node, install the `ollama` Python package and run a test query against the server using those values.

```{note}
The server runs inside your SLURM job on the allocated GPU node. API calls run separately — typically from a KLC login node in an interactive shell. You do not need to submit the Python client as a second job for this example. Keep the server job running while you query it.
```

## Submit the Server Job

Change to a writable directory before submitting — the job log (`ollama-<job-id>.out`) is written in your current working directory:

```bash
mkdir -p ~/ollama-example && cd ~/ollama-example
# or
mkdir -p /kellogg/proj/<your-netid>/ollama-example && cd /kellogg/proj/<your-netid>/ollama-example
```

Submit the shared launcher script:

```bash
sbatch /kellogg/software/Modules/modulefiles/klc-main-ollama/bin/start_ollama_server.sh
```

Defaults are enough for a first run. To serve a different model, prefix the command:

```bash
MODEL=gemma4:31b sbatch /kellogg/software/Modules/modulefiles/klc-main-ollama/bin/start_ollama_server.sh
```

For models much larger than the default ~12B parameters, request more GPUs on the command line:

```bash
MODEL=gemma4:31b sbatch --gres=gpu:2 /kellogg/software/Modules/modulefiles/klc-main-ollama/bin/start_ollama_server.sh
```

For other optional settings (`PORT`, `OLLAMA_MODELS`, `OLLAMA_NUM_PARALLEL`, and advanced overrides), see the environment variable table on [Open Source LLMs on KLC](/services/klc/user-guide/llm-klc).

## Wait for Ready

Monitor the job and tail the log:

```bash
squeue -u $USER
tail -f ollama-<job-id>.out
```

Wait until the log shows the ready banner:

```text
============================================================
 Ollama is ready
============================================================

 Model:
   gemma4:12b

 Node:
   qgpu0202

 Port:
   8234

 Native Ollama API:
   http://qgpu0202:8234

 OpenAI-compatible API:
   http://qgpu0202:8234/v1
```

Use these values when connecting from a login node:

| Banner field | Python flag | Example |
|---|---|---|
| `Node:` | `--host` | `qgpu0202` |
| `Port:` | `--port` | `8234` |
| `Model:` | `--model` | `gemma4:12b` |

The hostname in `Native Ollama API: http://qgpu0202:8234` is the GPU node where your job is running — not `localhost`. From a login node, `localhost` would refer to the login node itself, where no Ollama server is listening.

## Query From a Login Node

Install the Ollama Python client in a local environment:

```bash
module purge
eval "$('/hpc/software/mamba/24.3.0/bin/conda' 'shell.bash' 'hook' 2> /dev/null)"
source "/hpc/software/mamba/24.3.0/etc/profile.d/mamba.sh"
mamba create --prefix=./env python=3.13 --yes
mamba activate ./env
python -m pip install ollama
```

Save the client script below as `query_ollama.py`. Run it from a login node while the server job is still in `RUNNING` state. Pass the hostname and port from the job log — not the script defaults:

```bash
python query_ollama.py --host qgpu0202 --port 8234 --model gemma4:12b
```

```python
import argparse
import logging

from ollama import Client

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Query an Ollama server on KLC Reserve")
    parser.add_argument(
        "--host",
        default="localhost",
        help="Hostname of the GPU node running the Ollama server (from the job log)",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=8234,
        help="Port the Ollama server is listening on (from the job log)",
    )
    parser.add_argument(
        "--model",
        default="gemma4:12b",
        help="Ollama model name (must match MODEL in the launcher)",
    )
    return parser.parse_args()


def ensure_model_available(client, model):
    available = {m.model for m in client.list().models}
    normalized = model if ":" in model else f"{model}:latest"
    if model in available or normalized in available:
        logger.info("Model already available: %s", model)
        return

    logger.info("Model not found locally: %s — pulling ...", model)
    last_status = None
    for progress in client.pull(model, stream=True):
        if progress.status != last_status:
            logger.info("pull %s: %s", model, progress.status)
            last_status = progress.status
    logger.info("Model pulled: %s", model)


def main() -> None:
    args = parse_args()
    client = Client(host=f"http://{args.host}:{args.port}")
    logger.info("Connected to http://%s:%s  |  model: %s", args.host, args.port, args.model)
    ensure_model_available(client, args.model)

    response = client.chat(
        model=args.model,
        messages=[{"role": "user", "content": "Say hello in one sentence."}],
    )
    print("Reply:", response["message"]["content"])


if __name__ == "__main__":
    main()
```

You can also verify connectivity with `curl` before running Python:

```bash
curl http://qgpu0202:8234/api/tags
```

Replace `qgpu0202` and `8234` with the hostname and port from your job log.

## Tips

- Keep the SLURM job running for as long as you need to send API requests. When the job ends or is cancelled, the server stops and clients can no longer connect.
- Model weights download into `/scratch/$USER/Ollama-Models` on first pull and are reused in later jobs.
- For HuggingFace-style batch serving or very large models, see [vLLM Inference on KLC Reserve GPUs](vllm-example).

## Related Pages

- [GPU Jobs](gpu-jobs) — request and monitor GPU nodes on the `kellogg` partition
- [vLLM Inference on KLC Reserve GPUs](vllm-example) — OpenAI-compatible serving for larger models and batch inference
- [Open Source LLMs on KLC](/services/klc/user-guide/llm-klc) — CPU-based inference with Ollama on KLC main
- [When to Use KLC Reserve](when-to-use) — interactive vs. scheduled workloads
