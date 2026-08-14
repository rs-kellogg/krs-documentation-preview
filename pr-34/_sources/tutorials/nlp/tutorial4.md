# Open-Source LLMs for Text Analysis

This tutorial covers running open-source LLMs on KLC for text analysis research. Open-source models are preferable when your data is sensitive, when you need full reproducibility, or when cost at scale is a concern.

For a broader overview of why and when to use open-source models, see the [Open Source LLMs guide](/guides/llm/llm).

## Using Ollama on KLC

[Ollama](https://ollama.com/) provides a simple server/client interface for running open-source LLMs. On KLC, start the server with a shared launcher script.

### Start the Server

After logging onto KLC, start the server in a [tmux](/services/klc/user-guide/klc-tmux) session (the script runs in the foreground):

```bash
/kellogg/software/Modules/modulefiles/klc-main-ollama/bin/start_ollama_server.sh
```

When the server is ready, the script prints the node hostname and port — use those values for API calls below. For the full ready-banner reference, environment variables, and the GPU (`sbatch`) path, see [Open Source LLMs on KLC](/services/klc/user-guide/llm-klc).

### Connect with Python

```bash
module purge
module load mamba/24.3.0
eval "$('/hpc/software/mamba/24.3.0/bin/conda' 'shell.bash' 'hook' 2> /dev/null)"
source "/hpc/software/mamba/24.3.0/etc/profile.d/mamba.sh"
mamba create --prefix=./env ollama python=3.13
mamba activate ./env
```

```python
from ollama import Client

HOST = "localhost"  # same node as the server
PORT = 8234         # from the ready banner

client = Client(host=f"http://{HOST}:{PORT}")
```

Browse additional models at [ollama.com/search](https://ollama.com/search).

## Running a Prompt

```python
from ollama import Client

HOST = "localhost"  # same node as the server
PORT = 8234         # from the ready banner

client = Client(host=f"http://{HOST}:{PORT}")

# Pull a model (only needed once)
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

For the broader cost, privacy, and performance comparison between open-source and paid APIs, see [Open Source LLMs](/guides/llm/llm).

## Example: Batch Classification

```python
from ollama import Client

HOST = "localhost"  # same node as the server
PORT = 8234         # from the ready banner

client = Client(host=f"http://{HOST}:{PORT}")

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
