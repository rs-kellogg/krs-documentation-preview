# Open Source LLMs on KLC

## Why Open-Source LLMs?

Open-source large language models offer key advantages for research:

* **Data Security & Privacy** — Models run entirely on KLC; no data leaves your environment, making them well-suited for proprietary, sensitive, or IRB-governed datasets.
* **Reproducibility** — Pin exact model versions and share weights alongside your code so others can replicate your results.
* **Long-Term Availability** — Weights are publicly accessible; your research is not dependent on a vendor's API remaining available.
* **Customization** — Fine-tune models on your own domain-specific data (finance, marketing, healthcare, etc.).

## Pre-Downloaded Models

Commonly used model weights are already available on KLC — no large downloads needed:

```
/kellogg/data/llm_models_opensource
```

## Running Models with Ollama

[Ollama](https://ollama.com/) provides a simple server/client interface for running open-source LLMs. It is available on KLC via the `klc-llm-pipeline` module.

### Start the Server

```bash
module load klc-llm-pipeline/1.0
ollama_start
```

This sets `OLLAMA_PORT` and `OLLAMA_MODELS`, then starts the server as a background process. Verify it is running:

```bash
curl http://localhost:${OLLAMA_PORT}/api/version
```

### Set Model Storage Location

Ollama downloads models into `~/.ollama` by default, which will quickly fill your 80 GB home directory quota. Set a better location before pulling any models:

```bash
export OLLAMA_MODELS=/scratch/$USER/Ollama-Models
# To make this permanent:
echo 'export OLLAMA_MODELS=/scratch/$USER/Ollama-Models' >> ~/.bashrc
```

### Connect with Python

```bash
pip install ollama
```

```python
import ollama, os

client = ollama.Client(host=f"http://localhost:{os.environ.get('OLLAMA_PORT')}")

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

### Via Quest OnDemand

Open the [Quest OnDemand](https://quest.northwestern.edu/pun/sys/dashboard) Jupyter app and select **"ollama"** as the pre-installed kernel — this starts the server automatically alongside JupyterHub.

## Workshop Materials

The **Open Source LLMs the Right Way** workshop (April 2024) covers model selection and deployment on KLC in depth:

- Workshop book: [krs-openllm-cookbook](https://rs-kellogg.github.io/krs-openllm-cookbook/welcome.html)
- Sample scripts: [GitHub repo](https://github.com/rs-kellogg/krs-openllm-cookbook/tree/main/scripts)

## Related Pages

- [Open Source LLMs Guide](/guides/llm/llm) — overview and comparison with paid APIs
- [NLP Tutorial 4: Open-Source LLMs for Text Analysis](/tutorials/nlp/tutorial4) — hands-on tutorial with batch classification examples
- [Using GPUs on Quest and KLC](klc-gpu) — GPU-accelerated inference for larger models
