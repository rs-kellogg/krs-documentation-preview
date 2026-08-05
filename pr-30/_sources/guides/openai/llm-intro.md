# Understanding LLMs

## What Is a Language Model?

A **language model** (LM) assigns probabilities to sequences of words. Models are trained — their probabilities estimated — using large collections of naturally occurring text (a *corpus*). A language model can be used to select the most probable next word given the preceding context.

## What Makes a Model "Large"?

A language model is considered **large** when:

- It has billions (or approaching trillions) of parameters
- It was trained on billions or trillions of words/tokens

As scale increases, new *emergent* capabilities appear — such as complex reasoning — that smaller models showed no indication of. This is why large language models have attracted so much research attention.

## The Transformer Architecture

**Transformers** are the key architectural innovation that enabled language models to scale. They allow massive parallelization of training and inference on GPUs. The foundational paper is [Attention Is All You Need](https://arxiv.org/abs/1706.03762) (Vaswani et al., 2017).

## Pre-Training and Fine-Tuning

**Pre-trained** models are trained via self-supervision on vast quantities of text. These are sometimes called *foundation models*. They can be used as-is or further trained (*fine-tuned*) to improve performance on specific domains or tasks.

The assistant-style models most people are familiar with have been further trained using supervised fine-tuning and reinforcement learning from human feedback (**RLHF**) to behave safely and helpfully — going beyond simple next-word prediction.

## Generative Models

**Generative** models produce content as output. "GPT base" models do simple next-word prediction. RLHF-trained assistant models respond to questions in a helpful, contextually aware way.

## Choosing a Model: Open vs. Closed Source

The choice between a closed-source API (like OpenAI or Anthropic) and an open-source model (like Llama or Mistral) depends on your research needs:

| Consideration | Closed-Source (API) | Open-Source (e.g., Ollama on KLC) |
|---|---|---|
| **Ease of use** | Very easy — send a request, get a response | Requires setup on KLC |
| **Performance** | Frontier models (GPT-5, Claude) are state of the art | Slightly behind frontier, improving rapidly |
| **Cost** | Usage-based (per token); costs scale | Free to run on KLC compute |
| **Data privacy** | Data sent to external servers | Data stays on KLC |
| **Reproducibility** | Models update without notice | Pin exact version |
| **Customization** | Limited fine-tuning options | Full access to weights; fine-tune on your data |

**Use a closed-source API when:**
- You need state-of-the-art performance
- Data privacy is not a constraint
- You want the simplest possible setup

**Use an open-source model when:**
- Your data is sensitive, proprietary, or IRB-governed
- You need guaranteed reproducibility
- You want to fine-tune on domain-specific data
- Cost at scale is a concern

## Popular Models

**Closed-source:**
- **OpenAI GPT series** – [platform.openai.com](https://platform.openai.com/docs/overview)
- **Anthropic Claude** – [docs.anthropic.com](https://docs.anthropic.com/en/docs/get-started)
- **Google Gemini** – [ai.google.dev](https://ai.google.dev/gemini-api/docs/models)

**Open-source (available on KLC):**
- Browse available weights at `/kellogg/data/llm_models_opensource`
- Additional models via [Ollama](https://ollama.com/search) or [Hugging Face](https://huggingface.co/)

## Related Pages

- [OpenAI API](openai-api) — Setting up and using the OpenAI API
- [Open Source LLMs Guide](/guides/llm/llm) — Running open-source models on KLC
- [LLM API Usage on KLC](/services/klc/user-guide/llm-api) — Best practices for API workflows on the cluster
