# Open Source LLMs on KLC

## Why Open-Source LLMs?

Open-source large language models offer key advantages for research:

* **Data Security & Privacy** — Models run entirely on KLC; no data leaves your environment, making them well-suited for proprietary, sensitive, or IRB-governed datasets.
* **Reproducibility** — Pin exact model versions and share weights alongside your code so others can replicate your results.
* **Long-Term Availability** — Weights are publicly accessible; your research is not dependent on a vendor's API remaining available.
* **Customization** — Fine-tune models on your own domain-specific data (finance, marketing, healthcare, etc.).

## Running Models with Ollama

[Ollama](https://ollama.com/) provides a simple server/client interface for running open-source LLMs. On KLC, start the server with a shared launcher script at `/kellogg/software/Modules/modulefiles/klc-main-ollama/bin/start_ollama_server.sh`. The same script runs on CPU (KLC main) or GPU (KLC Reserve); only the invocation changes.

### Choose CPU or GPU

| | CPU on KLC main | GPU on KLC Reserve |
|---|---|---|
| **Command** | Run the script directly | Submit with `sbatch` |
| **Best for** | Smaller models, interactive work | Larger models, GPU acceleration |
| **How-to** | This page | [Ollama Inference on KLC Reserve GPUs](/services/klc-reserve/ollama-example) and [GPU Jobs](/services/klc-reserve/gpu-jobs) |

### Start the Server

```bash
# CPU (KLC main)
/kellogg/software/Modules/modulefiles/klc-main-ollama/bin/start_ollama_server.sh

# GPU (KLC Reserve)
sbatch /kellogg/software/Modules/modulefiles/klc-main-ollama/bin/start_ollama_server.sh
```

Defaults are enough for a first run. The script starts Ollama in a Singularity container, selects an available port, stores models under `/scratch/$USER/Ollama-Models` when scratch is available, and pulls the default model (`gemma4:12b`).

On KLC main, the script runs in the foreground and holds the terminal until the server exits. Start it in a [tmux](klc-tmux) session (or a second SSH session) and send API requests from another shell on the same node. On KLC Reserve, `sbatch` runs the server in the background; tail the job log for the node hostname and port.

For GPU jobs, change to a writable directory before submitting — the log file (`ollama-<job-id>.out`) is written in your current working directory.

### Optional Environment Variables

Override settings by prefixing the command. None of these are required.

| Variable | Default | Purpose |
|---|---|---|
| `MODEL` | `gemma4:12b` | Ollama model name (see the [Ollama library](https://ollama.com/library)) |
| `PORT` | Auto-selected (7000–11000) | TCP port for the server |
| `OLLAMA_MODELS` | `/scratch/$USER/Ollama-Models` | Directory for downloaded model weights |
| `OLLAMA_NUM_PARALLEL` | `4` | Concurrent request limit inside the container |
| `SIF_IMAGE` | Site-managed image | Advanced override for the Singularity image path |

```bash
MODEL=gemma4:31b /kellogg/software/Modules/modulefiles/klc-main-ollama/bin/start_ollama_server.sh
MODEL=gemma4:31b sbatch /kellogg/software/Modules/modulefiles/klc-main-ollama/bin/start_ollama_server.sh
```

For models much larger than the default, request more GPUs on the command line: `sbatch --gres=gpu:2 /kellogg/software/Modules/modulefiles/klc-main-ollama/bin/start_ollama_server.sh`.

### Read Node and Port

When the server is ready, the script prints a banner with the node hostname, port, and API URLs. Use those values for API calls — do not assume port `11434`.

On KLC main, query from another shell on the same node with `--host localhost` and the printed port. From a login node to a GPU job, use the GPU node hostname from the job log, not `localhost`. See [Ollama Inference on KLC Reserve GPUs](/services/klc-reserve/ollama-example) for the GPU workflow.

Verify the server with `curl`:

```bash
curl http://localhost:<PORT>/api/tags
```

Replace `<PORT>` with the port from the ready banner.

### Connect with Python

Install the Ollama Python client in a local environment:

```bash
module purge
module load mamba/24.3.0
eval "$('/hpc/software/mamba/24.3.0/bin/conda' 'shell.bash' 'hook' 2> /dev/null)"
source "/hpc/software/mamba/24.3.0/etc/profile.d/mamba.sh"
mamba create --prefix=./env ollama python=3.13
mamba activate ./env
```

Pass the hostname and port from the ready banner:

```python
import argparse
from ollama import Client

parser = argparse.ArgumentParser()
parser.add_argument("--host", default="localhost")
parser.add_argument("--port", type=int, required=True)
parser.add_argument("--model", default="gemma4:12b")
args = parser.parse_args()

client = Client(host=f"http://{args.host}:{args.port}")

response = client.chat(
    model=args.model,
    messages=[
        {"role": "system", "content": "You are a helpful research assistant."},
        {"role": "user",   "content": "Summarize the key risks in this 10-K excerpt: ..."},
    ],
    options={"temperature": 0, "seed": 42},
)
print(response["message"]["content"])
```

Run with the port from the ready banner, for example:

```bash
python my_script.py --port 8234
```

### Via Quest OnDemand

Open the [Quest OnDemand](https://quest.northwestern.edu/pun/sys/dashboard) Jupyter app and select **"ollama"** as the pre-installed kernel — this starts the server automatically alongside JupyterHub.

## Workshop Materials

The **Open Source LLMs the Right Way** workshop (April 2024) covers model selection and deployment on KLC in depth:

- Workshop book: [krs-openllm-cookbook](https://rs-kellogg.github.io/krs-openllm-cookbook/welcome.html)
- Sample scripts: [GitHub repo](https://github.com/rs-kellogg/krs-openllm-cookbook/tree/main/scripts)

## Related Pages

- [Open Source LLMs Guide](/guides/llm/llm) — overview and comparison with paid APIs
- [NLP Tutorial 4: Open-Source LLMs for Text Analysis](/tutorials/nlp/tutorial4) — hands-on tutorial with batch classification examples
- [GPU Concepts and Options](/services/klc-reserve/gpu-concepts) — GPU-accelerated inference for larger models
- [Ollama Inference on KLC Reserve GPUs](/services/klc-reserve/ollama-example) — serve and query models with Ollama on Reserve GPU nodes
- [vLLM Inference on KLC Reserve GPUs](/services/klc-reserve/vllm-example) — serve and query open-source models on Reserve GPU nodes
