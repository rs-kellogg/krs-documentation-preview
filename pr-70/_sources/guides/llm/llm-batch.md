# LLM Batch Pipeline

The LLM Batch Pipeline is a tool for running large, auditable batches of LLM requests against tabular research data. It converts tabular data into structured, inspectable prompts, submits them to a provider, and standardizes the responses for analysis — separating preparation from execution so you can review prompts and cost estimates before anything is submitted.

## Key Features

- Immutable, inspectable prepared requests before submission
- Cost estimation and provider limit validation
- Record-level provenance tracking, with raw responses and retries stored separately
- Source files remain unmodified
- Support for per-record file attachments (PNG/PDF)
- Retry management, provider comparisons, and batch cancellation with recovery

## Supported Providers

The pipeline supports OpenAI and Anthropic APIs, as well as self-hosted models served through [Ollama](https://ollama.com/) or [vLLM](https://docs.vllm.ai/) — including deployments on KLC. See [Open Source LLMs on KLC](/services/klc/user-guide/llm-klc) and [LLM API Usage](/services/klc/user-guide/llm-api) for the underlying KLC workflows.

## Resources

- Online book: [LLM Batch Pipeline documentation](https://rs-kellogg.github.io/llm-batch_pipeline/)
- Source code: [GitHub repo](https://github.com/rs-kellogg/llm-batch_pipeline)

Maintained by Kellogg Research Support.
