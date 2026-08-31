# Application Workflow

This page describes a proven workflow for developing research applications with LLMs — from initial idea to production-scale deployment — and walks through a concrete case study.

## Development Cycle

```
Identify dataset + task
        ↓
Engineer a prompt (use Playground)
        ↓
Evaluate on a small sample
    ├── Acceptable → Deploy at scale
    └── Not acceptable → Prompt engineering / fine-tuning
```

### Step 1: Identify Your Dataset and Task

Be precise about what you want to extract or classify. Vague tasks produce vague results. Define:
- What is the input? (a document, a paragraph, a sentence)
- What exactly do you want to extract or infer?
- What format should the output be in?

### Step 2: Engineer Your Prompt

Use the [OpenAI Playground](https://platform.openai.com/playground) to develop prompts interactively before writing code. Tips:

- Use a `system` message to set role and format expectations
- Use structured output (JSON) when you need to parse results programmatically
- Start simple; add constraints only when needed
- See OpenAI's [Prompt Engineering Guide](https://platform.openai.com/docs/guides/prompt-engineering)

### Step 3: Evaluate on a Sample

Test on 20–50 examples before running at scale:
- If performance is unacceptable → revise the prompt
- If prompt engineering isn't enough → consider fine-tuning or a different model
- Always validate against a known gold standard (see [Validation and Rigor](/tutorials/nlp/tutorial5))

### Step 4: Deploy at Scale

Once satisfied with sample performance:
- Structure your code into functions (source code) and scripts
- Add logging and output files for reproducibility
- Run the job on KLC — see [Launching Jobs](../../services/klc/user-guide/klc-software)

## Code Structure Best Practices

```
project/
├── src/           ← Core functions (reusable, testable)
├── scripts/       ← Scripts that compose functions; include runtime tests
├── tests/         ← Unit tests
└── output/        ← Logs and results (never modify; treat as artifacts)
```

- Keep functions in `src/`; compose them in scripts
- Scripts should generate logs
- All code goes in version control (git)
- Save outputs; never modify them after the fact

## Case Study: Extracting Author Information from arXiv Papers

This example demonstrates extracting structured metadata from scientific PDFs — a task that scales to thousands of inputs.

**Research question**: Who are the LLM researchers, where are they located, and what topics do they work on?

**Dataset**: ~1,700 arXiv PDFs containing "Large Language Model" in the abstract.

### Task Definition

For each paper, extract:
- Paper title
- List of author names, email addresses, and affiliations
- Geographic coordinates (latitude/longitude) for each affiliation

**Output schema:**
```json
{
  "title": "The paper's title",
  "authors": [
    {
      "name": "Author Name",
      "email": "name@domain.edu",
      "affiliations": ["0", "1"]
    }
  ],
  "affiliations": [
    {
      "index": "0",
      "name": "University Name",
      "longitude": "-87.6298",
      "latitude": "41.8781"
    }
  ]
}
```

### Implementation

```python
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI()

def extract_authors(paper_text: str) -> dict:
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are an expert research librarian. You return information in JSON format. "
                    "Extract title, authors (with email and affiliation indices), and affiliations "
                    "(with name and lat/lon coordinates) from the first page of a scientific paper."
                ),
            },
            {"role": "user", "content": f'"""\n{paper_text}\n"""'},
        ],
        temperature=0,
        seed=42,
    )
    return response.choices[0].message.content
```

### Logging

Log every run for reproducibility — record timestamp, model version, prompts, and outputs:

```python
import csv, os

def log_to_csv(csv_path, model, system_prompt, user_prompt, response, test_result):
    os.makedirs(os.path.dirname(csv_path), exist_ok=True)
    file_exists = os.path.isfile(csv_path)
    with open(csv_path, mode="a", newline="") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["timestamp", "model", "system_prompt", "user_prompt",
                             "response", "test_result"])
        import datetime
        writer.writerow([datetime.datetime.now(), model, system_prompt,
                         user_prompt, response, test_result])
```

## Takeaways

**Selecting a model**
- Closed-source APIs are easiest and most capable; open-source gives privacy and reproducibility
- Document the exact model version used (e.g., `gpt-4o-2024-08-06`)

**Development workflow**
- Identify dataset → engineer prompt → evaluate sample → deploy at scale

**Structuring and testing code**
- Separate source functions from scripts; add unit tests and logs
- Put everything in version control

## Related Pages

- [OpenAI API](openai-api) — Setting up API access and authentication
- [Understanding LLMs](llm-intro) — Model concepts and choosing a model
- [NLP Tutorials](/tutorials/nlp/nlp) — Hands-on text analysis tutorials with code
- [Launching Jobs on KLC](/services/klc/user-guide/klc-software) — Running scripts at scale
