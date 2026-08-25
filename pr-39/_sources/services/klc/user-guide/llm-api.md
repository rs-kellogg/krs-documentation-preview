# LLM API Usage

Hosted LLM APIs provide programmatic access to language models over the network. Researchers call these APIs from Python, R, or other environments on KLC to automate text tasks at scale while keeping analysis scripts under version control.

For provider-specific setup (OpenAI keys, billing limits, first API call), see [OpenAI API](/guides/openai/openai-api). For models that run entirely on KLC without sending data externally, see [Open Source LLMs on KLC](llm-klc).

## Hosted API vs. On-Cluster Model

| | Hosted LLM API | Open-source on KLC |
|---|---|---|
| **Data location** | Sent to the provider's servers | Stays on KLC |
| **Cost** | Usage-based (tokens) | Compute time on KLC; no per-token fee |
| **Setup** | API key and client library | Model weights and runtime (Ollama, PyTorch) |
| **Best for** | Latest closed models, rapid prototyping at moderate scale | IRB-governed or proprietary data, large batch jobs at fixed compute cost |

Choose a hosted API when your data governance policies allow external processing and you need a specific commercial model. Choose on-cluster inference when data cannot leave Kellogg systems.

## Data Governance and IRB

Before sending any research data to a third-party API:

- Follow your IRB protocol and Northwestern data governance policies
- Do not send identifiable human-subjects data unless explicitly permitted
- Document which provider and model version processed each dataset

```{warning}
When in doubt, use [open-source models on KLC](llm-klc) or contact [rs@kellogg.northwestern.edu](mailto:rs@kellogg.northwestern.edu) before transmitting data externally.
```

Northwestern does not currently offer an approved institutional LLM API (such as Azure OpenAI). Researchers use provider accounts directly (OpenAI, Anthropic, Google, etc.) subject to data governance policies.

## Workflow on KLC

### 1. Set Up a Python Environment

Create an isolated environment in your project directory. See [Conda Environments on KLC](klc-conda).

```bash
module load mamba
mamba create -p /kellogg/proj/<your-netid>/envs/llm-api python=3.11
source activate /kellogg/proj/<your-netid>/envs/llm-api
pip install openai python-dotenv    # or anthropic, google-generativeai, etc.
```

### 2. Store API Keys Securely

Never commit API keys to Git or embed them in scripts.

Store keys in a file outside your repository:

```bash
mkdir -p /kellogg/proj/<your-netid>/keys
chmod 700 /kellogg/proj/<your-netid>/keys
nano /kellogg/proj/<your-netid>/keys/.env
chmod 600 /kellogg/proj/<your-netid>/keys/.env
```

Example `.env` contents:

```bash
OPENAI_API_KEY=sk-proj-...
```

Load in Python:

```python
from dotenv import load_dotenv
import os

load_dotenv("/kellogg/proj/<your-netid>/keys/.env")
api_key = os.getenv("OPENAI_API_KEY")
```

Add `keys/` and `.env` to your `.gitignore`.

### 3. Write and Test on a Small Sample

Develop prompts and validate outputs on a handful of rows before scaling. Set `temperature=0` and document the model name and version for reproducibility.

### 4. Run at Scale

For large batches, run from a SLURM job so the process continues if your SSH session drops:

```bash
sbatch run_llm_batch.sh
```

See [Submitting SLURM Jobs](/services/klc-reserve/slurm-jobs).

KLC Reserve compute nodes have outbound internet access, so hosted LLM API calls work from batch jobs on the `kellogg` partition.

### 5. Log Prompts, Parameters, and Responses

Save inputs and raw API responses for every run:

```python
import json

record = {
    "model": "gpt-4o-2024-08-06",
    "prompt": prompt_text,
    "response": response.choices[0].message.content,
    "usage": response.usage.model_dump(),
}
with open(f"logs/response_{row_id}.json", "w") as f:
    json.dump(record, f)
```

Log files support replication, debugging, and audit trails.

## Best Practices

**Reproducibility**
- Log all prompts, parameters, and responses
- Record exact model names and versions (for example, `gpt-4o-2024-08-06`, not `gpt-4o`)
- Set `seed` where the provider supports it

**Data privacy**
- Follow IRB and institutional data governance policies
- Redact or aggregate identifiers before API calls when possible

**Cost control**
- Set a maximum billing limit in your provider account
- Test on small samples before full-scale runs
- Use `max_tokens` to cap per-request cost
- Monitor usage at your provider's usage dashboard

**Validation**
- LLMs produce errors, hallucinations, and biases
- Build checks on known examples before deploying at scale
- See [Validation and Rigor](/tutorials/nlp/tutorial5) for a framework

## Rate Limits and Retries

Providers enforce rate limits on requests and tokens per minute. For large batches:

- Add exponential backoff on HTTP 429 responses
- Limit concurrent requests with a small worker pool
- Split work across multiple job array tasks, each with its own rate budget

## Provider Documentation

- [OpenAI API documentation](https://platform.openai.com/docs/overview)
- [Anthropic Claude documentation](https://docs.anthropic.com/en/docs/get-started)
- [Google Gemini API documentation](https://ai.google.dev/gemini-api/docs/models)
- [Groq API documentation](https://console.groq.com/docs/libraries)

## Related Pages

- [OpenAI API](/guides/openai/openai-api) — OpenAI account setup, keys, and first call
- [Open Source LLMs on KLC](llm-klc) — on-cluster models without external data transfer
- [Open Source LLMs Guide](/guides/llm/llm) — broader comparison of approaches
- [Submitting SLURM Jobs](/services/klc-reserve/slurm-jobs) — batch jobs for large API pipelines
