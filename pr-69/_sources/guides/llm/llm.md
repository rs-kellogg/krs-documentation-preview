# Open Source LLMs

Open source large language models (LLMs) can be run locally or on KLC's computing infrastructure, giving you full control over your data and analysis pipeline. Use this page to weigh open-source models against paid APIs, then find the right workflow — interactive use on KLC, GPU-accelerated serving with Ollama or vLLM, or the hands-on NLP research tutorial.

## Why Open-Source LLMs?

| Feature | Open-Source LLMs | Paid / Proprietary APIs |
|---|---|---|
| **Cost** | Free (outside of resource wait time) | Usage-based pricing, scales with volume |
| **Data Privacy** | Data stays in your environment | Data sent to external servers |
| **Reproducibility** | Pin exact model version; weights inspectable | Models can update without notice |
| **Customization** | Fine-tune on your own data | Limited by provider APIs |
| **Transparency** | Full access to weights and architecture | Closed-box systems |

For research involving sensitive, proprietary, or IRB-governed data, running a model locally on KLC ensures data never leaves your controlled environment.

## Using Ollama or vLLM on KLC

[Ollama](https://ollama.com/) and [vLLM](https://docs.vllm.ai/) both provide a server/client interface for running open-source LLMs — Ollama for a quick start with a shared launcher script, vLLM for OpenAI-compatible batch and high-throughput serving. See [Open Source LLMs on KLC](/services/klc/user-guide/llm-klc) for the full CPU and GPU workflow, environment variables, and Python client setup.

## Using Hugging Face / Transformers

[Hugging Face Transformers](https://huggingface.co/) is another popular option, especially for fine-tuning or when you need more control over the inference pipeline. Contact KRS at [rs@kellogg.northwestern.edu](mailto:rs@kellogg.northwestern.edu) if you need guidance on setting up a Transformers workflow on KLC.

## Workshop Materials

The **Open Source LLMs the Right Way** workshop (April 2024) covers model selection and deployment on KLC:

- Workshop book: [krs-openllm-cookbook](https://rs-kellogg.github.io/krs-openllm-cookbook/welcome.html)
- Sample scripts: [GitHub repo](https://github.com/rs-kellogg/krs-openllm-cookbook/tree/main/scripts)

## Where to Go Next

| If you want to... | Go to |
|---|---|
| Run a model interactively on KLC (CPU) | [Open Source LLMs on KLC](/services/klc/user-guide/llm-klc) |
| Serve a model on a GPU with Ollama | [Ollama Inference on KLC Reserve GPUs](/services/klc-reserve/ollama-example) |
| Serve a model on a GPU with vLLM | [vLLM Inference on KLC Reserve GPUs](/services/klc-reserve/vllm-example) |
| Understand CPU vs. GPU and when you need one | [GPU Concepts and Options](/services/klc-reserve/gpu-concepts) |
| Request and submit GPU jobs directly | [GPU Jobs](/services/klc-reserve/gpu-jobs) |
| Use a hosted API (OpenAI, Anthropic, etc.) instead | [LLM API Usage](/services/klc/user-guide/llm-api) |
| Follow a hands-on NLP research tutorial | [Open-Source LLMs for Text Analysis](/tutorials/nlp/tutorial4) |
| Learn general LLM concepts (transformers, model selection) | [Understanding LLMs](/guides/openai/llm-intro) |
