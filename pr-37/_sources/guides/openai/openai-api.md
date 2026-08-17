# OpenAI API

## Chat vs. API

OpenAI provides two separate services — make sure you're using the right one:

- **ChatGPT** (`chat.openai.com`) — web-based chat interface; not suitable for batch processing
- **OpenAI API** (`platform.openai.com`) — programmatic access; pay-as-you-go; scalable to thousands of inputs

For research workflows, you want the **API**.

## Setting Up

### 1. Create an API Account

Go to [platform.openai.com](https://platform.openai.com/) and create an account (separate from your ChatGPT account).

### 2. Create an API Key

In the [API keys page](https://platform.openai.com/api-keys):

1. Click **Create new secret key**
2. Copy and save it immediately — it will not be shown again
3. **Set a spending limit** under Billing → Limits to avoid unexpected charges

### 3. Store Your Key Securely

```{warning}
Never put your API key directly in source code or commit it to a GitHub repository.
```

The recommended approach is to store your key in a `.env` file and load it at runtime:

```bash
# ~/.env or /kellogg/proj/<your-netid>/keys/.env
OPENAI_API_KEY=sk-proj-...
OPENAI_ORG_ID=org-...
```

Load it in Python:

```python
import os
from dotenv import load_dotenv  # pip install python-dotenv

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
```

Alternatively, store the key in a plain text file and read it:

```python
with open("/kellogg/proj/<your-netid>/keys/openai-key.txt", "r") as f:
    api_key = f.read().strip()
```

## Making Your First API Call

```python
from openai import OpenAI  # pip install openai

client = OpenAI()  # reads OPENAI_API_KEY from environment

response = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "system", "content": "You are a helpful research assistant."},
        {"role": "user",   "content": "Summarize the key ideas in behavioral finance."}
    ],
    temperature=0,   # 0 = deterministic; increase for more variety
    max_tokens=512,
    seed=42          # improves reproducibility
)

print(response.choices[0].message.content)
```

## Best Practices for Research

These best practices align with the [LLM API Usage on KLC](../../services/klc/user-guide/llm-api) recommendations.

**Reproducibility**
- Set `seed` and document the exact `model` version (e.g., `gpt-4o-2024-08-06`)
- Log all prompts, parameters, and responses — models can update and outputs can change
- Save raw API responses before any post-processing

**Cost Management**
- Set a max billing limit in your OpenAI account settings
- Develop and test on small samples before running at scale
- Use `max_tokens` to bound per-request cost

**Data Privacy**
- Check your institution's data governance policies before sending any data to OpenAI
- For sensitive or IRB-governed data, use [open-source models on KLC](../../guides/llm/llm) instead

**Validation**
- LLMs can produce errors, hallucinations, and biases
- Build unit tests that validate outputs on known examples before deploying at scale
- See [Validation and Rigor](/tutorials/nlp/tutorial5) for a framework

## The OpenAI Playground

The [Playground](https://platform.openai.com/playground) is a web-based interface for developing and testing prompts before writing code. Use it to:

- Experiment with different system prompts
- Compare models side by side
- Fine-tune parameters (temperature, max tokens, top_p)

## Monitoring Usage

Track your token usage and costs at [platform.openai.com/usage](https://platform.openai.com/usage). Set alerts under **Billing → Notification thresholds**.

## Related Pages

- [Understanding LLMs](llm-intro) — Model concepts and open vs. closed comparison
- [Application Workflow](openai-workflow) — End-to-end development workflow and case study
- [LLM API Usage on KLC](/services/klc/user-guide/llm-api) — Running API workflows on the cluster
