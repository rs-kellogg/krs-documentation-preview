# Open Source LLMs

Open source large language models (LLMs) can be run locally or on KLC's computing infrastructure, giving you full control over your data and analysis pipeline. This page covers why you might choose an open-source model and how to get started on KLC.

For hands-on tutorials on using LLMs for text analysis, see the [NLP Tutorials](/tutorials/nlp/nlp).

## Why Open-Source LLMs?

| Feature | Open-Source LLMs | Paid / Proprietary APIs |
|---|---|---|
| **Cost** | Free (outside of resource wait time) | Usage-based pricing, scales with volume |
| **Data Privacy** | Data stays in your environment | Data sent to external servers |
| **Reproducibility** | Pin exact model version; weights inspectable | Models can update without notice |
| **Customization** | Fine-tune on your own data | Limited by provider APIs |
| **Transparency** | Full access to weights and architecture | Closed-box systems |

For research involving sensitive, proprietary, or IRB-governed data, running a model locally on KLC ensures data never leaves your controlled environment.

## Models Available on KLC

Commonly used open-source LLM weights have already been downloaded to KLC at:

```
/kellogg/data/llm_models_opensource
```

This avoids large downloads and storage issues in your home directory.

## Using Ollama on KLC

[Ollama](https://ollama.com/) provides a simple server/client interface for running open-source LLMs. It is available on KLC via the `klc-llm-pipeline` module.

### Start the Ollama Server

```bash
module load klc-llm-pipeline/1.0
ollama_start
```

This sets two important environment variables and starts the server as a background process:

- `OLLAMA_PORT` – the port the server listens on
- `OLLAMA_MODELS` – where downloaded models are stored (defaults to `/scratch/$USER/Ollama-Models`)

Verify the server is running:

```bash
curl http://localhost:${OLLAMA_PORT}/api/version
```

### Connect with Python

```python
import ollama
import os

client = ollama.Client(host=f"http://localhost:{os.environ.get('OLLAMA_PORT')}")
```

Install the Python library with:

```bash
pip install ollama
```

### Model Storage

Set `OLLAMA_MODELS` to a location outside your home directory (80 GB quota) before downloading models:

```bash
export OLLAMA_MODELS=/scratch/$USER/Ollama-Models
```

To make this permanent, add it to `~/.bashrc`. Browse available models at [ollama.com/search](https://ollama.com/search).

## Using Hugging Face / Transformers

[Hugging Face Transformers](https://huggingface.co/) is another popular option, especially for fine-tuning or when you need more control over the inference pipeline. Contact KRS at [rs@kellogg.northwestern.edu](mailto:rs@kellogg.northwestern.edu) if you need guidance on setting up a Transformers workflow on KLC.

## Workshop Materials

The **Open Source LLMs the Right Way** workshop (April 2024) covers model selection and deployment on KLC:

- Workshop book: [krs-openllm-cookbook](https://rs-kellogg.github.io/krs-openllm-cookbook/welcome.html)
- Sample scripts: [GitHub repo](https://github.com/rs-kellogg/krs-openllm-cookbook/tree/main/scripts)

## Related Pages

- [Open Source LLMs on KLC (user guide)](../../services/klc/user-guide/llm-klc.md) – command-line reference for running LLMs on KLC
- [NLP Tutorials: Open-Source LLMs for Text Analysis](/tutorials/nlp/tutorial4) – hands-on tutorial
- [Choosing an LLM](/guides/openai/llm-intro) – comparison of open vs. closed models
