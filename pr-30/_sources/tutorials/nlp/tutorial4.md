# Open-Source LLMs for Text Analysis

This tutorial covers running open-source LLMs on KLC for text analysis research. Open-source models are preferable when your data is sensitive, when you need full reproducibility, or when cost at scale is a concern.

For a broader overview of why and when to use open-source models, see the [Open Source LLMs guide](/guides/llm/llm).

## Using Ollama on KLC

[Ollama](https://ollama.com/) provides a simple server/client interface for running open-source LLMs. The `klc-llm-pipeline` module handles the setup for you.

### Start the Server

After logging onto KLC:

```bash
module load klc-llm-pipeline/1.0
ollama_start
```

This sets two environment variables and starts the Ollama server as a background process:

- `OLLAMA_PORT` — the port the server listens on
- `OLLAMA_MODELS` — where models are stored (defaults to `/scratch/$USER/Ollama-Models`)

Verify the variables were set:

```python
import os
print(f"OLLAMA_PORT:   {os.environ.get('OLLAMA_PORT')}")
print(f"OLLAMA_MODELS: {os.environ.get('OLLAMA_MODELS')}")
```

Verify the server is running:

```bash
curl http://localhost:${OLLAMA_PORT}/api/version
# → {"version":"..."}
```

### Connect with Python

```bash
pip install ollama
```

```python
import ollama
import os

client = ollama.Client(host=f"http://localhost:{os.environ.get('OLLAMA_PORT')}")
```

### Model Storage

Set `OLLAMA_MODELS` to avoid filling your 80 GB home directory:

```bash
export OLLAMA_MODELS=/scratch/$USER/Ollama-Models
```

To make this permanent, add it to `~/.bashrc`. Pre-downloaded model weights are also available at:

```
/kellogg/data/llm_models_opensource
```

Browse available models at [ollama.com/search](https://ollama.com/search).

## Running a Prompt

```python
import ollama, os

client = ollama.Client(host=f"http://localhost:{os.environ.get('OLLAMA_PORT')}")

# Pull a model (only needed once; skip if using pre-downloaded weights)
client.pull("llama3.2")

response = client.chat(
    model="llama3.2",
    messages=[
        {"role": "system", "content": "You are a helpful research assistant."},
        {"role": "user",   "content": "Summarize the key risks in this 10-K excerpt: ..."},
    ],
    options={"temperature": 0, "seed": 42},
)
print(response["message"]["content"])
```

## Reproducibility Settings

Open-source models give you full control over reproducibility:

| Setting | What It Does |
|---|---|
| `temperature=0` | Deterministic output |
| `seed=42` | Fixes random state (where supported) |
| Model version pinning | Use `model:tag` (e.g., `llama3.2:3b`) to freeze the model version |

Always record the model name and tag in your logs. Unlike API providers, you can ensure the exact same model weights are used across runs.

## Comparing Open-Source and Paid APIs

| | Open-Source (Ollama/KLC) | Paid API (OpenAI, Anthropic) |
|---|---|---|
| **Data stays local** | ✓ | ✗ |
| **Cost** | Free (KLC resources) | Per-token billing |
| **Reproducibility** | Exact version control | Models update without notice |
| **Performance** | Slightly behind frontier | State-of-the-art |
| **Setup** | Requires `module load` and `ollama_start` | Requires API key |

## Example: Batch Classification

```python
import ollama, os, csv, datetime

client = ollama.Client(host=f"http://localhost:{os.environ.get('OLLAMA_PORT')}")

def classify_text(text: str, model: str = "llama3.2") -> str:
    response = client.chat(
        model=model,
        messages=[
            {
                "role": "system",
                "content": (
                    "Classify the sentiment of the following text as one of "
                    "[Positive, Negative, Neutral]. Return only the label."
                ),
            },
            {"role": "user", "content": text},
        ],
        options={"temperature": 0, "seed": 42},
    )
    return response["message"]["content"].strip()

# Batch process a list of documents
documents = ["Revenue exceeded expectations.", "Significant litigation risk.", "Operations were stable."]
results   = [(doc, classify_text(doc)) for doc in documents]

for doc, label in results:
    print(f"{label:10} | {doc}")
```

## Using Quest OnDemand

An alternative to the command line: open the [Quest OnDemand](https://quest.northwestern.edu/pun/sys/dashboard) Jupyter interactive app and select **"ollama"** as the pre-installed kernel. This automatically starts the Ollama server alongside JupyterHub.

## Next Steps

- [Tutorial 5: Validation and Rigor](tutorial5) — ensuring your results meet academic standards
- [Open Source LLMs Guide](/guides/llm/llm) — broader guide including workshop materials
- [Launching Jobs on KLC](/services/klc/user-guide/klc-software) — running batch jobs at scale
