# Paid LLMs for Text Analysis

This tutorial covers when and how to use paid LLM APIs (OpenAI, Anthropic, Google) for text analysis research. It complements the rule-based methods in [Tutorial 1](tutorial1) and [Tutorial 2](tutorial2).

## Do LLMs Always Help?

LLMs are powerful but not always the right tool. The key question is: **does the task require understanding context and nuance, or can a rule-based method handle it?**

| Scenario | Better Approach |
|---|---|
| Extract a known pattern (dates, identifiers) | Regex or NLP pipeline |
| Handle negation ("not satisfied") | LLM wins |
| Classify with new/unseen terminology | LLM wins |
| Detect sarcasm or irony | Classic NLP can win |
| Interpret complex nested clauses | LLM wins |
| High-volume, deterministic extraction | Dictionary/TF-IDF |

**Advantages of paid LLMs:**
- Easy to use — send a request, receive structured output
- State-of-the-art contextual understanding

**Disadvantages:**
- Costly — usage-based pricing scales quickly
- Not transparent — model weights and training data are opaque
- Difficult to reproduce — models update without notice

## Basic API Pattern

The same pattern works across providers. Below is OpenAI, but Anthropic (Claude) and Google (Gemini) follow a nearly identical structure.

```python
import os
from openai import OpenAI

# Load key from file (never hardcode it)
KEY_PATH = "/kellogg/proj/<your-netid>/keys/openai-key.txt"
with open(os.path.expanduser(KEY_PATH)) as f:
    client = OpenAI(api_key=f.read().strip())

SYSTEM_PROMPT = "You are a completion engine. Predict the next word based on context."
USER_PROMPT   = "Complete this sentence in 1 word: I should have taken more..."

response = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user",   "content": USER_PROMPT},
    ],
    temperature=0,
    seed=42,
)
print(response.choices[0].message.content)
```

For a script that toggles between Anthropic, OpenAI, and Google, see the [krs-openai-cookbook GitHub repo](https://github.com/rs-kellogg/krs-openai-cookbook).

## Logging

**Always log your runs.** LLM outputs are non-deterministic, models update over time, and you need a record for reproducibility.

Log at minimum: timestamp, model version, system prompt, user prompt, and the raw response.

```python
import csv, os, datetime

def log_to_csv(csv_path, model, ctx_window, sys_prompt, usr_prompt, response, test_result):
    os.makedirs(os.path.dirname(csv_path), exist_ok=True)
    file_exists = os.path.isfile(csv_path)
    with open(csv_path, mode="a", newline="") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["timestamp", "model", "ctx_window",
                             "system_prompt", "user_prompt", "response", "test_result"])
        writer.writerow([
            datetime.datetime.now(), model, ctx_window,
            sys_prompt, usr_prompt, response, test_result,
        ])
```

## Testing LLM Outputs

Because LLMs can introduce errors, hallucinations, and biases, embed automated checks into your pipeline.

A simple approach: validate the grammatical structure of outputs using spaCy.

```python
import spacy

nlp = spacy.load("en_core_web_sm")

def get_pos_tag(text: str) -> str:
    """Return POS tag of the first non-punctuation token."""
    doc = nlp(text)
    for token in doc:
        if not token.is_punct:
            return token.tag_
    return "UNKNOWN"

def test_is_noun(response_text: str) -> str:
    tag = get_pos_tag(response_text.strip())
    return "PASS" if tag.startswith("NN") else f"FAIL ({tag})"

# Example
print(test_is_noun("statistics"))   # → PASS (NN)
print(test_is_noun("running"))      # → FAIL (VBG)
```

Run tests on a known gold standard before processing the full dataset. See [Tutorial 5: Validation and Rigor](tutorial5) for a full framework.

## Demo: Classifying Enron Emails

Enron emails are a commonly used benchmark dataset. The goal: classify an email's tone or topic.

```python
def classify_email(email_text: str, client: OpenAI) -> str:
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are an expert at classifying corporate email communications. "
                    "Classify the tone as one of: [Neutral, Positive, Negative, Urgent]. "
                    "Return only the label."
                ),
            },
            {"role": "user", "content": email_text},
        ],
        temperature=0,
        seed=42,
    )
    return response.choices[0].message.content.strip()
```

## Demo: Classifying 10-K Risk Disclosures

For financial text (e.g., SEC 10-K filings), classify risk factor paragraphs:

```python
RISK_CATEGORIES = ["Market Risk", "Operational Risk", "Regulatory Risk",
                   "Litigation Risk", "Other"]

def classify_risk(paragraph: str, client: OpenAI) -> str:
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content": (
                    f"You are a financial analyst. Classify the following risk disclosure "
                    f"paragraph into exactly one of: {RISK_CATEGORIES}. Return only the label."
                ),
            },
            {"role": "user", "content": paragraph},
        ],
        temperature=0,
        seed=42,
    )
    return response.choices[0].message.content.strip()
```

## Next Steps

- [Tutorial 4: Open-Source LLMs](tutorial4) — run local models on KLC for privacy and reproducibility
- [Tutorial 5: Validation and Rigor](tutorial5) — validating LLM outputs for academic research
- [OpenAI API Guide](/guides/openai/openai-api) — full setup and best practices
